#A bot that notifies people.

import json

import multiroom
import euphoria as eu

rooms = dict()
with open("data/rooms.json", 'r') as f:
    rooms = json.loads(f.read())

def main():
    notifiers = multiroom.MultiRoom(rooms)

    eu.executable.start(notifiers)

if __name__ == "__main__":
    main()
