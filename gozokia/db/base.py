'''
Gozokia model
based on Django settings module:
https://github.com/django/django/blob/master/django/conf/__init__.py
'''
import os
import importlib
from gozokia.conf import settings


class ModelBase(object):
    DEFAULT_ENGINE = 'gozokia.db.backends.memory'
    """
    Metaclass for all models.
    """

    def __init__(self, *args, **kwargs):
        try:
            mod = importlib.import_module(settings.DATABASES['default']['ENGINE'])
            self.db = mod.Database()
        except Exception:
            mod = importlib.import_module(self.DEFAULT_ENGINE)
            self.db = mod.Database()

    def get_db(self):
        return self.db

    def get(self, key=None, search=None):
        return self.db.get(key, search)

    def set_chat(self, chat):
        self.db.set({'chat': chat})

    def set(self, *args, **kwargs):
        return self.db.set(*args, **kwargs)
