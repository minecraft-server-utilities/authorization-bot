import json
from dataclasses import dataclass, asdict
from dacite import from_dict
from pprint import pprint

from utils import Singleton


@dataclass
class Entry:
    username: str
    discord_id: str
    password: str = ""


class Storage(metaclass=Singleton):
    def __init__(self):
        self._initialized = False
        self._file = ""
        self.entries: list[Entry] = []

    def init(self, file: str):
        self._file = file
        with open(file, 'a+') as storage_file:
            storage_file.seek(0)
            contents = storage_file.read()
            entries = [] if len(contents) == 0 else json.loads(storage_file)

            for entry in entries:
                self.entries.append(from_dict(Entry, entry))

        pprint(self.entries)
        self._initialized = True

    def save(self):
        entries = json.dumps([asdict(e) for e in self.entries])
        with open(self._file, 'w') as storage_file:
            storage_file.write(entries)
