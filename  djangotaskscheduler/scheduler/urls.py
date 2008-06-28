from django.conf.urls.defaults import *

urlpatterns = patterns('scheduler.views',
    (r'^$', 'show_scheduler'),
    (r'^detail/(?P<schedule_id>\d+)/$', 'edit_schedule'),
    (r'^create/$', 'add_schedule'),
)
