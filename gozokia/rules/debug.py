class Debug():
    completed = False
    gozokia = None
    object = None

    @classmethod
    def condition(cls, *args, **kwargs):
        cls.gozokia = kwargs.get('gozokia')
        cls.sentence = kwargs.get('sentence')
        if len([True for t in cls.sentence if t == ('foo', 'NN')]) > 0:
            return True

    @classmethod
    def response(cls, *args, **kwargs):
        result = ("***** Activated rules *****\n")
        for rule in cls.gozokia.rules_map:
            result += str(rule) + "\n"
        result += ("***** Activated raises *****\n")
        for rule in cls.gozokia.rules_map.get_raises():
            result += str(rule) + "\n"
        result += ("***** Activated objectives *****\n")
        for rule in cls.gozokia.rules_map.get_objetives():
            result += str(rule) + "\n"
        return result

    @classmethod
    def is_completed(cls, *args, **kwargs):
        return cls.completed
