import os
from optparse import OptionParser
import fileinput


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



thistask = Schedule(id = options.instance_id)
thistask.start_task()

file1 = thistask.createFile('file1.txt')
file2 = thistask.createFile('file2.txt')

try:
    f1 = open(file1, "w")
    f2 = open(file2, "w")
    s = 0

    thistask.set_message('Processing')
    for a in range(25):
        #time.sleep(1)
        f1.write(str(a)+"\n")
        thistask.add_log_message('progress '+str(a))
        print 'progress '+str(a)
        s += a
    thistask.add_log_message('ended '+str(s))
    thistask.set_message('Completed')

    f2.write(str(a)+"\n")

    f1.close()
    f2.close()

    thistask.closeFile(file1)
    thistask.closeFile(file2)

except:
    thistask = Schedule(id = options.instance_id)
    thistask.failed_task()

thistask.end_task()
