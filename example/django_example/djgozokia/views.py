# -*- coding: utf-8 -*-
import os
import sys
from django.http import HttpResponse
from gozokia import Gozokia
# First, declare our settings file:
os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "django_example.settings")


def index(request):
        # Initialize
    goz = Gozokia()
    goz.initialize()
    return HttpResponse(goz.api(request.GET.get('input')))
