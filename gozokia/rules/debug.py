from gozokia.conf import settings
from gozokia.core.rules import RuleBase


class Debug(RuleBase):
    __OPTIONS = ['list_rules',
                 'active_rule',
                 'list_settings',
                 ]
    __SELECTED_OPTION = None

    def __init__(self, *args, **kwargs):
        super(Debug, self).__init__(*args, **kwargs)
        self.set_reload(True)

    def condition_raise(self, *args, **kwargs):
        super(Debug, self).condition_raise(*args, **kwargs)
        self.sentence = self.analyzer.get_tagged()
        cond_list = ('show', 'VB'), ('me', 'PRP'), ('your', 'PRP$'), ('rules', 'NNS')
        cond_active = ('show', 'VB'), ('me', 'PRP'), ('the', 'DT'), ('active', 'JJ'), ('rule', 'NN')
        cond_settings = ('show', 'VB'), ('me', 'PRP'), ('the', 'DT'), ('settings', 'NNS')
        if len([True for t in self.sentence if t in cond_list]) == len(cond_list):
            self.__SELECTED_OPTION = 0
            return True
        if len([True for t in self.sentence if t in cond_active]) == len(cond_active):
            self.__SELECTED_OPTION = 1
            return True
        if len([True for t in self.sentence if t in cond_settings]) == len(cond_settings):
            self.__SELECTED_OPTION = 2
            return True

    def condition_completed(self, *args, **kwargs):
        self.set_completed()

    def response(self, *args, **kwargs):
        self.response_output = "Here is the debug response"

        if self.__SELECTED_OPTION is not None:
            print("### RULES OF SESSION {}".format(self.gozokia.session_id))
            if self.__OPTIONS[self.__SELECTED_OPTION] == 'list_rules':
                self.print_output = ("***** Activated rules *****\n")
                for rule in self.gozokia.rules:
                    self.print_output += str(rule) + "\n"
                self.print_output += ("***** Activated raises *****\n")
                for rule in self.gozokia.rules.get_raises():
                    self.print_output += str(rule) + "\n"
                self.print_output += ("***** Activated objectives *****\n")
                for rule in self.gozokia.rules.get_objetives():
                    self.print_output += str(rule) + "\n"
                self.print_output += ("***** Completed rules *****\n")
                for rule in self.gozokia.rules.get_rules_completed():
                    self.print_output += str(rule) + "\n"

            elif self.__OPTIONS[self.__SELECTED_OPTION] == 'active_rule':
                self.print_output = self.gozokia.rules.get_active_rule()
            elif self.__OPTIONS[self.__SELECTED_OPTION] == 'list_settings':
                self.print_output = ("***** Settings *****\n")
                for setting in dir(settings):
                    if setting.isupper():
                        self.print_output += str(setting) + " = " + str(getattr(settings, setting)) + "\n"
