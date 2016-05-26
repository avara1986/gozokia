try:
    import nltk
except ImportError:
    nltk = False

from gozokia.conf import settings


class Analyzer():
    # Text Analyzer:
    ta = None

    text = ""

    def __init__(self):
        pass

    def set(self, text):
        if settings.GOZOKIA_TEXT_ANALYZER_ENGINE == "nltk":
            self.ta = nltk
        self.text = text

    def get_tokens(self):
        if self.ta:
            return self.ta.word_tokenize(self.text)
        return self.text

    def get_tagged(self):
        if self.ta:
            return self.ta.pos_tag(self.get_tokens())
        return self.text

    def get_entities(self):
        if self.ta:
            return self.ta.chunk.ne_chunk(self.get_tagged())
        return self.text
