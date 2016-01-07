from operator import itemgetter


class Rule(object):
    __rules = []

    def add(self, rule):
        self.__rules.append(rule)

    def get_rules(self, cond=None):
        f = lambda x: True
        if cond == 'raise' or cond == 'objetive':
            f = lambda x: x['type'] == cond
        return sorted(map(f, self.__rules), key=itemgetter('rank'))

    def get_rules_rises(self):
        return self.get_rules('raise')

    def get_rules_objetives(self):
        return self.get_rules('objetive')

    def __getitem__(self, key):
        if key in self.__rules:
            return self.__rules[key]
        raise KeyError

    def __iter__(self):
        for rule in self.get_rules():
            yield rule
