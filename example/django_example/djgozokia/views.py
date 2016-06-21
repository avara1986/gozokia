# -*- coding: utf-8 -*-
import os
import sys

from gozokia import Gozokia

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from djgozokia.models import GozokiaChat
from djgozokia.rules import GreetingRaise, GreetingObjetive, Whoami

# First, declare our settings file:
os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "app.settings")


class GozokiaChatView(View):
    template_name = "djgozokia/index.html"

    def get(self, request, *args, **kwargs):
        # Initialize
        if request.user.is_authenticated():
            goz = Gozokia(user=request.user.id, session=request.session.session_key)

            goz.rule(name='greeting', type=goz.RAISE_COND, rank=100)(GreetingRaise)
            goz.rule(name='whoami', type=goz.RAISE_COND, rank=1)(Whoami)
            goz.initialize(model=GozokiaChat)

            return render(request, self.template_name, {'input': request.GET.get('input'),
                                                        'session': request.session.session_key,
                                                        'output': goz.api(request.GET.get('input')),
                                                        })
        else:
            return HttpResponse("No login")


def api(request):
    # Initialize
    if request.user.is_authenticated():
        goz = Gozokia(user=request.user.id, session=request.session.session_key)
        # goz.rule(name='greeting', type=goz.OBJETIVE_COND, rank=100)(GreetingObjetive)
        goz.rule(name='greeting', type=goz.RAISE_COND, rank=100)(GreetingRaise)
        goz.rule(name='whoami', type=goz.RAISE_COND, rank=1)(Whoami)
        goz.initialize(model=GozokiaChat)

        return JsonResponse({'input': request.GET.get('input'),
                             'session': request.session.session_key,
                             'output': goz.api(request.GET.get('input')),
                             })
    else:
        return HttpResponse("No login")
