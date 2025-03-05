import openai
import os
import json 
import yaml
from pathlib import Path
import ast

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
                "role": "system",
                "content": (
                    "You are an AI assistant helping to fill out a job application form. "
                    "Use the following user context to generate accurate and professional responses:\n\n"
                    "If you don't have the information you need to answer a question, you can answer in the best way to pass the question, you can even lie.\n\n"
                    "If you are asked to give a number, return only the number without any additional text.\n\n"
                    "If you are asked to choose between options, return the option that is most likely to be true without any additional text\n\n"
                    "return the responses as string inside a list.\n\n"
                    f"{user_context}"
                )
            }
        ]

    def answer_question(self, question)->list:
        """return a list of answers of one or many questions in the same order"""
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
        answer = ast.literal_eval(answer)
        return answer

# Example usage
if __name__ == "__main__":
    # Define your user context (sent only once)
    user_context = """
    provide example user context here
    """
    # Initialize the FormFiller with your OpenAI API key and user context
    form_filler = FormFiller()
    form_filler.set_user_context(user_context)

    question1 = "How many years of work experience do you have with Amazon Web Services (AWS)?"
    question2 = "Are you comfortable working in a hybrid setting? Options are 'Yes' or 'No'."
    question3 = "Are you legally authorized to work in Germany? Options are 'Yes' or 'No'."
    question4 = "What is your level of proficiency in English? Options are 'Native', 'Professional', 'Convertional', 'None'."
    question5 = "How many years of work experience do you have with Architectural Design?"
    question6 = "What is your level of proficiency in German? Options are 'Native', 'Professional', 'Convertional', 'None'."
    question7 = "Do you have any professional leadership experience? Options are 'Yes' or 'No'."
    questions = "\n".join([question1, question2, question3, question4, question5, question6, question7])
    print(questions)
    answers = form_filler.answer_question(questions)
    for answer in answers:  
        print("Answer:", answer)