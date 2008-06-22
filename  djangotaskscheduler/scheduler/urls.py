from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^scheduler/$', 'schedulerdemo.scheduler.views.show_scheduler'),
    (r'^schedule/(?P<schedule_id>\d+)/$', 'schedulerdemo.scheduler.views.show_scheduler'),
)
