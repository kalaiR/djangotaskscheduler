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
from datetime import *
from scheduler.models import *
import time


thistask = Schedule(id = options.instance_id)
thistask.start_task()

try:
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM scheduler_schedule   \
                    WHERE status = 4 AND scheduled_dt < date(%s)",
                    [datetime.now()-timedelta(14)])
    result_set = cursor.fetchone()
    num_del = result_set[0]
    cursor.execute("DELETE FROM scheduler_schedule   \
                    WHERE status = 4 AND scheduled_dt < date(%s)",
                    [datetime.now()-timedelta(14)])
    thistask.set_message('Deleted '+str(num_del)+' old schedule rows.')
    cursor.execute("optimize table scheduler_schedule")
except:
    thistask.failed_task()

thistask.end_task()
