import euphoria

import euphoria.utils as ut

import time

class NotifyBot(euphoria.ping_room.PingRoom, euphoria.standard_room.StandardRoom):
    def __init__(self, messages, groups, roomname, password=None):
        super().__init__(roomname, password)
        self.nickname = "NotBot"
        self.help_text = ""
        with open("data/help.txt", 'r') as f:
            self.help_text = f.read()
        self.short_help_text = self.help_text.split('\n')[0]

        self.messages = messages
        self.groups = groups

        self.start_time = time.time()

    def parse_notify(self, info, parts):
        """
        parse_notify(info, parts) -> None

        Take the text and try to send it to the specified user.
        """

        #Divide the people and the message into two parts.
        users = []
        for p in parts:
            if p[0] == '@' or p[0] == '*':
                users.append(p)
            else:
                break

        if len(users) != 0 and len(users) != len(parts):
            sender = info["sender"]["name"]
            notification = " ".join(parts[len(users):])
            timestamp = info["time"]

            for user in users:
                self.send_chat(self.messages.add_notification(user, sender, notification, timestamp), info["id"])

    def parse_group(self, info, parts, add=True):
        """
        parse_group(info, parts) -> None

        Take the text and try to add someone to a group.
        """

        if len(parts) >= 2 and parts[0][0] == "*":
            # Check for non-users.
            for p in parts[1:]:
                if p[0] != "@":
                    return

            group = parts[0][1:]

            for entry in parts[1:]:
                user = entry[1:]

                if add:
                    self.send_chat(self.groups.add_to_group(user, group), info["id"])
                else:
                    self.send_chat(self.groups.remove_from_group(user, group), info["id"])

    def handle_chat(self, info):
        #Handle sending messages if the user speaks
        user = ut.filter_nick(info["sender"]["name"])
        if self.messages.has_notifications(user):
            ms = self.messages.get_notifications(user)
            for m in ms:
                self.send_chat(m, info["id"])

        #Now, begin proccessing the message
        #Split the message into parts and work out the command
        parts = info["content"].split()
        if len(parts) == 0:
            return
        command = parts[0]

        #!notify someone
        if command == "!notify":
            self.parse_notify(info, parts[1:])

        #Create a group
        elif command == "!group":
            self.parse_group(info, parts[1:], add=True)

        #Remove someone from a group
        elif command == "!ungroup":
            self.parse_group(info, parts[1:], add=False)

        #Get a list of all the groups
        elif command == "!grouplist":
            if len(parts) == 1:
                gs = self.groups.get_groups()
                if len(gs) != 0:
                    gs = ["*" + g for g in gs]
                    self.send_chat("\n".join(gs), info["id"])
            elif len(parts) == 2:
                if parts[1][0] == "*":
                    us = self.groups.get_users(parts[1][1:])
                    if len(us) != 0:
                        self.send_chat("\n".join(us), info["id"])
