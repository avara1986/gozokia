from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.db import models

from djgozokia.constants import TYPE_CHAT
from djgozokia.managers import GozokiaChatManager


class GozokiaChat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='chats',
                             blank=False, null=False
                             )
    type = models.IntegerField(
        choices=TYPE_CHAT,
    )
    objects = GozokiaChatManager()

    @classmethod
    def set_chat(cls, *args, **kwargs):
        pass

    @classmethod
    def get_chat(cls, *args, **kwargs):
        return []
