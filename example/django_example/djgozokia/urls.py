from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from djgozokia.views import GozokiaChatView
urlpatterns = patterns('',
                       # Redirect old urls to new one
                       #url(r'^partials/$', TemplateView.as_view(template_name="bookings/menu.html"), name='booking_partials_'),
                       url(r'^api$', 'djgozokia.views.api', name='gozokia-chat-api'),
                       url(r'^$', GozokiaChatView.as_view(), name='gozokia-chat'),

                       )
