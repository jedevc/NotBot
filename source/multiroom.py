import euphoria

import notifybot

class MultiRoom(euphoria.execgroup.ExecGroup):
    def __init__(self, rooms):
        super().__init__()

        for i in rooms:
            self.add(notifybot.NotifyBot("message_dump/%s.txt" % i, 3 * 60, i, rooms[i]))

    def run(self):
        print("Starting...")
        
        super().run()
        
    def quit(self):
        print("Quitting...")
        
        super().quit()
        
        print("Quit.")