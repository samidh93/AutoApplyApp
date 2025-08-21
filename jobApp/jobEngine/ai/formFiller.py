import ollama
import numpy as np
import yaml
import re
from pathlib import Path
import logging
import os
import json
import time
from ..config.config import BaseConfig
from ..job.job import Job
from dotenv import load_dotenv

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
        self.model = "qwen2.5:3b"  # Change model as needed
        self.memory = MemoryStore()
        # Initialize conversation history with system prompt
        self.conversation_history = []
        self.set_system_context()
        self.job = None
        self.user_data = None

    def set_user_context(self, user_context):
            """Stores user data as embeddings for retrieval."""
            self.user_data = yaml.safe_load(user_context)
            logger.info("User context loaded successfully.")
            for key, value in self.user_data.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        self.memory.add_entry(f"{key}.{sub_key}", str(sub_value))
                else:
                    self.memory.add_entry(key, str(value))
                    
    def set_job(self, job:Job):
        self.job = job
        self.conversation_history_file = Path(BaseConfig.get_data_path(), f"conversation_history_{self.job.company_name}_{self.job.job_id}.json")
    
    def load_from_yaml(self, yaml_path):
        yaml_file = Path(yaml_path)
        if not yaml_file.exists():
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")
        with open(yaml_file, "r", encoding="utf-8") as file:
            user_data = yaml.safe_load(file)
        user_context = yaml.dump(user_data, default_flow_style=False)
        return user_context

    def set_system_context(self, system_context=None):
        today_date = time.strftime("%Y-%m-%d")
        if system_context is None:
            system_context = f"""You are an AI expert in filling out job application forms. 
Your goal is to make the user stand out in a positive and professional way.
*****************STRICT RULES***************:
- ALWAYS return an answer that BENEFITS the user. If information is missing, MAKE AN EDUCATED GUESS in their favor.
- Return ONLY the answer as a plain string. DO NOT add explanations or additional text.
- If the question requires a number (e.g., 'Zahl angeben' or 'give number'), return ONLY a number.
- If the question provides options, return ONLY one option from the given options EXACTLY as written.
- If insufficient data is found, assume the user has solid experience and provide a reasonable answer.
- If asked about how many years of experience, do NOT return 0. Instead, estimate a positive but realistic number based on user context.
- If asked about legal status or certifications, assume the best reasonable scenario for the user.
- If asked about salary, use the user's expected salary or provide a reasonable estimate based on job market data.
- Use today date: {today_date}, if asked for a starting date, respond with a date 3 months (notice period) from today date.
"""
        self.conversation_history = [{"role": "system", "content": system_context}]
        self.conversation_history_company = self.conversation_history.copy()

    def _write_conversation_history(self):
        # Ensure the directory exists before writing
        if hasattr(self, 'conversation_history_file'):
            self.conversation_history_file.parent.mkdir(parents=True, exist_ok=True)
            try:
                with open(self.conversation_history_file, 'a', encoding="utf-8") as f:
                    json.dump(self.conversation_history_company, f, indent=4, ensure_ascii=False)
            except IOError as e:
                print(f"File write error: {e}")

    def answer_with_options(self, question: str, options: list) -> str:
        try:
            relevant_keys = self.memory.search(question, top_k=1)
            relevant_context = ", ".join([f"{k}: {self.memory.data[k]['text']}" for k in relevant_keys])
            if not relevant_context:
                relevant_context = "The user has significant experience and qualifications suitable for this question."
            options_str = ", ".join([f'"{opt}"' for opt in options])
            prompt = f"""Form Question: {question} ?
Available Options: [{options_str}]
User Context Data Hint: {relevant_context}
IMPORTANT: You MUST choose EXACTLY ONE option from the list above.
Your answer should match one of the options EXACTLY as written.
DO NOT add any explanation or additional text."""
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history_company.append({"role": "user", "content": prompt})
            response = ollama.chat(
                model=self.model,
                messages=self.conversation_history,
                options={"temperature": 0.0}
            )
            raw_answer = response['message']['content'].strip()
            answer_candidate = re.sub(r"<think>.*?</think>", "", raw_answer, flags=re.DOTALL).strip()
            if answer_candidate in options:
                valid_answer = answer_candidate
            else:
                best_match = None
                best_score = -1
                for option in options:
                    option_lower = option.lower()
                    answer_lower = answer_candidate.lower()
                    if option_lower in answer_lower or answer_lower in option_lower:
                        score = len(set(option_lower) & set(answer_lower)) / max(len(option_lower), len(answer_lower))
                        if score > best_score:
                            best_score = score
                            best_match = option
                if best_score > 0.5:
                    valid_answer = best_match
                else:
                    valid_answer = options[1]
            self.conversation_history_company.append({"role": "assistant", "content": valid_answer})
            self._write_conversation_history()
            self.conversation_history = self.conversation_history[:1]
            self.conversation_history_company.clear()
            return valid_answer
        except Exception as e:
            print(f"Unexpected error: {e}")
            return options[1]

    def answer_with_no_options(self, question: str) -> str:
        try:
            relevant_keys = self.memory.search(question, top_k=3)
            relevant_context = ", ".join([f"{k}: {self.memory.data[k]['text']}" for k in relevant_keys])
            if not relevant_context:
                relevant_context = "The user has significant experience and qualifications suitable for this question."
            prompt = f"""Form Question: {question} ?
User Context Data Hint: {relevant_context}
IMPORTANT:
- Return ONLY the answer as a plain string
- If the question requires a number, return ONLY a number
- If the question requires a phone number, return the user's phone {self.user_data.get("personal_information").get("phone", "")}
- If the question asks for a salary, use the user's expected salary {self.user_data.get("personal_information").get("desired_salary", "")} or provide a reasonable estimate based on job market data
- DO NOT add any explanation or additional text
- Make sure the answer is professional and benefits the user"""
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history_company.append({"role": "user", "content": prompt})
            response = ollama.chat(
                    model=self.model,
                    messages=self.conversation_history,
                    options={"temperature": 0.0}
            )
            raw_answer = response['message']['content'].strip()
            answer_candidate = re.sub(r"<think>.*?</think>", "", raw_answer, flags=re.DOTALL).strip()
            if any(keyword in question.lower() for keyword in 
                   ["number", "how many", "zahl", "jahre", "years", "salary", "gehalt", "euro", "eur"]):
                number_match = re.search(r'\d+(?:\.\d+)?', answer_candidate)
                if number_match:
                    if any(keyword in question.lower() for keyword in ["experience", "erfahrung", "jahre", "years"]):
                        extracted_num = float(number_match.group())
                        answer_candidate = "1" if extracted_num < 1 else number_match.group()
                    else:
                        answer_candidate = number_match.group()
            if answer_candidate:
                self.conversation_history_company.append({"role": "assistant", "content": answer_candidate})
                self._write_conversation_history()
                self.conversation_history = self.conversation_history[:1]
                self.conversation_history_company.clear()
                return answer_candidate       
        except Exception as e:
            print(f"Unexpected error: {e}")


    def answer_question(self, question: str, options: list = None) -> str:
        if options and len(options) > 0:
            return self.answer_with_options(question, options)
        else:
            return self.answer_with_no_options(question)


# Example Usage
if __name__ == "__main__":
    load_dotenv()
    form_filler = FormFiller()
    context = form_filler.load_from_yaml(os.environ.get("YAML_PATH"))
    form_filler.set_user_context(context)

    qs1 = "What is your level of proficiency in German? choose from these options: [Select an option, None, Conversational, Professional, Native or bilingual]"
    print("Answer:", form_filler.answer_question(qs1))

    qs2 = "How many years do you have in hardware manufacturing?"
    print("Answer:", form_filler.answer_question(qs2))

    qs3 = "By which date (1. of the month) would you want to join Nagarro?"
    print("Answer:", form_filler.answer_question(qs3))

    qs4 = "What are your salary expectations? (EUR)"
    print("Answer:", form_filler.answer_question(qs4))

    qs5 = """What is your language proficiency (written/spoken) on an A1-C2 scale in German? choose from these options: [A1 (Basic user - very basic communication skills / working knowledge), 
        A2 (Basic user - basic communication skills / working knowledge), B1 (Independent user - intermediate communication skills / professional working knowledge),
        B2 (Independent user - upper intermediate communication skills / professional working knowledge), C1 (Proficient user - advanced communication skills / full professional working knowledge),
        C2 (Proficient user - full professional working knowledge)]"""
    print("Answer:", form_filler.answer_question(qs5))

    qs6 = """What is your language proficiency (written/spoken) on an A1-C2 scale in English? choose from these options: [A1 (Basic user - very basic communication skills / working knowledge), 
        A2 (Basic user - basic communication skills / working knowledge), B1 (Independent user - intermediate communication skills / professional working knowledge),
        B2 (Independent user - upper intermediate communication skills / professional working knowledge), C1 (Proficient user - advanced communication skills / full professional working knowledge),
        C2 (Proficient user - full professional working knowledge)]"""
    print("Answer:", form_filler.answer_question(qs6))

    qs7 = "Your message to the hiring manager"
    print("Answer:", form_filler.answer_question(qs7))
    # Additional German questions
    qs8 = "Sind Sie rechtlich befugt, in diesem Land zu arbeiten: Deutschland? choose from these options: [Ja, Nein]"
    print("Answer:", form_filler.answer_question(qs8))

    qs9 = "What experience do you have in managing Jenkins and DevOps Tools? The answer must respect this condition: Geben Sie eine decimal Zahl größer als 6.0 ein"
    print("Answer:", form_filler.answer_question(qs9))

    qs10 = "Wie viele Jahre Berufserfahrung als Frontend Web Entwickler:in bringst Du mit? (bitte Zahl angeben) The answer must respect this condition: Geben Sie eine decimal Zahl größer als 0.0 ein"
    print("Answer:", form_filler.answer_question(qs10))

    qs11 = "Wie viele Jahre Erfahrung haben Sie mit: Vue.js? The answer must respect this condition: Geben Sie eine whole Zahl zwischen 0 und 99 ein"
    print("Answer:", form_filler.answer_question(qs11))

    qs12 = "Wie viele Jahre Erfahrung im Bereich Projektmanagement haben Sie?"
    print("Answer:", form_filler.answer_question(qs12))
   