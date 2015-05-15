#A bot that notifies people.

import notifybot
import sys

def main():
    if len(sys.argv) > 1:
        bot = notifybot.NotifyBot(sys.argv[1])
        bot.run()
    else:
        print("Must select room for bot to enter.")

if __name__ == "__main__":
    main()