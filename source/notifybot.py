import euphoria

import time
import unicodedata
import threading

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
    """
    extract_time(seconds) -> String
    
    Turn the time in seconds to a string containing the time formatted into
    hours and minutes.
    """
    
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    
    return "%dh %dm %ds" % (h, m, s)

class NotifyBot(euphoria.ping_room.PingRoom, euphoria.chat_room.ChatRoom):
    def __init__(self, dumpfile, delay, roomname, password=None):
        super().__init__(roomname, password)
        self.nickname = "NotBot"

        self.messages = dict()
        self.recover_messages(dumpfile)
        
        #Threading crap
        self.dump_thread = threading.Thread(target=self.regular_dump, 
                                            args=[delay, dumpfile])
        self.threadstop = False
        self.dump_thread.start()
        
    def regular_dump(self, delay, filename):
        """
        regular_dump(delay, filename) -> None
        
        Regularly dump to a file so that messages can be recovered if needed.
        """
        
        last_dump = time.time()
        while not self.threadstop:
            if time.time() - last_dump > delay:
                self.dump_messages(filename)
                last_dump = time.time()

            time.sleep(3)  #Calm CPU usage
    
    def dump_messages(self, filename):
        """
        dump_messages(filename) -> None
        
        Dump all the messages you have obtained in a file to be read in later.
        """
        
        with open(filename, 'w') as f:
            for user in self.messages:
                for i in self.messages[user]:
                    sender, message, timestamp = i
                    
                    f.write(str((user, sender, message, timestamp)) + "\n")
        
    def recover_messages(self, filename):
        """
        recover_messages(filename) -> None
        
        Recover all the messages that you previously dumped in a file
        """
        
        nots = None
        try:
            with open(filename) as f:
                nots = f.read().split('\n')
        except FileNotFoundError:
            return

        for n in nots:
            if len(n.strip()) != 0:
                user, sender, message, timestamp = eval(n)
                
                self.add_notification(user, sender, message, timestamp)
        
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
        if command == "!help" and self.nickname in info["content"]:
            self.send_chat("Use !notify to send messages to other people who "
                            "are currently unavailable.", info["id"])
        
        #Handle a notification request.
        elif command == "!notify":
            self.parse_notify(info, parts)
            
    def quit(self):
        self.threadstop = True
        self.dump_thread.join()
        
        super().quit()