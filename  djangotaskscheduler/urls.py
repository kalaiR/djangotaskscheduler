from django.conf.urls.defaults import *
from django.contrib import admin

urlpatterns = patterns('',
    # Admin is necessary for Django Task Scheduler
    (r'^admin/(.*)', admin.site.root),

    # Necessary for Django Task Scheduler
    (r'^scheduler/', include('scheduler.urls')),
    
)
