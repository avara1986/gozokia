from gozokia.core.rules import RuleBase


class Bar(RuleBase):

    def __init__(self):
        self.set_reload(False)

    def condition_raise(self, *args, **kwargs):
        super(Bar, self).condition_raise(*args, **kwargs)
        if self.sentence.lower() == 'foo':
            return True

    def condition_completed(self, *args, **kwargs):
        self.set_completed()

    def response(self, *args, **kwargs):
        self.response_output = 'bar'


class BarSecond(RuleBase):

    def __init__(self):
        self.set_reload(False)

    def condition_raise(self, *args, **kwargs):
        super(BarSecond, self).condition_raise(*args, **kwargs)
        if self.sentence.lower() == 'foo':
            return True

    def condition_completed(self, *args, **kwargs):
        self.set_completed()

    def response(self, *args, **kwargs):
        self.response_output = 'bar second'
