import json

class Dumper:
    def __init__(self, dumpfile):
        self.filename = "dump/" + dumpfile

    def dump(self, data):
        """
        dump() -> None

        Dump the data into a file.
        """

        with open(self.filename, 'w') as f:
            f.write(json.dumps(data))

    def recover(self):
        """
        recover() -> Data

        Recover all the data that you previously dumped in a file
        """

        data = None
        try:
            with open(self.filename) as f:
                data = json.loads(f.read())
        except FileNotFoundError:
            return None

        return data
