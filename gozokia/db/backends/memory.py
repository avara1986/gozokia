
class Database():
    __records = []

    def __init__(self):
        pass

    def get(self):
        return self.__records

    def set(self, *args, **kwargs):
        print(args)
        self.__records.append(args[0])
