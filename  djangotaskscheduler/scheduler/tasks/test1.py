import os
from optparse import OptionParser

usage = "usage: %prog -i INSTANCE_ID| --instance=INSTANCE_ID"
parser = OptionParser(usage)
parser.add_option('-i', '--instance', dest='instance_id', metavar='INSTANCE_ID',
                  help="Maintenance job test1")
(options, args) = parser.parse_args()
if not options.instance_id:
    parser.error("You must specify an instance")


from django.core.management import setup_environ
import settings
setup_environ(settings)
from django.db import connection
import time
from scheduler.models import *


thistask = Schedule(pk = options.instance_id)
thistask.start_task()

try:
    for i in range(100):
        time.sleep(1)
        thistask.set_message('Completed '+str(i)+'%')

except:
    thistask = Schedule(id = options.instance_id)
    thistask.failed_task()

thistask.set_message('Completed')
thistask.end_task()
