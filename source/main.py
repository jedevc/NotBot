#A bot that notifies people.

import multiroom
import euphoria as eu

rooms = {"xkcd": None,
         "bots": None,
         "test": None,
         "music": None}

def main():
    notifiers = multiroom.MultiRoom({"testing": None})
    
    eu.executable.start(notifiers)

if __name__ == "__main__":
    main()