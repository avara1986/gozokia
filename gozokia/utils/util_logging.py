"""
Libs imports
"""
import logging

"""
Project imports
"""
from gozokia.conf import settings


class Logging(object):

    def __init__(self, module_name):
        if settings.DEBUG:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(module_name)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)
