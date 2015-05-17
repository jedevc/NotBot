import euphoria

import time
import string

def filter_nick(name):
    """
    filter_nick(name) -> String
    
    Process the name and get rid of all whitespace, invisible characters and
    make it all lower case.
    """
    
    ret = "".join(name.split())
    ret = "".join([x for x in ret if x in string.printable])
    ret = ret.lower()
    
    return ret

class NotifyBot(euphoria.chat_component.ChatComponent):
    def __init__(self, owner):
        super().__init__(owner)

        self.messages = dict()
        
    def add_notification(self, user, sender, message, timestamp):
        """
        Add notification for a certain user.
        """
        
        if user not in self.messages:
            self.messages[user] = []

        self.messages[user].append((sender, message, timestamp))
        
    def get_notifications(self, user):
        """
        Clear and return all messages for a certain user.
        """
        
        if user in self.messages:
            ms = self.messages[user]
            self.messages[user] = []
            return ms
        
        return []
                
    def handle_chat(self, info):
        #Handle sending messages if the user speaks
        sender = filter_nick(info["sender"]["name"])
        if sender in self.messages:
            messages = self.get_notifications(sender)

            for message in messages:
                sender, content, timestamp = message
                tosend = "[" + sender + ", " + str(int(time.time()) - 
                                        timestamp) + " seconds ago] " + content
                self.send_chat(tosend, info["id"])
        
        #Split the message into parts
        parts = info["content"].split()
        if len(parts) == 0:
            return
        
        #Handle ping
        if parts[0] == "!ping":
            self.send_chat("Pong!", info["id"])
        
        #Handle a notification request.
        elif parts[0] == "!notify":
            people = []
            people_over = False
            
            #Divide the people and the message into two parts.
            words = []
            for i in parts[1:]:
                if i[0] == '@' and not people_over:
                    person = i.strip('@')
                    person = filter_nick(person)
                    people.append(person)
                else:
                    people_over = True
                    words.append(i)
                    
            if len(people) == 0: #Make sure that people will receive the message
                return
                    
            #Send the message to everyone
            notification = " ".join(words)
            notification = notification.strip()
            if len(notification) != 0:  #Make sure that the notification exists
                for user in people:
                    self.add_notification(user, info["sender"]["name"], 
                                            notification, int(info["time"]))
                
                self.send_chat("Message will be delivered to @" + 
                                " @".join(people) + ".", info["id"])