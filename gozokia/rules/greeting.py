from gozokia.core.rules import RuleBase


class GreetingObjetive(RuleBase):

    def __init__(self):
        self.set_reload(False)

    def condition_raise(self, *args, **kwargs):
        super(GreetingObjetive, self).condition_raise(*args, **kwargs)
        return True

    def condition_completed(self, *args, **kwargs):
        super(GreetingObjetive, self).condition_completed(*args, **kwargs)
        # TODO: this is an aval example very very simple. Refactored
        sentence = self.sentence.lower()
        if sentence.startswith('i am') or sentence.startswith("i'm") or sentence.startswith("im"):
            self.name = sentence.split(" ")[-1]

    def response(self, *args, **kwargs):
        try:
            if self.name:
                self.response_output = "Hi, {}".format(self.name)
            else:
                self.response_output = "No name"
            self.set_completed()
        except AttributeError:
            self.response_output = "Hi, who are you?"


class GreetingRaise(GreetingObjetive):

    def condition_raise(self, *args, **kwargs):
        super(GreetingRaise, self).condition_raise(*args, **kwargs)
        if self.sentence.startswith('hi'):
            return True
