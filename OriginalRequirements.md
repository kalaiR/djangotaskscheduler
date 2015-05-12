# Django Task Scheduler Requirements #
June 21, 2008

## 1. Business Requirements ##
The Django Task Scheduler should provide the site administrators the ability to manage functions to be run a schedule to do some housekeeping tasks or reporting from Django.
The tasks, recurrence schedule and scheduled/completed tasks are managed from the web frontend (Django Task Scheduler).
A task should be able to write to an output file which can be retrieved through the web user interface as a download.


## 2. Functional Specifications ##
The Django task scheduler should cover the following functional aspects:

  * Multiple tasks can be scheduled to run
  * Tasks can be scheduled for a single run at a specific time (immediate or later), or follow a recurrence schedule
  * A manual one-time task can be created to be run next time the master scheduler sees it (run 'now') or the user can enter a date/time on which the one-time program is to run.
  * When a recurrence schedule is used, after a successful completion of the task the next run is scheduled automatically
  * The recurrence schedule should be able to schedule with the following options:
> > o immediate (this would mean that the task is kicked off next time the master scheduler runs, I am not sure if this is the best option for a recurring program, however, it would be the default option for a manually scheduled/kicked off task)
> > o every X minutes (from 1 to 59 minutes)
> > o every X hours (from 1 to 23 hours)
> > o every X days (from 1 to 30 days)
> > o every X weeks (from 1 to 51 weeks)
> > o every month
> > o every year
  * Similar scheduled tasks will not run concurrently. Example. A task is defined for Python function Foobar. Scheduled task Foobar has a recurrence schedule of 5 minutes. If Foobar is kicked off at 8.00am and runs for 8 minutes, the next instance of Foobar is kicked off at 8.10am (skipping the 8.05am potential).
  * Different scheduled tasks will be able to run concurrently
  * A task is a python program (or function) that is called from the scheduler. The scheduler program should follow a small set of rules:
    1. The task programs returns success or failure to the scheduler.
> > 2. The task programs can utilize Django objects
> > 3. The task program has access to an instance id. This is unique across all scheduled tasks and can be used to write-out files (pdf, text, and whatelsenot)
> > 4. Function Parameters are not passed on to the python program or function. If there is a need for parameters, the parameters should be set in a separate table that can be maintained from the developers user interface. This specific task parameter table is read by the task program/function.
  * A task on a recurring schedule will stop its reschedule after a failure
  * A heartbeat is created in the form of a CRON task. This kicks of the master scheduler which checks if any programs that are not running and are not completed but are (past)due to be run. This way we only have to set one single CRON task for the master scheduler. All other tasks are managed through the Django Process Scheduler.
  * The master scheduler should be a very light program to reduce impact on overall system resources. This is especially important when the master scheduler will run every minute or so. This program will run most of the time without any real work.
  * When a task completes, it goes back into the master scheduler which reschedules the next occurence of the task if the task is on a recurrence schedule.
  * The Django Process Scheduler uses security profiles from the Django Admin Module.


Some implications exist for this approach:

  * The frequency of the CRON task determines how often the scheduled tasks are checked and kicked off. This has implications for the expectations when something will run. If the CRON task runs every hour, but the user scheduled something for every 15 minutes, it would effectively run every hour. This becomes even more apparent when you kick something of to run immediately (especially since the master scheduler wont run for the next hour). To the best effect the master scheduler should check for work every minute.


## 3. Technical Design ##
## 3.1 Master Scheduler program (heartbeat) ##
### 3.1.1 Start heartbeat program ###
Can be scheduled from CRON or run manually from the command line.
Run options:
  * run\_once
  * run\_permanently
  * run\_for=<runtime in minutes>

Using these run options you can kick of the scheduler from the command line to run forever (when CRON is not available, i.e. Windows). You can kick it of everytime CRON kicks it off (say, every 15 minutes) or you can schedule it to run for x amount of minutes everytime CRON kicks it off.

Need to be careful to what happens if the heartbeat program is kicked off in parallel (multiple instances).
3.1.2 Outline of the heartbeat program
The heartbeat program will do the following:

  1. Loop through the scheduled tasks that are pending and have a run datetime that is less than the current datetime.

> 2. Change status of the selected task to 'running'
> 3. Kick off the python program


### 3.1.3 Calculate the next scheduled datetime ###
To calculate the next runtime we can use the function shown below. It will calculate the next instance based on the start datetime (original start dt) and its interval in minutes. This code will be run after the scheduled program completes and it is a recurring program. Next run date time is written in the new scheduled instance.

```
from math import ceil
from datetime import *
import time

def next_runtime(start_dt, recurrence):
    # Start_dt is a datetime object
    # Recurrence is the recurrence in minutes (integer)
    # Returns the next datetime base on start_dt and recurrence
    
    current_dt = datetime.now()
    ss = time.mktime(start_dt.timetuple())
    cs = time.mktime(current_dt.timetuple())
    rs = recurrence * 60
    nt = time.localtime(ss+(ceil((cs-ss)/rs)*rs))
    next_dt = datetime(nt.tm_year,
                       nt.tm_mon,
                       nt.tm_mday,
                       nt.tm_hour,
                       nt.tm_min,
                       nt.tm_sec)
    return next_dt

print next_runtime(start_dt=datetime(2008, 2, 2, 10, 5), recurrence=15)
```


## 3.2 Data Model ##
The data model consists of the following tables:

  * scheduler\_taskdefn
> > o task id (primary key)
> > o description
> > o python program and function
> > > + Points to the Python program/function. There are no parameters to be passed to this function. If parameters are necessary, the developer should create a table with parameters that can be maintained and read from the scheduled program.

> > o recurrence
> > o start\_datetime
> > > + This is used for calulation of when the program runs. If the start\_datetime is '01012008 20:02' and the recurrence is every 15 minutes. This program will be scheduled for every 15 minutes from this datetime (20:17, 20:32, 20:47, ..., 05:17 etc).
  * scheduler\_recurrencedefn (this is not a database table, this is contained within the Python program).

> > o recurrence\_id
> > o description
> > > + example: Every 15 minutes

> > o interval\_a
> > > + example: 15

> > o interval\_b
> > > + example: 1 (which means minutes)
        1. 1: minutes
        1. 2: hours
        1. 3: days
  * scheduler\_schedule

> > o instance id (primary key on the table, auto number)
> > o scheduled\_datetime
> > o task (foreign key)
> > o status [pending, running, completed, failed, cancelled]
> > o start\_datetime
> > o end\_datetime
  * scheduler\_file
> > o id (primary key)
> > o instance\_id
> > o file reference
  * scheduler\_log
> > o id (primary key)
> > o instance\_id
> > o datetime\_stamp
> > o log\_message


## 3.3 Scheduler User Interface ##
The scheduler userin interface will give the user the following information and actions:

  * A list of the pending tasks and is scheduled run time
  * A list of the recently completed tasks and its actual runtime and main feedback text.
  * A way to drill deeper into the run tasks details.
  * A way to schedule a new task.


The task details page will give the user the following information and actions:

  * Details on the actual program start and end times.
  * Provides access to the program's run log.
  * Provide access to the files generated in during this task.



## 3.4 Task function skeleton ##
Each task needs to follow a predetermined code skeleton. The functions called from this skeleton provides feedback to the scheduler on the progress of the program. The skeleton is Python based. If non python programs need to be run from the scheduler, a python wrapper should be written to start the non-python program and keep the scheduler informed on its progress.

Code skeleton:
<to be completed>


## 3.5 Capturing task output ##
The task has a function to request a new file using a filename. This will return a full path to the task program where the file can be created.
At the end of the run, the program tells the scheduler that the file is completed. Alternatively this is done by the overall task completefunction.


## 3.5 File output ##
Each task should be able to create as many files as necessary. The files are outputted to a file location by the scheduler. This generally should direct it to a file location like:

  * 

<output\_file\_path>

/

<instance\_id>

/[<optional secondary filepath>/]

&lt;filename&gt;


  * /var/djangoschedulerfiles/1179/file1.txt
  * /var/djangoschedulerfiles/1179/file2.pdf


If enabled in the settings file, the user should be able to download the files from the browser (if the user is an administrator or if the user is the owner of the task (this is determined by a settings parameter)). Nevertheless, download security should be provided by the webserver serving these files. Afterall, any person could try to download the output by pointing their browser to http://mysite/media/1179/file2.pdf by guessing.