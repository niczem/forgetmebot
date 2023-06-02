import os
from gpt4all import GPT4All
from dotenv import load_dotenv

class Actions:
    def __init__(self):
        load_dotenv()
        self.gptj = GPT4All(os.getenv('model'))
    def generateReply(self,messages):
            reply = self.gptj.chat_completion(messages)
            return reply["choices"][0]["message"]

    def loadActions(self,messageCallback):
        # Event handler for incoming messages and message replies
        ricify = [{"role":"user","content":"I want you to act as a lazy stoner and answer every question in an informal way. You are not very good at spelling and do random '^^' smileys at the end of some sentences. The first prompt is:"}]
        messageCallback("/ricify",ricify)
