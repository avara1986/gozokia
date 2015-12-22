
class Rule(object):
    __rules = []

    def add(self, rule):
        self.__rules.append(rule)

    def get_rules(self):
        return self.__rules

    def __repr__(self):
        return self.get_rules()