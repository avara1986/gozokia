from gozokia.core.rules import RuleBase


class Debug(RuleBase):
    __OPTIONS = [
              'list_rules',
              'active_rule'
              ]
    __SELECTED_OPTION = None

    def __init__(self, *args, **kwargs):
        super(Debug, self).__init__(*args, **kwargs)
        self.set_reload(True)

    def condition(self, *args, **kwargs):
        super(Debug, self).condition(*args, **kwargs)
        cond_list = ('show', 'VB'), ('me', 'PRP'), ('your', 'PRP$'), ('rules', 'NNS')
        cond_active = ('show', 'VB'), ('me', 'PRP'), ('the', 'DT'), ('active', 'JJ'), ('rule', 'NN')
        if len([True for t in self.sentence if t in cond_list]) == len(cond_list):
            self.__SELECTED_OPTION = 0
            return True
        if len([True for t in self.sentence if t in cond_active]) == len(cond_active):
            self.__SELECTED_OPTION = 1
            return True

    def response(self, *args, **kwargs):
        super(Debug, self).response(*args, **kwargs)
        if self.__SELECTED_OPTION is not None:
            if self.__OPTIONS[self.__SELECTED_OPTION] == 'list_rules':
                result = ("***** Activated rules *****\n")
                for rule in self.gozokia.rules:
                    result += str(rule) + "\n"
                result += ("***** Activated raises *****\n")
                for rule in self.gozokia.rules.get_raises():
                    result += str(rule) + "\n"
                result += ("***** Activated objectives *****\n")
                for rule in self.gozokia.rules.get_objetives():
                    result += str(rule) + "\n"
                result += ("***** Completed rules *****\n")
                for rule in self.gozokia.rules.get_rules_completed():
                    result += str(rule) + "\n"

            elif self.__OPTIONS[self.__SELECTED_OPTION] == 'active_rule':
                result = self.gozokia.rules.get_active_rule()

            self.completed = True

        return result

