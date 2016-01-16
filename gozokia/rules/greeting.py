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
        # print("Reload Rule: {}".format(self.reload))
        self.gozokia = kwargs.get('gozokia')
        self.sentence = kwargs.get('sentence')
        if self.gozokia.db.get('users') is False:
            if len(self.sentence) == 1 and self.sentence[0][1] == "NN":
                name = " ".join(name for name, syntax in self.sentence)
            else:
                name = " ".join(name for name, syntax in filter(lambda x: x[1] == 'NNP', self.sentence))
            if len(name):
                self.gozokia.db.set({'users': {'name': name}})

        return self.completed

    def response(self, *args, **kwargs):
        if self.gozokia.db.get('users') is False:
            return "Hi, who are you?"
        else:
            self.completed = True
            return "Nice to meet you, {} :)".format(self.gozokia.db.get('users')[0]['name'])

