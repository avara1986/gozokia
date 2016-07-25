# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from djgozokia.constants import TYPE_CHAT
from djgozokia.managers import GozokiaChatManager


@python_2_unicode_compatible
class GozokiaChat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='chats',
                             blank=False, null=False
                             )
    session = models.ForeignKey(Session, blank=False, null=False)
    rule = models.CharField(
        choices=TYPE_CHAT, max_length=70, blank=True, null=True
    )
    type_rule = models.CharField(
        choices=TYPE_CHAT, max_length=2, blank=True, null=True
    )
    text = models.TextField(verbose_name=u'Texto', blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    objects = GozokiaChatManager()

    @classmethod
    def set_chat(cls, *args, **kwargs):
        kwargs['user'] = get_user_model().objects.get(id=kwargs['user'])
        kwargs['session'] = Session.objects.get(session_key=kwargs['session'])
        GozokiaChat.objects.create(**kwargs)

    @classmethod
    def get_chat(cls, *args, **kwargs):
        return [u for u in GozokiaChat.objects.filter(user__id=kwargs['user'], session__session_key=kwargs['session'])]

    class Meta:
        verbose_name = _('Gozokia Chat')
        verbose_name_plural = _('Gozokia Chats')
        ordering = ('timestamp',)

    def __str__(self):
        return u"[%s][User: %s][Rule: %s] %s: %s" % (self.timestamp, self.user, self.rule, self.type_rule, self.text)
