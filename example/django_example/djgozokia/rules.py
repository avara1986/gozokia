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
        user = self.get_user()
        print("User:")
        print(self.get_user())
        if not user.first_name:
            # TODO: this is an aval example very very simple. Refactored
            name = ""
            sentence = self.sentence.lower()
            if sentence.startswith('i am') or sentence.startswith("i'm") or sentence.startswith("im"):
                name = sentence.split(" ")[-1]
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
