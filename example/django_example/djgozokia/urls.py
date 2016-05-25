from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
                       # Redirect old urls to new one
                       #url(r'^partials/$', TemplateView.as_view(template_name="bookings/menu.html"), name='booking_partials_'),
                       url(r'^$', 'djgozokia.views.index', name='gozokia-api-index'),
                       )
