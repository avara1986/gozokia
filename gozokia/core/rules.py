from operator import itemgetter


class RuleBase(object):
    completed = False

    def condition(self, *args, **kwargs):
        return NotImplemented

    def response(self, *args, **kwargs):
        return NotImplemented

    def is_completed(self, *args, **kwargs):
        return self.completed


class Rules(object):
    __rules = []

    __rules_completed = []

    _RAISE_COND = 1

    _OBJETIVE_COND = 2

    def add(self, rule_name, rule_class=None, **options):
        rank = 10
        type_rule = None
        if 'rank' in options and type(options['rank']) is int:
            rank = options['rank']
        if 'type' in options and type(options['type']) is int:
            type_rule = options['type']
        rule_object = rule_class()
        self.__rules.append({'rule': rule_name, 'class': rule_object, 'rank': rank, 'type': type_rule})

    def get_rules(self, type_rule=None):
        f = lambda x: True
        if type_rule == self._RAISE_COND or type_rule == self._OBJETIVE_COND:
            f = lambda x: x['type'] == type_rule
        return sorted(filter(f, self.__rules), key=itemgetter('rank'))

    def get_raises(self):
        for rule in self.get_rules(type_rule=self._RAISE_COND):
            yield rule

    def get_objetives(self):
        for rule in self.get_rules(type_rule=self._OBJETIVE_COND):
            yield rule

    def pop(self, rule):
        self.__rules = [r for r in self if r != rule]
        self.__rules_completed.append(rule)

    def __getitem__(self, key):
        if key in self.__rules:
            return self.__rules[key]
        raise KeyError

    def __iter__(self):
        for rule in self.get_rules():
            yield rule
