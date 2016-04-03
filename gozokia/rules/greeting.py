from gozokia.core.rules import RuleBase


class Greeting(RuleBase):
    __OPTIONS = [
              'list_rules',
              'active_rule'
              ]
    __SELECTED_OPTION = None

    def __init__(self):
        self.set_reload(False)

    def condition_raise(self, *args, **kwargs):
        super(Greeting, self).condition_raise(*args, **kwargs)
        return True

    def condition_completed(self, *args, **kwargs):
        super(Greeting, self).condition_completed(*args, **kwargs)
        self.sentence = self.analyzer.get_tagged()

        # TODO: this is an aval example very very simple. Refactored
        if len(self.sentence) == 1 and self.sentence[0][1] == "NN":
            name = " ".join(name for name, syntax in self.sentence)
        else:
            name = " ".join(name for name, syntax in filter(lambda x: x[1] == 'NNP', self.sentence))

        if len(self.gozokia.db.get('people')) == 0 and len(self.gozokia.db.get('people', {'name': name})) == 0:
            self.gozokia.db.set({'people': {'name': name}})
        elif len(self.gozokia.db.get('people')) == 1:
            self.set_completed()

    def response(self, *args, **kwargs):
        if len(self.gozokia.db.get('people')) == 0:
            self.response_output = "Hi, who are you?"
        else:
            if len(self.gozokia.db.get('people')) == 1:
                # self.set_completed()
                self.response_output = "Hi, {}".format(self.gozokia.db.get('people')[0]['name'])
            """
            TODO: Check when the DDBB have more than 1 user
            """
