from django.contrib.auth import get_user_model

from gozokia.core.rules import RuleBase


class ModelMixin(object):

    def get_user(self):
        return get_user_model().objects.get(id=self.gozokia.user_id)


class GreetingObjetive(RuleBase, ModelMixin):

    def __init__(self):
        self.set_reload(False)

    def condition_raise(self, *args, **kwargs):
        super(GreetingObjetive, self).condition_raise(*args, **kwargs)
        return True

    def condition_completed(self, *args, **kwargs):
        super(GreetingObjetive, self).condition_completed(*args, **kwargs)
        print("#### CHECK CONDITION")
        user = self.get_user()
        if not user.first_name:
            self.sentence_parsed = self.analyzer.get_tagged()
            if len(self.sentence_parsed) == 1 and self.sentence_parsed[0][1] == "NN":
                name = " ".join(name for name, syntax in self.sentence_parsed)
            else:
                name = " ".join(name for name, syntax in filter(lambda x: x[1] == 'NNP', self.sentence_parsed))
            user.first_name = name
            user.save()
        else:
            pass  # self.set_completed()

    def response(self, *args, **kwargs):
        user = self.get_user()
        if not user.first_name:
            self.response_output = "Hi, who are you?"
        else:
            self.response_output = "Hi, {}".format(user.first_name)
            self.set_completed()


class GreetingRaise(GreetingObjetive):

    def condition_raise(self, *args, **kwargs):
        print("### RAISE")
        super(GreetingRaise, self).condition_raise(*args, **kwargs)
        if self.sentence.startswith('hi'):
            return True


class Whoami(RuleBase, ModelMixin):

    def __init__(self):
        self.set_reload(True)

    def condition_raise(self, *args, **kwargs):
        super(Whoami, self).condition_raise(*args, **kwargs)
        if self.sentence.startswith('who am i'):
            return True

    def condition_completed(self, *args, **kwargs):
        super(Whoami, self).condition_completed(*args, **kwargs)
        self.set_completed()

    def response(self, *args, **kwargs):
        user = self.get_user()
        self.response_output = "You are {}".format(user.first_name)
