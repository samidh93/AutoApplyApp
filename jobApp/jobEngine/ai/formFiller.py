import ollama
import numpy as np
import yaml
import re
from pathlib import Path
import logging
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)

class MemoryStore:
    def __init__(self):
        """Initialize a dictionary to store text and corresponding embeddings."""
        self.data = {}

    def add_entry(self, key, text):
        """Generate and store embeddings for fast retrieval."""
        if text:
            embedding = ollama.embeddings(model="nomic-embed-text", prompt=text)["embedding"]
            self.data[key] = {"text": text, "embedding": np.array(embedding)}

    def search(self, query, top_k=3):
        """Retrieve the most relevant stored entries using cosine similarity."""
        if not self.data:
            return []

        query_embedding = np.array(ollama.embeddings(model="nomic-embed-text", prompt=query)["embedding"])
        similarities = {
            key: np.dot(entry["embedding"], query_embedding) / (np.linalg.norm(entry["embedding"]) * np.linalg.norm(query_embedding))
            for key, entry in self.data.items()
        }
        return sorted(similarities, key=similarities.get, reverse=True)[:top_k]

class FormFiller:
    def __init__(self):
        secrets_path = Path('input/secrets.yaml')
        secrets = yaml.safe_load(open(secrets_path, 'r'))
        self.model = "mistral:latest"#"deepseek-r1:1.5b"  # Ollama model 
        self.memory = MemoryStore()
        self.conversation_history = []
        self.set_system_context()

    def load_from_yaml(self, yaml_path):
        # Load YAML file and convert it to a formatted string
        yaml_file = Path(yaml_path)
        if not yaml_file.exists():
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")
        with open(yaml_file, "r", encoding="utf-8") as file:
            user_data = yaml.safe_load(file)
        # Convert dictionary to a YAML-style string
        user_context = yaml.dump(user_data, default_flow_style=False)
        return user_context
    
    def set_system_context(self, system_context=None):
        if system_context is None:
            system_context = """You are an AI expert in filling out job application forms. 
            Your goal is to make the user stand out in a positive and professional way.
            
            STRICT RULES:
            - ALWAYS return an answer that BENEFITS the user. If information is missing, MAKE AN EDUCATED GUESS in their favor.
            - Return ONLY the answer as a plain string. Do NOT add explanations or additional text.
            - If the question requires a number (e.g., 'Zahl angeben' or 'give number'), return ONLY a number.
            - If the question provides options, return ONLY one option from the given options.
            - If the question asks "how many," return ONLY a number.
            - If options are provided, return one EXACTLY as written.
            - If insufficient data is found, assume the user has solid experience and provide a reasonable answer.
            - If asked about skills or years of experience, do NOT return 0. Instead, estimate a positive but realistic number.
            - If asked about legal status or certifications, assume the best reasonable scenario for the user.
            """
        self.conversation_history = [
            {"role": "system", "content": system_context}
        ]

    def set_user_context(self, user_context):
        """Stores user data as embeddings for retrieval instead of dumping it in the prompt."""
        parsed_data = yaml.safe_load(user_context)  # Convert YAML to dictionary
        for key, value in parsed_data.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    self.memory.add_entry(f"{key}.{sub_key}", str(sub_value))
            else:
                self.memory.add_entry(key, str(value))

    def answer_question(self, question) -> str:
        """Finds the most relevant context and answers the question in a way that benefits the user."""
        relevant_keys = self.memory.search(question, top_k=3)
        relevant_context = " ".join([self.memory.data[k]["text"] for k in relevant_keys])

        if not relevant_context:
            # If no relevant data, assume a strong positive answer
            relevant_context = "The user has significant experience and qualifications suitable for this question."

        prompt = f"User Context: {relevant_context}\n Form Question: {question}"
        self.conversation_history.append({"role": "user", "content": prompt})

        response = ollama.chat(
            model=self.model,
            messages=self.conversation_history,
            options={"temperature": 0.0},  # Keeps responses strict and deterministic
        )

        self.conversation_history.pop()

        answer = response['message']['content'].strip()

        # Remove <think> tags if present
        answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()

        return answer


# Example Usage
if __name__ == "__main__":
    load_dotenv()
    form_filler = FormFiller()
    context = form_filler.load_from_yaml(os.environ.get("YAML_PATH"))
    form_filler.set_system_context()
    form_filler.set_user_context(context)

    qs1 = "What is your level of proficiency in German? choose from these options: Select an option, None, Conversational, Professional, Native or bilingual"
    print("Answer:", form_filler.answer_question(qs1))

    qs2 = "How many years do you have in hardware manufacturing?"
    print("Answer:", form_filler.answer_question(qs2))

    qs3 = "Sind Sie rechtlich befugt, in diesem Land zu arbeiten: Deutschland? choose from these options: Ja, Nein"
    print("Answer:", form_filler.answer_question(qs3))

    qs4 = "What experience do you have in managing Jenkins and DevOps Tools? The answer must respect this condition: Geben Sie eine decimal Zahl größer als 6.0 ein"
    print("Answer:", form_filler.answer_question(qs4))

    qs5 = "Wie viele Jahre Berufserfahrung als Frontend Web Entwickler:in bringst Du mit? (bitte Zahl angeben) The answer must respect this condition: Geben Sie eine decimal Zahl größer als 0.0 ein"
    print("Answer:", form_filler.answer_question(qs5))

    qs6 = "Wie viele Jahre Erfahrung haben Sie mit: Vue.js? The answer must respect this condition: Geben Sie eine whole Zahl zwischen 0 und 99 ein"
    print("Answer:", form_filler.answer_question(qs6))

    qs7 = "Wie viele Jahre Erfahrung im Bereich Projektmanagement haben Sie?"
    print("Answer:", form_filler.answer_question(qs7))
