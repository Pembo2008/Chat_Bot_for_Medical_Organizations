import datetime
from pymongo.errors import DuplicateKeyError
from pymongo.collection import Collection
from pymongo import MongoClient


def get_collection():
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['chat_bot']


def add_value(c):
    try:
        c.insert_one({'id': 3, 'patient': 'Petrov Petr', 'doctor':'Хирург','date':'30 апреля','time':'12.30'})
        return True
    except DuplicateKeyError:
        return False


collection = get_collection()['patients']
# add_value(collection)
q = collection.find({'date': "01.05.2023",'doctor':'Эндокринолог'})
for x in q:
  print(x['time'])