from django.conf.urls.defaults import *
from scheduler.models import scheduler_admin_site
from django.contrib import admin

urlpatterns = patterns('scheduler.views',
    (r'^$', 'show_scheduler'),
    (r'^detail/(?P<schedule_id>\d+)/$', 'edit_schedule'),
    (r'^create/$', 'add_schedule'),
    (r'^admin/(.*)', scheduler_admin_site.root),
)
