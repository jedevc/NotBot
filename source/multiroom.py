import euphoria

import notification
import groups

import notifybot

class MultiRoom(euphoria.execgroup.ExecGroup):
    def __init__(self, rooms):
        super().__init__()

        grouping = groups.GroupManager("group.json")
        grouping.recover_groups()

        notifies = notification.NotificationManager("message.json", grouping)
        notifies.recover_notifications()

        for r in rooms:
            self.add(notifybot.NotifyBot(notifies, grouping, 60, r, rooms[r]))
