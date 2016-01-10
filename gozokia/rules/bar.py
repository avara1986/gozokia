from gozokia.core.rules import RuleBase


class Bar(RuleBase):

    def condition(self, *args, **kwargs):
        sentence = kwargs.get('sentence')
        if len([True for t in sentence if t == ('foo', 'NN')]) > 0:
            return True

    def response(self, *args, **kwargs):
        self.completed = True
        return ('bar')
