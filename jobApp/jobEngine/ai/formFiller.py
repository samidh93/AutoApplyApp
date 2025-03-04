import openai
import os
import json 
import yaml
from pathlib import Path

class FormFiller:
    def __init__(self, api_key, user_context):
        # Set up the API key
        openai.api_key = api_key
        
        # Initialize conversation history with user context as a system message
        self.conversation_history = [
            {
                "role": "system",
                "content": (
                    "You are an AI assistant helping to fill out a job application form. "
                    "Use the following user context to generate accurate and professional responses:\n\n"
                    "If you don't have the information you need to answer a question, you can answer in the best way to pass the question, you can even lie.\n\n"
                    f"{user_context}"
                )
            }
        ]

    def answer_question(self, question):
        # Append the new question to the conversation history
        self.conversation_history.append({"role": "user", "content": question})
        
        # Call the OpenAI API using the correct method and model
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # Replace with your preferred model, e.g., "gpt-3.5-turbo"
            temperature=0.8,
            messages=self.conversation_history
        )
        
        # Extract and clean the answer from the response
        answer = response.choices[0].message.content.strip()
        
        # Append the assistant's answer to the history for context in future questions
        self.conversation_history.append({"role": "assistant", "content": answer})
        
        return answer

# Example usage
if __name__ == "__main__":
    # Define your user context (sent only once)
    user_context = """
    Name: John Doe
    Experience: 5 years as a Software Engineer
    Skills: Python, JavaScript, DevOps
    Certifications: AWS Certified Solutions Architect
    Languages: English (Fluent), German (Intermediate)
    """
    secrets_path = Path('input/secrets.yaml')
    secrets = yaml.safe_load(open(secrets_path, 'r'))
    api_key = secrets['api_key']
    # Initialize the FormFiller with your OpenAI API key and user context
    form_filler = FormFiller(api_key=api_key, user_context=user_context)
    # Ask a question and print the answer
    question1 = "How many years of experience do you have in engineering?"
    answer1 = form_filler.answer_question(question1)
    print("Q:", question1)
    print("A:", answer1)
    
    # Ask another question without resending the user context
    question2 = "Are you confident working with cloud technologies?"
    answer2 = form_filler.answer_question(question2)
    print("\nQ:", question2)
    print("A:", answer2)

    # Ask another question without resending the user context
    question2 = "are you confident coding in cpp?"
    answer2 = form_filler.answer_question(question2)
    print("\nQ:", question2)
    print("A:", answer2)

