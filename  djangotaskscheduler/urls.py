from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^schedulerdemo/', include('schedulerdemo.foo.urls')),

    # Admin is necessary for Django Task Scheduler
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

    # Necessary for Django Task Scheduler
    (r'^scheduler/', include('schedulerdemo.scheduler.urls')),
    
)
