import euphoria

import notification
import groups
import notifybot

class MultiRoom(euphoria.execgroup.ExecGroup):
    def __init__(self, rooms):
        super().__init__()

        notifies = notification.NotificationManager("message_dump.txt")
        notifies.recover_notifications()

        grouping = groups.GroupManager("group_dump.txt")
        grouping.recover_groups()

        for i in rooms:
            self.add(notifybot.NotifyBot(notifies, grouping, 60, i, rooms[i]))
