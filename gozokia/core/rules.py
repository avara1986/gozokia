from operator import itemgetter


class RuleBase(object):
    completed = False
    reload = True

    def condition(self, *args, **kwargs):
        return NotImplemented

    def response(self, *args, **kwargs):
        return NotImplemented

    def is_completed(self, *args, **kwargs):
        return self.completed

    def set_reload(self, reload):
        self.reload = reload

    def reload_rule(self):
        if self.reload:
            self.completed = False
            return True
        else:
            return False

    def __str__(self):
        return self.__class__.__name__


class Rules(object):
    __rules = []

    __rules_completed = []

    __active_rule = None

    _RAISE_COND = 1

    _OBJETIVE_COND = 2

    __RULE_KEY_CLASS = "class"

    def add(self, rule_class, **options):
        rank = 10
        type_rule = None

        rule_object = rule_class()

        if 'rank' in options and type(options['rank']) is int:
            rank = options['rank']
        if 'type' in options and type(options['type']) is int:
            type_rule = options['type']
        if 'name' in options and type(options['name']) is str:
            rule_name = options['name']
        else:
            rule_name = str(rule_object)

        self.__rules.append({'rule': rule_name, self.__RULE_KEY_CLASS: rule_object, 'rank': rank, 'type': type_rule})

    def get_rules(self, type_rule=None):
        f = lambda x: True
        if type_rule == self._RAISE_COND or type_rule == self._OBJETIVE_COND:
            f = lambda x: x['type'] == type_rule and x[self.__RULE_KEY_CLASS].completed == False
        return sorted(filter(f, self.__rules), key=itemgetter('rank'))

    def get_raises(self):
        for rule in self.get_rules(type_rule=self._RAISE_COND):
            yield rule

    def get_objetives(self):
        for rule in self.get_rules(type_rule=self._OBJETIVE_COND):
            yield rule

    def get_rule(self, gozokia, sentence):
        # TODO:
        if self.exist_active_rule():
            if self.get_active_rule(self.__RULE_KEY_CLASS).is_completed(gozokia=gozokia, sentence=sentence):
                print("RULE {} is completed".format(self.get_active_rule(self.__RULE_KEY_CLASS)))
                if self.get_active_rule(self.__RULE_KEY_CLASS).reload_rule() is False:
                    self.pop(self.get_active_rule())
                self.set_active_rule(None)
                self.get_rule(gozokia=gozokia, sentence=sentence)
        else:
            for r in self.get_objetives():
                if r['class'].condition(gozokia=gozokia, sentence=sentence):
                    self.set_active_rule(r)
                    break
            if not self.exist_active_rule():
                for r in self.get_raises():
                    if r['class'].condition(gozokia=gozokia, sentence=sentence):
                        self.set_active_rule(r)
                        break

        return self.__active_rule

    def set_active_rule(self, rule=None):
        self.__active_rule = rule

    def get_active_rule(self, key=None):
        if key is None:
            rule = self.__active_rule
        else:
            rule = self.__active_rule[key]
        return rule

    def exist_active_rule(self):
        return self.__active_rule is not None

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
