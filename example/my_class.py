from gozokia.core.rules import RuleBase


class MyClassObjetive(RuleBase):

    def condition(self, *args, **kwargs):
        return False

    def response(self, *args, **kwargs):
        return ('My Class Objetive')
