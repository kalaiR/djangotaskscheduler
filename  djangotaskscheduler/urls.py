from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^schedulerdemo/', include('schedulerdemo.foo.urls')),

    # Admin is necessary for Django Task Scheduler
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

    # Necessary for Django Task Scheduler
    (r'^schedule/add/', 'schedulerdemo.scheduler.views.add_schedule'),
    (r'^schedule/(?P<schedule_id>\d+)/$', 'schedulerdemo.scheduler.views.edit_schedule'),
    (r'^admin/', include('schedulerdemo.scheduler.urls')),

)
