from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Admin is necessary for Django Task Scheduler
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

    # Necessary for Django Task Scheduler
    (r'^scheduler/', include('scheduler.urls')),
    
)
