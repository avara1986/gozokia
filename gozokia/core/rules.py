# encoding: utf-8
"""
Rules system.
All rules inherit from RuleBase. All rules needs a condition, a response
"""
import copy
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
        self.analyzer = self.gozokia.analyzer
        self.sentence = self.gozokia.sentence

    def condition_completed(self, *args, **kwargs):
        self.gozokia = kwargs.get('gozokia')
        self.analyzer = self.gozokia.analyzer
        self.sentence = self.gozokia.sentence

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
    __rules_pool = []
    __rules_map = {}

    __rules_completed = []

    __active_rule = None

    _STATUS_RULES_KEY = "status"
    _STATUS_RULES = (0, 1, 2)

    _STATUS_RULE_COMPLETED = 0
    _STATUS_RULE_PENDING = 1
    _STATUS_RULE_ACTIVE = 2

    _RAISE_COND = 1

    _OBJETIVE_COND = 2

    __RULE_KEY_CLASS = "class"

    def __init__(self, * args, **kwargs):
        self.session_id = kwargs['sessionid']

        # Set the session to
        for rule_pool in self.__rules_pool:
            rule_pool['session'] = self.session_id

        self.__rules_map[self.session_id] = []

        self._rules_completed = self.__rules_map[self.session_id]

        self.__rules_map[self.session_id] = self.__rules_pool
        self.__rules_qeue = self.__rules_map[self.session_id]
        """
        self.__rules_qeue = copy.copy(self.__rules_pool)
        """

    def __exit__(self, exc_type, exc_value, traceback):
        print("DESTROY OBJECTS")
        del self.__rules_pool
        del self.__rules_map
        del self.__rules_completed
        del self.__active_rule

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

        # Session is none because "add" method is a decorator. When this method is executed
        # the init method not exist
        if rule_name not in set(r['rule'] for r in self.__rules_pool):
            self.__rules_pool.append({'session': None, 'rule': rule_name, self.__RULE_KEY_CLASS: copy.copy(rule_object),
                                      'rank': rank, 'type': type_rule,
                                      self._STATUS_RULES_KEY: self._STATUS_RULE_PENDING})

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
        """
        Get the active rule or find one.
        """
        if self.exist_active_rule():
            active_rule_object = self.get_active_rule(self.__RULE_KEY_CLASS)
            active_rule_object.condition_completed(gozokia=gozokia)
            if active_rule_object.is_completed():
                gozokia.logger.debug("RULE {} end".format(active_rule_object))
                if active_rule_object.reload_rule() is False:
                    self.pop(self.get_active_rule())
                self.set_active_rule(None)
                self.get_rule(gozokia=gozokia)
        else:
            for r in self:
                if r['class'].condition_raise(gozokia=gozokia):
                    gozokia.logger.debug("RULE {} start".format(r['class']))
                    self.set_active_rule(r)
                    break
        return self.__active_rule

    def set_rule_status_active(self, rule):
        rule[self._STATUS_RULES_KEY] = self._STATUS_RULE_ACTIVE
        self.set_active_rule(None)

    def set_rule_status_pending(self, rule):
        rule[self._STATUS_RULES_KEY] = self._STATUS_RULE_PENDING

    def set_rule_status_completed(self, rule):
        rule[self._STATUS_RULES_KEY] = self._STATUS_RULE_COMPLETED

    def set_active_rule(self, rule=None):
        if rule:
            self.set_rule_status_active(rule)
        self.__active_rule = rule

    def get_active_rule(self, key=None):
        if key is None:
            rule = self.__active_rule
        else:
            rule = self.__active_rule[key]
        return rule

    def stop_active_rule(self):
        self.set_rule_status_pending(self.__active_rule)
        self.set_active_rule(None)

    def exist_active_rule(self):
        return self.__active_rule is not None

    def pop(self, rule):
        self.__rules_qeue = [r for r in self if r != rule]
        self.set_rule_status_completed(rule)
        self.__rules_completed.append(rule)

    def __getitem__(self, key):
        if key in self.__rules_qeue:
            return self.__rules_qeue[key]
        raise KeyError

    def __iter__(self):
        for rule in self.get_rules():
            yield rule
