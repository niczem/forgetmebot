import json
import os
session_path = os.path.join(os.path.dirname(__file__), '../../../data/sessions/')
class Sessions:
    def __init__(self):
        self.sessions = {}
        print("session class inited")
    def writeSession(self,session_id,session):
        json_object = json.dumps(session)
        with open(session_path+str(session_id)+".json", "w") as outfile:
            outfile.write(json_object)
    def getSession(self,session_id):
        try:
            f = open(session_path+str(session_id)+".json")
        except:
            print("could not open session")
        
        data = json.load(f)
        return data
    def createSession(self,session_id,message):
        messages = [{"role": "user", "content": message}]
        self.writeSession(session_id,{"messages":messages})
    def addMessageToSession(self,session_id, message, role="user"):
        session = self.getSession(session_id)
        if session:
            session['messages'].append({"role":role,"content":str(message)})
            self.writeSession(session_id,session)
        else:
            print("can not open session",session_id,self.sessions)
    def updateSessionIndex(self, old_index, new_index):
        print("updateSessionIndex", old_index, new_index)
        try:
            session = self.getSession(old_index)
            self.writeSession(new_index,session)
        except:
            print("update session")
        #by not deleting the old session, it is also possible to reply to all messages in the history
    def getSessionOld(self, session_id):
        if session_id in self.sessions:
            return self.sessions[session_id]
        else:
            print("can not open session",session_id,self.sessions)
