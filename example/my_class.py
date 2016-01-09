class MyClassObjetive():
    completed = False

    @classmethod
    def condition(cls, *args, **kwargs):
        return False

    @classmethod
    def response(cls, self, *args, **kwargs):
        return ('My Class Objetive')

    @classmethod
    def is_completed(cls, *args, **kwargs):
        return cls.completed