from gozokia.core.rules import RuleBase


class Greeting(RuleBase):
    __OPTIONS = [
              'list_rules',
              'active_rule'
              ]
    __SELECTED_OPTION = None

    def __init__(self):
        self.set_reload(False)

    def condition(self, *args, **kwargs):
        self.gozokia = kwargs.get('gozokia')
        self.sentence = kwargs.get('sentence')
        return True

    def is_completed(self, *args, **kwargs):
        print("Reload Rule: {}".format(self.reload))
        self.gozokia = kwargs.get('gozokia')
        self.sentence = kwargs.get('sentence')
        if self.gozokia.db.get('user') is False:
            name = " ".join(name for name, syntax in filter(lambda x: x[1] == 'NNP', self.sentence))
            self.gozokia.db.set({'user': name})
        else:
            self.completed = True

        return self.completed

    def response(self, *args, **kwargs):
        if self.completed is False:
            return "Hi, who are you?"
        else:
            return "Nice to meet yoy, {} :)".format(self.gozokia.db.get('user'))

