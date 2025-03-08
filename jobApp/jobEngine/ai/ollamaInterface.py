import ollama
import os
import json
import yaml
from pathlib import Path
import ast
import logging

logger = logging.getLogger(__name__)

class FormFiller:
    def __init__(self):
        # Load secrets (not needed for Ollama, but kept for compatibility)
        secrets_path = Path('input/secrets.yaml')
        secrets = yaml.safe_load(open(secrets_path, 'r'))
        self.model = "mistral:latest"  # Ollama model
    
    def set_user_context(self, user_context):
        self.conversation_history = [
            {
                "role": "system",
                "content": (
                    "You are an AI assistant helping to fill out a job application form.\n\n"
                    "STRICT RULES:\n"
                    "- Return ONLY the answer as a Python list of strings.\n"
                    "Example Question: What is your level of proficiency in English? Options are Native, Professional, Conversational, None.\n"
                    "Example Response: ['Professional']\n"
                    "- DO NOT include explanations, reasoning, or any additional text.\n"
                    "- If a question provides options, return one of the given options exactly as written.\n"
                    "- If you don't have enough information, return your best guess based on context.\n"
                    f"{user_context}"
                )
            }
        ]


    def answer_question(self, question) -> list:
        """Return a list of answers for one or multiple questions in the same order."""
        self.conversation_history.append({"role": "user", "content": question})
        
        response = ollama.chat(
            model=self.model,
            messages=self.conversation_history,
            #temperature=0.7
        )
        # remove the question from history
        self.conversation_history.pop()
        answer = response['message']['content'].strip()
        answer = ast.literal_eval(answer)
        
        # Validate the answer if the question contains options
        if "options:" in question.lower():
            options_part = question.split("options:")[-1].strip()
            choices = [opt.strip() for opt in options_part.split(",")]
            
            # Check if the answer is in the list
            if answer[0] not in choices:
                logger.warning(f"Invalid response '{answer[0]}'. Selecting closest valid option.")
                answer[0] = next((opt for opt in choices if opt.lower() in answer[0].lower()), choices[0])
        
        return answer

# Example usage
if __name__ == "__main__":
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
    """
    
    form_filler = FormFiller()
    form_filler.set_user_context(context)

    qs1 = "What is your level of proficiency in German? options: Select an option, None, Conversational, Professional, Native or bilingual"
    answers = form_filler.answer_question(qs1)
    for answer in answers:  
        print("Answer:", answer)
    
    qs2 = "How many years do you have in hardware manufacturing?"
    answers = form_filler.answer_question(qs2)
    for answer in answers:  
        print("Answer:", answer)
