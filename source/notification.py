class NotificationManager:
    def __init__(self, dumpfile):
        self.messages = dict()

        self.filename = dumpfile

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

    def has_notifications(self, user):
        """
        has_notifications(user) -> Bool

        Tests if a user has some notifications waiting for them.
        """

        return (user in self.messages)

    def dump_notifications(self):
        """
        dump_notifications() -> None

        Dump all the messages you have obtained in a file to be read in later.
        """

        with open(self.filename, 'w') as f:
            for user in self.messages:
                for i in self.messages[user]:
                    sender, message, timestamp = i

                    f.write(str((user, sender, message, timestamp)) + "\n")

    def recover_notifications(self):
        """
        recover_notifications() -> None

        Recover all the messages that you previously dumped in a file
        """

        nots = []
        try:
            with open(self.filename) as f:
                nots = f.read().split('\n')
        except FileNotFoundError:
            return

        for n in nots:
            if len(n.strip()) != 0:
                user, sender, message, timestamp = eval(n)

                self.add_notification(user, sender, message, timestamp)
