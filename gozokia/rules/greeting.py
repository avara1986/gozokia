from gozokia.core.rules import RuleBase


class Greeting(RuleBase):
    __OPTIONS = [
              'list_rules',
              'active_rule'
              ]
    __SELECTED_OPTION = None

    name = ""

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
        if len(self.sentence) == 1 and self.sentence[0][1] == "NN":
            name = " ".join(name for name, syntax in self.sentence)
        else:
            name = " ".join(name for name, syntax in filter(lambda x: x[1] == 'NNP', self.sentence))
        if len(self.gozokia.db.get('people')) == 0:
                users = self.gozokia.db.get('people', {'name': name})
                if len(users) == 0:
                    self.gozokia.db.set({'people': {'name': name}})
                if len(users) == 1:
                    pass
        return self.completed

    def response(self, *args, **kwargs):
        if len(self.gozokia.db.get('people')) == 0:
            return "Hi, who are you?"
        else:
            if len(self.gozokia.db.get('people')) == 1:
                self.completed = True
                return "Hi, {} :)".format(self.gozokia.db.get('people')[0]['name'])
        return None
