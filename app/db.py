import urllib.parse
from pymongo import MongoClient

from . import config

PASSWORD = urllib.parse.quote_plus(config.PASSWORD)

client = MongoClient(f"mongodb+srv://{config.USERNAME}:{PASSWORD}@{config.HOST}/?retryWrites=true&w=majority")

db = client.mpac