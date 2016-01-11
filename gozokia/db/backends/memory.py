
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
        # print(args)
        self.__records.update(args[0])
