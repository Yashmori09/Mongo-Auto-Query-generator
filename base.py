import configparser
from pymongo import MongoClient
from constant import*


class Base:
    __FILE__ = CONFIG_FILE

    def __init__(self) -> None:
        self.cfg = self.setup_config()

    def setup_config(self):
        configParser = configparser.RawConfigParser()
        configParser.read(Base.__FILE__)
        return configParser


class MongoDB(Base):

    def __init__(self) -> None:
        super().__init__()
        client = MongoClient(self.cfg.get('database4', 'uri'))
        dbname = self.cfg.get('database4', 'dbname')
        self.db = client[dbname]
