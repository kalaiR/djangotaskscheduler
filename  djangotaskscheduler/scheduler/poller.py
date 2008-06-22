from django.conf import settings
from django.core.management import setup_environ
import settings
setup_environ(settings)
from optparse import OptionParser
from django.db import connection
import thread, os, time


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
    cursor.execute("SELECT s.id, t.program                                  \
                    FROM scheduler_schedule s,                              \
                         scheduler_task t                                    \
                    WHERE s.scheduled_dt <= CURRENT_TIMESTAMP               \
                    AND s.task_id = t.id                                     \
                    AND s.status = 1")

    job_set = cursor.fetchall()
    if job_set == ():
        print 'Nothing to do'
    else:
        for job in job_set:
            instance = job[0]
            python   = 'python '
            jobdescr = job[1]
            program  = 'scheduler/tasks/' + jobdescr + '.py '
            args     =  '-i ' + str(instance)
            print 'Starting program', jobdescr, 'as instance', instance
            thread.start_new_thread(os.system,(python+program+args,))

    if options.repeat == None:
        end = True
    else:
        time.sleep(options.repeat)
