import euphoria

import notification
import notifybot

class MultiRoom(euphoria.execgroup.ExecGroup):
    def __init__(self, rooms):
        super().__init__()

        notifies = notification.NotificationManager("message_dump.txt")

        for i in rooms:
            self.add(notifybot.NotifyBot(notifies, 2 * 60, i, rooms[i]))

    def run(self):
        print("Starting...")
        
        super().run()
        
    def quit(self):
        print("Quitting...")
        
        super().quit()
        
        print("Quit.")