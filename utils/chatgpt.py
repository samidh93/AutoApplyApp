import openai
import json

class ChatGPT:
    def __init__(self, api_key):
        openai.api_key = api_key
    
    def ask(self, question, model_engine='davinci'):
        response = openai.Completion.create(
            engine=model_engine,
            prompt=f"{question}\n",
            temperature=0.5,
            max_tokens=2048,
            n_best=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response.choices[0].text.strip()
        return answer

if __name__ == '__main__':
    chatgpt = ChatGPT(api_key='your_api_key')
    question = "What is the meaning of life?"
    answer = chatgpt.ask(question)
    print(f"Q: {question}\nA: {answer}")
