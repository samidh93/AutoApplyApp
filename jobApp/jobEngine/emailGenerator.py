from chatgpt import ChatGPT
import json

class emailCompanyGenerator:
    def __init__(self, company, location):
        query = f"what is the career or recruiting email of the company {company} located in {location}. \
        respond in json fromat 'email':'value' if you don't know, try to guess it. i am sure you can\n"
        reply = ChatGPT("jobApp/secrets/openai.json").ask(query)
        print(f"chatgpt replied: {reply}")
        email = json.loads(reply)
        return email["email"]
    
if __name__ == '__main__':
    print(emailCompanyGenerator("luxoft", "germany"))