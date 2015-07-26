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

        #Threading crap
        self.dump_thread = threading.Thread(target=self.regular_dump,
                                            args=[dumpdelay])
        self.threadstop = False

    def ready(self):
        self.dump_thread.start()

    def regular_dump(self, delay):
        """
        regular_dump(delay) -> None

        Regularly dump to a file so that messages can be recovered if needed.
        """

        last_dump = time.time()
        while not self.threadstop:
            if time.time() - last_dump > delay:
                self.grouping.dump_groups()
                self.notifies.dump_notifications()
                last_dump = time.time()

            time.sleep(3)  #Calm CPU usage

    def cleanup(self):
        self.threadstop = True
        self.dump_thread.join()
