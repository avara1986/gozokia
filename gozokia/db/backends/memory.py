
class Database():
    __records = {}

    def __init__(self):
        pass

    def get(self, key=None):
        if key is not None:
            try:
                return self.__records[key]
            except KeyError:
                return False;
        return self.__records

    def set(self, *args, **kwargs):
        collection = [k for k in args[0].keys()][0]
        record = [k for k in args[0].values()][0]
        try:
            self.__records[collection].append(record)
        except KeyError:
            self.__records.update({collection: []})
            self.__records[collection].append(record)
