
class Rule(object):
    __rules = []

    def add(self, rule):
        self.__rules.append(rule)

    def get_rules(self):
        return self.__rules

    def __iter__(self):
        for rule in self.get_rules():
            yield rule

    def __iteritems__(self):
        for key, value in self.get_rules().items():
            yield key, value
