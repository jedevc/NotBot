#A bot that notifies people.

import notifybot
import euphoria as eu

import sys

def main():
    if len(sys.argv) >= 2:
        
        bot = None
        if len(sys.argv) == 2:
            bot = notifybot.NotifyBot(dumpfile="message_dump.txt", delay=60, 
                                      roomname=sys.argv[1])
        elif len(sys.argv) >= 3:
            bot = notifybot.NotifyBot(dumpfile="message_dump.txt", delay=60,
                                      roomname=sys.argv[1], 
                                      password=sys.argv[2])
            
        eu.executable.start(bot)
    else:
        print("Invalid arguments.")

if __name__ == "__main__":
    main()