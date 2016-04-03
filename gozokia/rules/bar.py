from gozokia.core.rules import RuleBase


class Bar(RuleBase):
    def __init__(self):
        self.set_reload(False)

    def condition_raise(self, *args, **kwargs):
        self.analyzer = kwargs.get('analyzer')
        self.sentence = self.analyzer.get_tagged()
        if len([True for t in self.sentence if t == ('foo', 'NN')]) > 0:
            return True

    def condition_completed(self, *args, **kwargs):
        self.set_completed()

    def response(self, *args, **kwargs):
        self.response_output = 'bar'


class BarSecond(RuleBase):
    def __init__(self):
        self.set_reload(False)

    def condition_raise(self, *args, **kwargs):
        self.analyzer = kwargs.get('analyzer')
        self.sentence = self.analyzer.get_tagged()
        if len([True for t in self.sentence if t == ('foo', 'NN')]) > 0:
            return True

    def condition_completed(self, *args, **kwargs):
        self.set_completed()

    def response(self, *args, **kwargs):
        self.response_output = 'bar second'
