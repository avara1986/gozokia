# encoding: utf-8
"""
Rules system.

"""
import copy
from operator import itemgetter


class RuleBase(object):
    """
    All rules inherit from RuleBase. All rules needs a condition, a response.

    RuleBase is the base model to all rules. with this class, the rules will can to access
    to the main class (Gozokia), the sentence (the input), and/or the
    analyzer (if it is active)
    """
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

    def set_completed(self, status=True):
        self.completed = status

    def set_reload(self, reload):
        self.reload = reload

    def reload_rule(self):
        if self.reload:
            self.set_completed(False)
            return True
        else:
            return False

    def __str__(self):
        return self.__class__.__name__


class Rules(object):
    __rules_pool = []
    __rules_map = {}

    __rules_qeue = []
    __rules_qeue_completed = []

    __active_rule = None

    _STATUS_RULES_KEY = "status"
    _STATUS_RULES = (0, 1, 2)

    _STATUS_RULE_COMPLETED = 0
    _STATUS_RULE_PENDING = 1
    _STATUS_RULE_ACTIVE = 2

    _RAISE_COND = 1

    _OBJETIVE_COND = 2

    __RULE_KEY_CLASS = "class"
    __RULE_KEY_NAME = "rule"

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
        """
        return a diccionary of rules order by rank and filter by type or fule
        """
        f = lambda x: True
        if type_rule in [self._RAISE_COND, self._OBJETIVE_COND]:
            f = lambda x: x['type'] == type_rule and x[self.__RULE_KEY_CLASS].completed == False
        return sorted(filter(f, self.__rules_qeue), key=itemgetter('rank'))

    def get_rules_completed(self):
        return sorted(self.__rules_qeue_completed, key=itemgetter('rank'))

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
            active_rule_object = self.get_active_rule().get(self.__RULE_KEY_CLASS)
            active_rule_object.condition_completed(gozokia=gozokia)
            if active_rule_object.is_completed():
                self.complete_active_rule()
                self.get_rule(gozokia=gozokia)
        else:
            for r in self:
                if r.get(self.__RULE_KEY_CLASS).condition_raise(gozokia=gozokia):
                    self.set_active_rule(r)
                    break
        return self.__active_rule

    def eval(self, gozokia):
        response_output = None
        print_output = None
        rule = self.get_rule(gozokia)
        if rule:
            active_rule_object = rule.get(self.__RULE_KEY_CLASS)
            response_output, print_output = active_rule_object.get_response()
            active_rule_object.condition_completed(gozokia=gozokia)
            if active_rule_object.is_completed():
                self.complete_active_rule()
        return rule, response_output, print_output

    def set_rule_status_active(self, rule):
        print("RULE {} start".format(rule.get(self.__RULE_KEY_NAME)))
        rule[self._STATUS_RULES_KEY] = self._STATUS_RULE_ACTIVE
        self.set_active_rule(None)

    def set_rule_status_pending(self, rule):
        print("RULE {} pending".format(rule.get(self.__RULE_KEY_NAME)))
        rule[self._STATUS_RULES_KEY] = self._STATUS_RULE_PENDING

    def set_rule_status_completed(self, rule):
        print("RULE {} completed".format(rule.get(self.__RULE_KEY_NAME)))
        rule[self._STATUS_RULES_KEY] = self._STATUS_RULE_COMPLETED

    def complete_active_rule(self):
        rule = self.get_active_rule()
        self.set_rule_completed(rule)
        self.set_active_rule(None)

    def set_rule_completed(self, rule):
        self.set_rule_status_completed(rule)
        if rule.get(self.__RULE_KEY_CLASS).reload_rule() is False:
            self.pop(rule)

    def set_rule_pending(self, rule):
        self.set_rule_status_pending(rule)

    def get_active_rule(self, key=None):
        if key is None:
            rule = self.__active_rule
        else:
            rule = self.__active_rule[key]
        return rule

    def set_active_rule(self, rule=None):
        if rule:
            self.set_rule_status_active(rule)
        self.__active_rule = rule

    def stop_active_rule(self):
        self.set_rule_status_pending(self.__active_rule)
        self.set_active_rule(None)

    def exist_active_rule(self):
        return self.__active_rule is not None

    def pop(self, rule):
        # Pop rule from main queue
        self.__rules_qeue = [r for r in self if r.get(self.__RULE_KEY_CLASS) != rule.get(self.__RULE_KEY_CLASS)]

        # Add rule to completed queue
        if rule.get(self.__RULE_KEY_CLASS) not in set(r.get(rule.get(self.__RULE_KEY_CLASS)) for r in self.__rules_qeue_completed):
            self.__rules_qeue_completed.append(rule)

    def __getitem__(self, key):
        if key in self.__rules_qeue:
            return self.__rules_qeue[key]
        raise KeyError

    def __iter__(self):
        for rule in self.get_rules():
            yield rule
