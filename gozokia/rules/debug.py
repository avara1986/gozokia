from gozokia.core.rules import RuleBase


class Debug(RuleBase):

    gozokia = None
    object = None

    def condition(self, *args, **kwargs):
        self.gozokia = kwargs.get('gozokia')
        self.sentence = kwargs.get('sentence')
        cond = ('show', 'VB'), ('me', 'PRP'), ('your', 'PRP$'), ('rules', 'NNS')
        if len([True for t in self.sentence if t in cond]) == len(cond):
            return True

    def response(self, *args, **kwargs):
        result = ("***** Activated rules *****\n")
        for rule in self.gozokia.rules:
            result += str(rule) + "\n"
        result += ("***** Activated raises *****\n")
        for rule in self.gozokia.rules.get_raises():
            result += str(rule) + "\n"
        result += ("***** Activated objectives *****\n")
        for rule in self.gozokia.rules.get_objetives():
            result += str(rule) + "\n"
        return result
