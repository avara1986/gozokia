from operator import itemgetter


class Rules(object):
    __rules = []

    __rules_completed = []

    _RAISE_COND = 1

    _OBJETIVE_COND = 2

    def add(self, rule):
        self.__rules.append(rule)

    def get_rules(self, type_rule=None):
        f = lambda x: True
        if type_rule == self._RAISE_COND or type_rule == self._OBJETIVE_COND:
            f = lambda x: x['type'] == type_rule
        return sorted(filter(f, self.__rules), key=itemgetter('rank'))

    def get_raises(self):
        for rule in self.get_rules(type_rule=self._RAISE_COND):
            yield rule

    def pop(self, rule):
        self.__rules = [r for r in self if r != rule]
        self.__rules_completed.append(rule)

    def get_objetives(self):
        for rule in self.get_rules(type_rule=self._OBJETIVE_COND):
            yield rule

    def __getitem__(self, key):
        if key in self.__rules:
            return self.__rules[key]
        raise KeyError

    def __iter__(self):
        for rule in self.get_rules():
            yield rule
