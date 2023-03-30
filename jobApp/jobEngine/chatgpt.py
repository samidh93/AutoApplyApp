import openai
import json
import os


class ChatGPT:
    def __init__(self, token_file):
        # Load the JSON file containing the API token
        self.cwd = os.getcwd()
        self.token_path = os.path.join(self.cwd, token_file)
        # Construct the path to the token.json file relative to the current working directory
        # Check if the file exists
        if os.path.exists(self.token_path):
            print("openai.json found at:", self.token_path)
        else:
            print("openai.json not found at:", self.token_path)
        with open(self.token_path) as f:
            data = json.load(f)
        # Extract the API token from the JSON data
        token = data['token']
        openai.api_key = token
        self.conversation = ()

    def ask(self, question):
        message_history = [{"role": "user", "content": f"{question}"}]
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=message_history)
        reply_content = completion.choices[0].message.content
        message_history.append(
            {"role": "assistant", "content": f"{reply_content}"})
        self.conversation += (message_history[0]
                              ["content"], message_history[1]["content"])
        return reply_content

    def printConversationHistory(self):
        for i, msg in enumerate(self.conversation):
            if i % 2 != 0:
                print(
                    f"                                                {msg} ")
            else:
                print(f"{msg} ")


if __name__ == '__main__':
    chatgpt = ChatGPT("secrets/openai.json")
    q1 = "create a draft email to the hiring manager for my job application as project manager at IPSET"
    q2 =" create a draft email for software engineer job application at bosch  \
        Experience:  \
        Lead robotics & software engineer theion Jun 2021 - Present (1 year 10 months) \
        Project: software solution design of several custom Machines for sulfur battery production. \
        Team size: 5 Tech-stack: C++, python, Qt, uml, ros, git, github actions, docker, cmake, sql, agile scrum \
        Software Engineer German Aerospace Center (DLR) Apr 2020 - Jun 2021 (1 year 3 months) \
        Project: development of autonomus driving simulation testing framework \
        Team size: 9 Tech-stack: c++, python, ros, git, gitlab ci, docker, sumo, yaml, json, cmake, agile scrum \
        Working Student embedded software Berlin University of Applied Sciences Berlin (BHT) \
        Apr 2019 - Apr 2020 (1 year 1 month) Project: design of customized stereolithography 3d printer \
        Team size: 4 Tech-stack: c, c++, stm32, cubemx, simulink \
        "
    q3 = "create a draft email to apply for the job as recruiting manager at BIC in paris, france"
    # Example usage of the ask() function
    chatgpt.ask(q1)
    chatgpt.ask(q2)
    chatgpt.ask(q3)
    chatgpt.printConversationHistory()
