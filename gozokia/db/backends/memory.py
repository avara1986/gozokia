
class Database():
    _records = {}

    def __init__(self):
        pass

    def get(self, key=None, search=None):
        if key is not None:
            try:
                if search is not None:
                    key_search = [k for k in search.keys()][0]
                    value = [k for k in search.values()][0]
                    return [u for u in self._records[key] if u.get(key_search) == value]
                return self._records[key]
            except KeyError:
                return []
        return self._records

    def set(self, *args, **kwargs):
        collection = [k for k in args[0].keys()][0]
        record = [k for k in args[0].values()][0]
        try:
            self._records[collection].append(record)
        except KeyError:
            self._records.update({collection: []})
            self._records[collection].append(record)
