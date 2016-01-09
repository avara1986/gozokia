from operator import itemgetter


class Rules(object):
    __rules = []

    _RAISE_COND = "raise"

    _OBJETIVE_COND = "objetive"

    def add(self, rule):
        self.__rules.append(rule)

    def get_rules(self, type=None):
        f = lambda x: True
        if type == self._RAISE_COND or type == self._OBJETIVE_COND:
            f = lambda x: x['type'] == type
        return sorted(filter(f, self.__rules), key=itemgetter('rank'))

    def get_raises(self):
        for rule in self.get_rules(type=self._RAISE_COND):
            yield rule

    def pop(self, rule):
        self.__rules = [r for r in self if r != rule]

    def get_objetives(self):
        for rule in self.get_rules(type=self._OBJETIVE_COND):
            yield rule

    def __getitem__(self, key):
        if key in self.__rules:
            return self.__rules[key]
        raise KeyError

    def __iter__(self):
        for rule in self.get_rules():
            yield rule
