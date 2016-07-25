import os
import importlib

from gozokia.conf import settings


class Model(object):
    DEFAULT_ENGINE = 'gozokia.db.backends.memory'

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        """

        """
        try:
            mod = importlib.import_module(settings.DATABASES['default']['ENGINE'])
            return mod.Database()
        except Exception:
            mod = importlib.import_module(cls.DEFAULT_ENGINE)
            return mod.Database()

    def getdb(cls):
        return cls.db
