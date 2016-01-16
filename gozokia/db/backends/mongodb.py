from pymongo import MongoClient
from gozokia.conf import settings


class Database():
    client = {}

    def __init__(self):
        self.client = MongoClient("mongodb://{}:{}".format(
                                 settings.DATABASES['default']['HOST'],
                                 settings.DATABASES['default']['PORT'],
                                 ))
        self.db = self.client[settings.DATABASES['default']['NAME']]
        pass

    def get(self, key=None):
        if key is not None:
            return [c for c in self.db[key].find()]

    def set(self, *args, **kwargs):
        collection = [k for k in args[0].keys()][0]
        record = [k for k in args[0].values()][0]
        documents = self.db[collection]
        document_id = documents.insert_one(record).inserted_id
        print(document_id)
