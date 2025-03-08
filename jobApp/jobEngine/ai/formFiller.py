import openai
import os
import json
import yaml
from pathlib import Path
import ast
import logging

logger = logging.getLogger(__name__)

class FormFiller:
    def __init__(self):
        # Set up the API key
        secrets_path = Path('input/secrets.yaml')
        secrets = yaml.safe_load(open(secrets_path, 'r'))
        api_key = secrets['api_key']
        openai.api_key = api_key
    
    def set_user_context(self, user_context):
        # Initialize conversation history with user context as a system message
        self.conversation_history = [
            {
                "role": "developer",
                "content": (
                    "You are an AI assistant helping to fill out a job application form. "
                    "Use the following user context to generate accurate and professional responses.\n\n"
                    "Instructions:\n"
                    "- If you lack the necessary information, provide the best possible response to pass the question, even if it requires fabricating an answer.\n"
                    "- If a question requires a numerical response, return only the number without any additional text.\n"
                    "- If a question provides options to choose from, return only one of the given options exactly as it appears, without modifications, additional text, or synonyms.\n"
                    "Example Questions: What is your level of proficiency in English? Options are Native, Professional, Conversational, None.\n"
                    "Example Response: [Professional]\n"
                    "- Return all responses as strings inside a list.\n\n"
                    f"{user_context}"
                )
            }
        ]

    def answer_question(self, question) -> list:
        """Return a list of answers for one or multiple questions in the same order."""
        self.conversation_history.append({"role": "user", "content": question})
        #logger.info(f"AI Conversation History: {self.conversation_history}")
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.7,
            messages=self.conversation_history
        )

        answer = response.choices[0].message.content.strip()
        answer = ast.literal_eval(answer)
        # Validate the answer if the question contains options
        if "options:" in question.lower():
            options_part = question.split("options:")[-1].strip()
            choices = [opt.strip() for opt in options_part.split(",")]

            # Check if the answer is in the list
            if answer not in choices:
                logger.warning(f"Invalid response '{answer[0]}'. Selecting closest valid option.")
                answer[0] = next((opt for opt in choices if opt.lower() in answer[0].lower()), choices[0])

        
        return answer


# Example usage
if __name__ == "__main__":
    # Define your user context (sent only once)
    context = """
    personal_information:
    name: "Alex"
    surname: "Embrata"
    country: "Germany"
    city: "Munich"
    phone_prefix: "+49"
    phone: "1766604"
    email: "Alex.Embrata@gmail.com"
    citizenship: "German Citizenship"
    summary: "
        Innovative System Engineer with a strong background in mechatronics, robotics, and automation, 
        specializing in software development, system architecture, and industrial automation. 
        Over 6 years of experience working on cutting-edge technologies across automotive, Robotics, 
        Energie and advanced manufacturing industries. 
        Adept at designing and implementing high-performance software solutions for autonomous systems, 
        cloud-based infrastructures, and embedded applications.
        Proven ability to lead cross-functional teams, optimize processes, and integrate software with 
        hardware to enhance system efficiency and reliability. Strong expertise in Python, C++, 
        cloud technologies (AWS), DevOps, and software testing automation. Passionate about AI-driven solutions, 
        sustainable technologies, and open-source development.  
        Holds multiple industry-recognized certifications, including AWS Certified Solutions Architect, 
        EXIN Agile Scrum Master, and Clean Code & SOLID Principles. Fluent in French, Arabic, German, and English, 
        with excellent problem-solving and leadership skills.
        "
    """
    
    # Initialize the FormFiller with your OpenAI API key and user context
    form_filler = FormFiller()
    form_filler.set_user_context(context)

    qs1 = "What is your level of proficiency in German? options: Select an option, None, Conversational, Professional, Native or bilingual"
    qs2 = "How many years do you have in hardware manufacturing?"
    answers = form_filler.answer_question(qs1)
    for answer in answers:  
        print("Answer:", answers[0])

    qs2 = "How many years do you have in hardware manufacturing?"
    answers = form_filler.answer_question(qs2)
    for answer in answers:  
        print("Answer:", answers[0])