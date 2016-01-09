class Bar():
    completed = False

    @classmethod
    def condition(*args, **kwargs):
        sentence = kwargs.get('sentence')
        if len([True for t in sentence if t == ('foo', 'NN')]) > 0:
            return True

    @classmethod
    def response(cls, *args, **kwargs):
        cls.completed = True
        return ('bar')

    @classmethod
    def is_completed(cls, *args, **kwargs):
        return cls.completed
