import json
from dataclasses import dataclass

from dacite import from_dict


@dataclass
class Config:
    token: str
    db_file: str

    @classmethod
    def load(cls, file: str) -> 'Config':
        with open(file) as config_file:
            config_dict = json.load(config_file)

        return from_dict(Config, config_dict)
