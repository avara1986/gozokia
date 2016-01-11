from gozokia.core.rules import RuleBase


class Debug(RuleBase):
    __OPTIONS = [
              'list_rules',
              'active_rule'
              ]
    __SELECTED_OPTION = None

    def condition(self, *args, **kwargs):
        self.gozokia = kwargs.get('gozokia')
        self.sentence = kwargs.get('sentence')
        cond_list = ('show', 'VB'), ('me', 'PRP'), ('your', 'PRP$'), ('rules', 'NNS')
        cond_active = ('show', 'VB'), ('me', 'PRP'), ('the', 'DT'), ('active', 'JJ'), ('rule', 'NN')
        if len([True for t in self.sentence if t in cond_list]) == len(cond_list):
            self.__SELECTED_OPTION = 0
            return True
        if len([True for t in self.sentence if t in cond_active]) == len(cond_active):
            self.__SELECTED_OPTION = 1
            return True

    def response(self, *args, **kwargs):
        if self.__SELECTED_OPTION is not None:
            if self.__OPTIONS[self.__SELECTED_OPTION] == 'list_rules':
                self.gozokia.db.set("TEST")
                self.gozokia.db.set("TEST")
                self.gozokia.db.set("TEST")
                result = ("***** Activated rules *****\n")
                for rule in self.gozokia.rules:
                    result += str(rule) + "\n"
                result += ("***** Activated raises *****\n")
                for rule in self.gozokia.rules.get_raises():
                    result += str(rule) + "\n"
                result += ("***** Activated objectives *****\n")
                for rule in self.gozokia.rules.get_objetives():
                    result += str(rule) + "\n"

            elif self.__OPTIONS[self.__SELECTED_OPTION] == 'active_rule':
                result = self.gozokia.rules.get_active_rule()

            self.completed = True

        return result

