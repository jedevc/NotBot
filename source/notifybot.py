import euphoria

import time
import threading

import utilities as ut

class NotifyBot(euphoria.ping_room.PingRoom, euphoria.chat_room.ChatRoom):
    def __init__(self, messages, groups, dumpdelay, roomname, password=None):
        super().__init__(roomname, password)
        self.nickname = "NotBot"

        self.groups = groups
        self.messages = messages

        self.helptxt = ""
        with open("data/help.txt", 'r') as f:
            self.helptxt = f.read()

        #Threading crap
        self.dump_thread = threading.Thread(target=self.regular_dump,
                                            args=[dumpdelay])
        self.threadstop = False
        self.dump_thread.start()

    def regular_dump(self, delay):
        """
        regular_dump(delay) -> None

        Regularly dump to a file so that messages can be recovered if needed.
        """

        last_dump = time.time()
        while not self.threadstop:
            if time.time() - last_dump > delay:
                self.messages.dump_notifications()
                self.groups.dump_groups()
                last_dump = time.time()

            time.sleep(3)  #Calm CPU usage

    def send_notifications(self, user, info):
        """
        send_notifications(user, info) -> None

        Send all the messages queued by the bot.
        """

        messages = self.messages.get_notifications(user)

        for message in messages:
            user, content, timestamp = message
            tosend = "[" + user + ", " + ut.extract_time(int(time.time()) -
                        timestamp) + " ago] " + content
            self.send_chat(tosend, info["id"])

    def parse_notify(self, info, parts):
        """
        parse_notify(info, parts) -> None

        Take the text and try to send it to the specified user.
        """

        if len(parts) >= 2:
            #Divide the people and the message into two parts.
            user = parts[0]
            sender = info["sender"]["name"]
            notification = " ".join(parts[1:])
            timestamp = info["time"]

            self.send_chat(self.messages.add_notification(user, sender, notification, timestamp), info["id"])

    def parse_group(self, info, parts, add=True):
        """
        parse_group(info, parts) -> None

        Take the text and try to add someone to a group.
        """

        if len(parts) == 2 and parts[0][0] == "*" and parts[1][0] == "@":
            group = parts[0][1:]
            user = parts[1][1:]

            if add:
                self.send_chat(self.groups.add_to_group(user, group), info["id"])
            else:
                self.send_chat(self.groups.remove_from_group(user, group), info["id"])

    def handle_chat(self, info):
        #Handle sending messages if the user speaks
        user = ut.filter_nick(info["sender"]["name"])
        if self.messages.has_notifications(user):
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
        elif command == "!help" and self.nickname in info["content"]:
            self.send_chat(self.helptxt, info["id"])

        #Handle a notification request.
        elif command == "!notify":
            self.parse_notify(info, parts[1:])

        #Handle a request to create a group
        elif command == "!group":
            self.parse_group(info, parts[1:], add=True)

        elif command == "!ungroup":
            self.parse_group(info, parts[1:], add=False)

    def cleanup(self):
        self.threadstop = True
        self.dump_thread.join()
