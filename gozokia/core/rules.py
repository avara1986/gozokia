from operator import itemgetter


class Rule(object):
    __rules = []

    def add(self, rule):
        self.__rules.append(rule)

    def get_rules(self):
        return sorted(self.__rules, key=itemgetter('rank'))

    def __getitem__(self, key):
        if key in self.__rules:
            return self.__rules[key]
        raise KeyError

    def __iter__(self):
        for rule in self.get_rules():
            yield rule
