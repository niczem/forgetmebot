class Sessions:
    def __init__(self):
        self.sessions = {}
        print("session class inited")
    def createSession(self,message_id,message):
        messages = [{"role": "user", "content": message}]
        self.sessions[message_id] = {"messages":messages}
    def addMessageToSession(self,session_id, message, role="user"):
        print("addMessageToSession",session_id, message, role)
        if session_id in self.sessions:
            self.sessions[session_id]['messages'].append({"role":role,"content":str(message)})
        else:
            print("can not open session",session_id,self.sessions)
    def updateSessionIndex(self, old_index, new_index):
        print("updateSessionIndex", old_index, new_index)
        if old_index == new_index:
            return
        if old_index in self.sessions:
            self.sessions[new_index] = self.sessions[old_index]
            del self.sessions[old_index]
        else:
            if new_index in self.sessions:
                print("old_session id does not exist, but new does exist. do nothing")
            else: 
                raise Exception("can not open session", old_index, new_index ,self.sessions)
    def getSession(self, session_id):
        if session_id in self.sessions:
            return self.sessions[session_id]
        else:
            print("can not open session",session_id,self.sessions)
