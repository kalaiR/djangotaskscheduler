from django.conf import settings
from django.core.management import setup_environ
import settings
setup_environ(settings)
from optparse import OptionParser
from django.db import connection
from scheduler.models import Schedule
from datetime import *
import thread, os, time
from scheduler.scheduler_settings import PYTHON_APP


#   --------------------------------------------------------------------
#   --- The following in necessary if you want to run this from CRON ---
#   --------------------------------------------------------------------
#
#   PYTHONPATH=<path to schedulerdemo>/schedulerdemo
#   DJANGO_SETTINGS_MODULE=schedulerdemo
#
#   # m h  dom mon dow   command
#     * *  *   *   *     cd <path to schedulerdemo>/schedulerdemo; ! /usr/bin/env python $
#


usage = "usage: %prog -r SECONDS| --repeat=SECONDS"
parser = OptionParser(usage)
parser.add_option('-r', '--repeat', dest='repeat', metavar='SECONDS',
                  help="Repeat poller program every specified seconds")
(options, args) = parser.parse_args()

if options.repeat:
    options.repeat = int(options.repeat)


cursor = connection.cursor()
end = False

while end == False:
    tasks = Schedule.objects.filter(status__exact=1, scheduled_dt__lte=datetime.now())
    if len(tasks) == 0:
        print datetime.now(), ': Nothing to do'
    else:
        for task in tasks:
            thistask    = Schedule(pk = task.id)
            python      = PYTHON_APP + ' '
            taskdescr   = task.task.program
            program     = 'scheduler/tasks/' + taskdescr + '.py '
            stdoutfile  = thistask.createFile('stdout.txt')
            args        =  '-i ' + str(task.id) + ' > ' + stdoutfile
            print datetime.now(), ': Starting program', taskdescr, 'as instance', task.id
            thread.start_new_thread(os.system,(python+program+args,))

    if options.repeat == None:
        end = True
    else:
        time.sleep(options.repeat)
