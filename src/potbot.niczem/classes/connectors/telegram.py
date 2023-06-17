from ast import And, List
import os
from classes.actions.actions import Actions
from classes.sessions import Sessions
from dotenv import load_dotenv
from telethon.sync import TelegramClient, events
actions = Actions()
class Connector:
    def __init__(self):
        self.sessions = Sessions()
        print("connector class inited")
    def run(self):
        load_dotenv()

        # Telegram API credentials
        api_id = os.getenv('api_id')
        api_hash = os.getenv('api_hash')
        bot_token = os.getenv('bot_token')

        # Create a Telegram client
        client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

        def messageCallback(pattern: List,callback):
            # Event handler for incoming messages and message replies
            @client.on(events.NewMessage(pattern=pattern))  # Custom command to start the bot
            async def start(event):
                input_message = str(event.message.message.replace(pattern,''))
                prompts = callback(input_message)
                prompts.append({"role":"user","content":input_message})
                self.sessions.createSession(event.message.id,str(event.message.message.replace(pattern,'')))
                reply = actions.generateReply(prompts)
                self.sessions.addMessageToSession(event.message.id, reply['content'], "assistant")
                response = await event.respond(reply['content'])
                self.sessions.updateSessionIndex(event.message.id,response.id)
        actions.loadActions(messageCallback)
        @client.on(events.NewMessage)
        async def handle_message(event):
            if event.is_private:
                sender = await event.get_sender()
                message = event.message.message

                if event.message.message.startswith('/'):
                    if event.is_reply:
                        replied_msg = await event.get_reply_message()

                else:
                    # Check if the message is a reply
                    if event.is_reply:
                        replied_msg = await event.get_reply_message()

                        if replied_msg.reply_to:
                            old_message_id = replied_msg.reply_to.reply_to_msg_id
                        else:
                            old_message_id = event.message.id

                        new_message_id = replied_msg.id
                        old_message_id = replied_msg.id
                        
                        if old_message_id == new_message_id:
                            if replied_msg.reply_to:
                                old_message_id = replied_msg.reply_to.reply_to_msg_id
                        try:
                            self.sessions.updateSessionIndex(old_message_id,new_message_id)
                        except:
                            self.sessions.updateSessionIndex(replied_msg.reply_to.reply_to_msg_id,new_message_id)

                        try:
                            self.sessions.addMessageToSession(new_message_id, message)
                        except:
                            self.sessions.addMessageToSession(replied_msg.reply_to.reply_to_msg_id, message)

                        

                        new_message = actions.generateReply(self.sessions.getSession(new_message_id)['messages'])

                        self.sessions.addMessageToSession(new_message_id, new_message['content'], "assistant")
                        reply = str(new_message['content'])
                        
                    else:
                        self.sessions.createSession(event.message.id,message)
                        reply = actions.generateReply(self.sessions.getSession(event.message.id)['messages'])
                        self.sessions.addMessageToSession(event.message.id, reply['content'], "assistant")
                        reply = reply["content"]
                        #reply = gptj.chat_completion(sessions[event.message.id])

                    # Reply to the message
                    replyObj = await event.reply(reply)
                    if replyObj.id and 'new_message_id' in locals():
                        self.sessions.updateSessionIndex(new_message_id,replyObj.id)

        # Start the bot
        client.run_until_disconnected()