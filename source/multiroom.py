import euphoria

import notification
import groups
import notifybot

import threading
import time

class MultiRoom(euphoria.execgroup.ExecGroup):
    def __init__(self, rooms, dumpdelay=60):
        super().__init__()

        self.grouping = groups.GroupManager("group.json")
        self.grouping.recover_groups()

        self.notifies = notification.NotificationManager("message.json", self.grouping)
        self.notifies.recover_notifications()

        for r in rooms:
            self.add(notifybot.NotifyBot(self.notifies, self.grouping, r, rooms[r]))

        self.dumper = euphoria.forever.ForeverCall(self.dump_all, dumpdelay)
        self.dumper.launch()

    def dump_all(self):
        """
        regular_dump() -> None

        Regularly dump to a file so that messages can be recovered if needed.
        """

        self.grouping.dump_groups()
        self.notifies.dump_notifications()

    def quit(self):
        super().quit()

        self.dumper.quit()
