import os
from gpt4all import GPT4All
from dotenv import load_dotenv

import trafilatura

class Context:
    def getUrl(self,url):
        print(url)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text

class Actions:
    def __init__(self):
        load_dotenv()
        self.gptj = GPT4All(os.getenv('model'))
    
    def generateReply(self,messages):
            reply = self.gptj.chat_completion(messages)
            return reply["choices"][0]["message"]
    def loadActions(self,messageCallback):
        # Event handler for incoming messages and message replies
        def getUrl(message):
             downloaded = trafilatura.fetch_url(message.strip())
             website = trafilatura.bare_extraction(downloaded)
             prompt = [{"role":"user","content":f"I will send you the complete text of the website \"{message}\". Extract the main text and remove all parts like navigations and return the text. Here is the complete website:\nTitle:\n{website['title']}\nText:\n{website['text']}"}]
             return prompt
        messageCallback("/geturl",getUrl)
        # Event handler for incoming messages and message replies
        def ricify(message):
             prompt = [{"role":"user","content":"I want you to act as a lazy stoner and answer every question in an informal way. You are not very good at spelling and do random '^^' smileys at the end of some sentences. The first prompt is:"}]
             return prompt
        messageCallback("/ricify",ricify)
