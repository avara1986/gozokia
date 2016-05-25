# encoding: utf-8
from django.db import models


class SelectRelatedManager(models.Manager):

    def get_queryset(self):
        return super(SelectRelatedManager, self).get_queryset().select_related()


class GozokiaChatQuerySet(models.query.QuerySet):
    pass


class GozokiaChatManager(SelectRelatedManager):

    def get_queryset(self):
        return GozokiaChatQuerySet(self.model)
