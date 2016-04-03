# encoding: utf-8
"""
Rules system.
All rules inherit from RuleBase. All rules needs a condition, a response
"""
from operator import itemgetter


class RuleBase(object):
    completed = False
    reload = True
    response_output = ""
    print_output = ""

    def __init__(self):
        self.set_reload(False)

    def condition_raise(self, *args, **kwargs):
        self.gozokia = kwargs.get('gozokia')
        self.analyzer = kwargs.get('analyzer')

    def condition_completed(self, *args, **kwargs):
        self.gozokia = kwargs.get('gozokia')
        self.analyzer = kwargs.get('analyzer')

    def response(self, *args, **kwargs):
        raise NotImplementedError(__class__.__name__ + ": response not defined")

    def get_response(self, *args, **kwargs):
        self.response(*args, **kwargs)
        return self.response_output, self.print_output

    def is_completed(self, *args, **kwargs):
        return self.completed

    def set_completed(self):
        self.completed = True

    def set_reload(self, reload):
        self.reload = reload

    def reload_rule(self):
        if self.reload:
            self.set_completed()
            return True
        else:
            return False

    def __str__(self):
        return self.__class__.__name__


class Rules(object):
    __rules_qeue = []

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

        self.__rules_qeue.append({'rule': rule_name, self.__RULE_KEY_CLASS: rule_object, 'rank': rank, 'type': type_rule})

    def get_rules(self, type_rule=None):
        f = lambda x: True
        if type_rule in [self._RAISE_COND, self._OBJETIVE_COND]:
            f = lambda x: x['type'] == type_rule and x[self.__RULE_KEY_CLASS].completed == False
        return sorted(filter(f, self.__rules_qeue), key=itemgetter('rank'))

    def get_rules_completed(self):
        return sorted(self.__rules_completed, key=itemgetter('rank'))

    def get_raises(self):
        for rule in self.get_rules(type_rule=self._RAISE_COND):
            yield rule

    def get_objetives(self):
        for rule in self.get_rules(type_rule=self._OBJETIVE_COND):
            yield rule

    def get_rule(self, gozokia):
        from gozokia.conf import settings
        """
        Get the active rule or find one.
        """
        if self.exist_active_rule():
            active_rule_object = self.get_active_rule(self.__RULE_KEY_CLASS)

            active_rule_object.condition_completed(gozokia=gozokia, analyzer=gozokia.analyzer)
            if active_rule_object.is_completed():
                if settings.DEBUG:
                    print("RULE {} end".format(active_rule_object))
                if active_rule_object.reload_rule() is False:
                    self.pop(self.get_active_rule())
                self.set_active_rule(None)
                self.get_rule(gozokia=gozokia)
        else:
            for r in self:
                if r['class'].condition_raise(gozokia=gozokia, analyzer=gozokia.analyzer):
                    if settings.DEBUG:
                        print("RULE {} start".format(r['class']))
                    self.set_active_rule(r)
                    break
            """
            TODO: Check if is needed split rules in objetives and raises
            for r in self.get_objetives():
                if r['class'].condition(gozokia=gozokia, analyzer=analyzer):
                    self.set_active_rule(r)
                    break
            if not self.exist_active_rule():
                for r in self.get_raises():
                    if r['class'].condition(gozokia=gozokia, analyzer=analyzer):
                        self.set_active_rule(r)
                        break
            """
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
        self.__rules_qeue = [r for r in self if r != rule]
        self.__rules_completed.append(rule)

    def __getitem__(self, key):
        if key in self.__rules_qeue:
            return self.__rules_qeue[key]
        raise KeyError

    def __iter__(self):
        for rule in self.get_rules():
            yield rule
