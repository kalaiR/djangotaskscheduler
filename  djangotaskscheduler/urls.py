from django.conf.urls.defaults import *

urlpatterns = patterns('',


    # Necessary for Django Task Scheduler
    (r'^scheduler/', include('scheduler.urls')),    
)
