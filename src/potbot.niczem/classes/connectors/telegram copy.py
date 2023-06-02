from ast import List
import os
from classes.actions.actions import Actions
from dotenv import load_dotenv
from telethon.sync import TelegramClient, events
actions = Actions()

class Connector:
    def __init__(self):
        self.sessions = {}
        print("class inited")
    def run(self):
        load_dotenv()

        # Telegram API credentials
        api_id = os.getenv('api_id')
        api_hash = os.getenv('api_hash')
        bot_token = os.getenv('bot_token')

        # Create a Telegram client
        client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)


        def createSession(message_id,message):
            messages = [{"role": "user", "content": message}]
            self.sessions[message_id] = {"messages":messages}

        def addMessageToSession(session_id, message, role="user"):

            if self.sessions[session_id]:
                self.sessions[session_id]['messages'].append({"role":role,"content":str(message)})
            else:
                print("can not open session when adding message")

            print(self.sessions)

        def messageCallback(pattern: List,prompts):
            # Event handler for incoming messages and message replies
            @client.on(events.NewMessage(pattern=pattern))  # Custom command to start the bot
            async def start(event):
                prompts.append({"role":"user","content":str(event.message.message.replace(pattern,''))})
                print("prompts")
                print(prompts)
                reply = actions.generateReply(prompts)
                print("reply")
                print(reply)
                createSession(event.message.id,prompts)
                addMessageToSession(event.message.id, reply['content'], "assistant")
                await event.respond(reply['content'])

        actions.loadActions(messageCallback)

        @client.on(events.NewMessage)
        async def handle_message(event):
                

            if event.is_private:
                print("private")
                sender = await event.get_sender()
                message = event.message.message

                if event.message.message.startswith('/'):
                    print('ignore system message')
                else:
                    # Check if the message is a reply
                    if event.is_reply:
                        replied_msg = await event.get_reply_message()
                        print(event.message)
                        print(replied_msg)
                        if replied_msg.reply_to:
                            old_message_id = replied_msg.reply_to.reply_to_msg_id
                        else:
                            old_message_id = event.message.id

                        new_message_id = event.message.id
                        print("old, new")
                        print(old_message_id, new_message_id)
                        #move session to new id, easier than looping ab the replies
                        if new_message_id != old_message_id:
                            self.sessions[new_message_id] = self.sessions[old_message_id]
                            del self.sessions[old_message_id]
                        addMessageToSession(new_message_id, message)
                        new_message = actions.generateReply(self.sessions[new_message_id]['messages'])

                        
                        addMessageToSession(new_message_id, new_message['content'], "assistant")
                        reply = str(new_message['content'])
                        
                    else:
                        createSession(event.message.id,message)
                        reply = actions.generateReply(self.sessions[event.message.id]['messages'])
                        print("reply")
                        print(reply)

                        addMessageToSession(event.message.id, reply['content'], "assistant")
                        reply = reply["content"]
                        #reply = gptj.chat_completion(sessions[event.message.id])

                    # Reply to the message
                    print("reply")
                    print(reply)
                    await event.reply(reply)
            else:
                print("not private")
        # Start the bot
        client.run_until_disconnected()