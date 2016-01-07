import nltk


class Analyzer():
    text = ""

    def __init__(self):
        pass

    def set(self, text):
        self.text = text

    def get_tokens(self):
        return nltk.word_tokenize(self.text)

    def get_tagged(self):
        return nltk.pos_tag(self.get_tokens())

    def get_entities(self):
        return nltk.chunk.ne_chunk(self.get_tagged())