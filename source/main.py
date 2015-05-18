#A bot that notifies people.

import euphoria
import notifybot
import sys

def main():
    if len(sys.argv) >= 2:
        
        bot = None
        if len(sys.argv) == 2:
            bot = euphoria.room.Room(roomname=sys.argv[1])
        elif len(sys.argv) >= 3:
            bot = euphoria.room.Room(roomname=sys.argv[1], password=sys.argv[2])
        
        bot.add_component("ping", euphoria.ping_component.PingComponent(bot))
        bot.add_component("notify", notifybot.NotifyBot(bot))

        bot.run("NotBot")
    else:
        print("Invalid arguments.")

if __name__ == "__main__":
    main()