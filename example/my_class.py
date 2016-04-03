from gozokia.core.rules import RuleBase


class MyClassObjetive(RuleBase):

    def condition_raise(self, *args, **kwargs):
        return False

    def response(self, *args, **kwargs):
        self.response_output = 'My Class Objetive'
