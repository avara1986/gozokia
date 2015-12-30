import nltk


class Analyzer():
    text = ""

    def __init__(self):
        pass

    def set(self, text):
        self.text = text

    def get_tagged(self):
        tokens = nltk.word_tokenize(self.text)
        return nltk.pos_tag(tokens)