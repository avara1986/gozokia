from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from djgozokia.models import GozokiaChat


class GozokiaChatAdmin(admin.ModelAdmin):
    pass

admin.site.register(GozokiaChat, GozokiaChatAdmin)
