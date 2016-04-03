from gozokia.core.rules import RuleBase


class Bar(RuleBase):
    def __init__(self):
        self.set_reload(False)

    def condition(self, *args, **kwargs):
        self.analyzer = kwargs.get('analyzer')
        self.sentence = self.analyzer.get_tagged()
        if len([True for t in self.sentence if t == ('foo', 'NN')]) > 0:
            return True

    def response(self, *args, **kwargs):
        self.completed = True
        return ('bar')

    def is_completed(self, *args, **kwargs):
        return self.completed


class BarSecond(RuleBase):
    def __init__(self):
        self.set_reload(False)

    def condition(self, *args, **kwargs):
        self.analyzer = kwargs.get('analyzer')
        self.sentence = self.analyzer.get_tagged()
        if len([True for t in self.sentence if t == ('foo', 'NN')]) > 0:
            return True

    def response(self, *args, **kwargs):
        self.completed = True
        return ('bar second')

    def is_completed(self, *args, **kwargs):
        return self.completed
