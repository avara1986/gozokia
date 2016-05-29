# -*- coding: utf-8 -*-
import os
import sys
from django.http import HttpResponse
from gozokia import Gozokia
from djgozokia.rules import GreetingRaise, GreetingObjetive, Whoami
# First, declare our settings file:
os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "django_example.settings")


def index(request):
    # Initialize
    if request.user.is_authenticated():
        goz = Gozokia(user=request.user.id, session=request.session.session_key)
        #goz.rule(name='greeting', type=goz.OBJETIVE_COND, rank=100)(GreetingObjetive)
        goz.rule(name='greeting', type=goz.RAISE_COND, rank=100)(GreetingRaise)
        goz.rule(name='whoami', type=goz.RAISE_COND, rank=1)(Whoami)
        goz.initialize()
        return HttpResponse("SESSION: {}. RESPONSE: {}".format(request.session.session_key, goz.api(request.GET.get('input'))))
    else:
        return HttpResponse("No login")
