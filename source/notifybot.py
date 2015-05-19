import euphoria

import time
import unicodedata

def filter_nick(name):
    """
    filter_nick(name) -> String
    
    Process the name and get rid of all whitespace, invisible characters and
    make it all lower case.
    """
    
    ret = "".join(c for c in name if unicodedata.category(c)[0] not in ["C", "Z"])
    
    ret = "".join(ret.split())
    ret = ret.lower()
    
    return ret

def extract_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    
    return "%dh %dm %ds" % (h, m, s)

class NotifyBot(euphoria.chat_component.ChatComponent):
    def __init__(self, owner):
        super().__init__(owner)

        self.messages = dict()
        
    def add_notification(self, user, sender, message, timestamp):
        """
        add_notification(user, sender, message, timestamp) -> None
        
        Add notification for a certain user.
        """
        
        if user not in self.messages:
            self.messages[user] = []

        self.messages[user].append((sender, message, timestamp))
        
    def get_notifications(self, user):
        """
        get_notifications(user) -> None
        
        Clear and return all messages for a certain user.
        """
        
        if user in self.messages:
            ms = self.messages[user]
            self.messages[user] = []
            return ms
        
        return []
    
    def send_notifications(self, user, info):
        """
        send_notifications(user, info) -> None
        
        Send all the messages queued by the bot.
        """
        
        messages = self.get_notifications(user)

        for message in messages:
            user, content, timestamp = message
            tosend = "[" + user + ", " + extract_time(int(time.time()) - 
                        timestamp) + " ago] " + content
            self.send_chat(tosend, info["id"])
                
    def parse_notify(self, info, parts):
        """
        parse_notify(info, parts) -> None
        
        Take the text and try to send it to the specified user.
        """
        
        #Divide the people and the message into two parts.
        receiver = parts[1]
        notification = " ".join(parts[2:])
        
        #No receiver or no message
        if receiver[0] != "@" or len(notification) == 0:
            return
        
        #Send the message to the receiver
        to = receiver[1:]
        to = filter_nick(to)
        self.add_notification(to, info["sender"]["name"], notification, 
                                int(info["time"]))
        self.send_chat("Message will be delivered to %s." % receiver, 
                        info["id"])

    def handle_chat(self, info):
        #Handle sending messages if the user speaks
        user = filter_nick(info["sender"]["name"])
        if user in self.messages:
            self.send_notifications(user, info)
        
        #Now, begin proccessing the message
        #Split the message into parts and work out the command
        parts = info["content"].split()
        if len(parts) == 0:
            return
        command = parts[0]
        
        #Handle ping
        if command == "!ping":
            self.send_chat("Pong!", info["id"])
            
        #Handle help
        if command == "!help" and self.owner.nickname in info["content"]:
            self.send_chat("Use !notify to send messages to other people who "
                            "are currently unavailable.", info["id"])
        
        #Handle a notification request.
        elif command == "!notify":
            self.parse_notify(info, parts)