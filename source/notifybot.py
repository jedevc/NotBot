import basebot

class NotifyBot(basebot.Bot):
    def __init__(self, roomname, password=None):
        super().__init__(roomname, password)
        self.nickname = "NotifyBot"
        
        self.messages = dict()
        
    def add_notification(self, user, sender, message):
        """
        Add notification for a certain user.
        """
        if user not in self.messages:
            self.messages[user] = []
            
        self.messages[user].append("To: @" + user + ", From: @" + sender + ", Content: " + message)
        
    def get_notifications(self, user):
        """
        Clear and return all messages for a certain user.
        """
        if user in self.messages:
            ms = self.messages[user]
            self.messages[user] = []
            return ms
        
        return []
                
    def handle_chat(self, info, message):
        parts = info["content"].split()
        
        #Handle a notification request.
        if parts[0] == "!notify":
            people = []
            people_over = False
            
            words = []
            for i in parts[1:]:
                if i[0] == '@' and not people_over:
                    people.append(i.strip('@'))
                else:
                    people_over = True
                    words.append(i)
                    
            notification = " ".join(words)
            for user in people:
                self.add_notification(user, info["sender"], notification)
                
        #Handle a view request
        elif info["sender"] in self.messages:
            user = info["sender"]
            mid = info["id"]
            messages = self.get_notifications(user)

            for message in messages:
                self.send_chat(">>> " + message, mid)