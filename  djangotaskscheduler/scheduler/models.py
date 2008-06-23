from django.db import models
from django.contrib.auth.models import User
from django.db import connection
from math import ceil
from datetime import *
import time
import os
from scheduler.scheduler_settings import *



INTERVAL_TYPES = {
    1: ('minutes', 60),
    2: ('hours', 3600),
    3: ('days', 86400),
    4: ('weeks', 604800),
}


STATUS_TYPES = {
    1: 'Queued',
    2: 'Processing',
    3: 'Failed',
    4: 'Completed',
    5: 'Cancelled',
}


class Recurrence(models.Model):
    description     = models.CharField("Description", max_length=50)
    interval        = models.IntegerField(default = 15)
    interval_type   = models.IntegerField(default = 1)


    def next_runtime(self, start_dt):
        current_dt = datetime.now()

        m = INTERVAL_TYPES[self.interval_type][1]

        if self.interval > 0 or start_dt == None:
            current_dt = datetime.now()
            ss = time.mktime(start_dt.timetuple())
            cs = time.mktime(current_dt.timetuple())
            rs = self.interval * m
            nt = time.localtime(ss+(ceil((cs-ss)/rs)*rs))
            next_dt = datetime(nt.tm_year,
                               nt.tm_mon,
                               nt.tm_mday,
                               nt.tm_hour,
                               nt.tm_min,
                               nt.tm_sec)
            return next_dt
        else:
            return start_dt


    def __unicode__(self):
        return self.description


    class Admin:
        list_display = (['description'])
        list_filter = (['description'])
        pass



class Task(models.Model):
    description     = models.CharField("Description", max_length=50)
    program         = models.CharField("Program", max_length=50)
    longdescription = models.CharField("Long description", max_length=250)
    recurrence      = models.ForeignKey(Recurrence)
    start_datetime  = models.DateTimeField("Start date and time")
    user            = models.ForeignKey(User)


    def __unicode__(self):
        return "Task: " + str(self.id)


    class Admin:
        list_display = ('description',
                        'user',
                        'program',
                        'longdescription',
                        'recurrence',)
        list_filter = ('description',
                       'user')
        pass



class Schedule(models.Model):
    task            = models.ForeignKey(Task)
    scheduled_dt    = models.DateTimeField("Scheduled date and time")
    start_dt        = models.DateTimeField("Start date and time", null=True)
    end_dt          = models.DateTimeField("End date and time", null=True)
    status          = models.IntegerField(default = 1)
    message         = models.CharField("Message", max_length=200)


    def status_descr(self):
        "Return a sensible text describing the status"
        return STATUS_TYPES[self.status]


    def start_task(self):
        "Show the current running task as started"
        try:
            s = Schedule.objects.get(id = self.id, status = 1)
            s.status = 2
            s.start_dt = datetime.now()
            s.save()
            s.add_log_message("Task start.")
        except self.DoesNotExist:
            print "Unable to mark task with instance",self.id,"as started"


    def failed_task(self):
        "Mark the current running task as failed"
        try:
            s = Schedule.objects.get(id = self.id, status = 2)
            s.status = 3
            s.end_dt = datetime.now()
            s.save()
            s.add_log_message("Task failed.")
        except self.DoesNotExist:
            print "Unable to mark task with instance",self.id,"as failed"


    def end_task(self):
        "Finish up the current running task"
        try:
            s = Schedule.objects.get(id = self.id, status = 2)
            s.status = 4
            s.end_dt = datetime.now()
            s.save()
            s.add_log_message("Task ended successfully.")
            # If recurring task, reschedule
            t = Task.objects.get(id = s.task_id)
            r = Recurrence.objects.get(id = t.recurrence_id)
            if r.interval_type <> 0:
                new_datetime = r.next_runtime(s.scheduled_dt)
                newtask = Schedule(task_id = s.task_id, scheduled_dt = new_datetime, status = 1)
                newtask.save()
        except s.DoesNotExist:
            print "Unable to mark task with instance",self.id,"as ended"


    def set_message(self, message):
        "Set a message for the current running task"
        try:
            s = Schedule.objects.get(id = self.id, status = 2)
            s.message = message
            s.save()
        except self.DoesNotExist:
            print "Unable to set message for instance",self.id


    def add_log_message(self, message):
        "Add a message to this tasks log."
        try:
            l = Log.objects.create(schedule = self,
                                    log = message,
                                    timestamp_dttm = datetime.now()
                                    )
            l.save()
        except self.DoesNotExist:
            print "Unable to set a message to the log for instance",self.id


    def createFile(self, filename):
        "Return a filename to use as an export file for the task program."
        f = File.objects.create(schedule = self, filename = filename)
        f.save()
        self.add_log_message("File created: "+filename)
        return f.createFile()


    def closeFile(self, filename):
        "Close the attached file."
        f = File.objects.get(schedule = self, filename = filename[filename.rfind('/')+1:])
        f.closeFile()
        self.add_log_message("File closed: "+filename)


    def numberFiles(self):
        "Return the number of files created for the scheduled task"
        return len(File.objects.filter(schedule = self))


    def runnow(self):
        "Set the run time for start when the scheduler awakes.  \
         Please note that the status of the task instance must  \
         be 'queued'. "
        try:
            s = Schedule.objects.get(id = self.id, status = 1)
            s.scheduled_dt = datetime.now()
            s.save()
        except self.DoesNotExist:
            print "Unable to update the scheduled date for instance",self.id


    def reschedule(self):
        "Set the run time for start when the scheduler awakes   \
         to rerun this program after it had failed.             \
         Please note that the status of the task instance must  \
         be 'failed', 'completed' or 'cancelled'. "
        try:
            s = Schedule.objects.get(id = self.id, status__in = (3,4,5))
            t = Task.objects.get(id = s.task_id)
            r = Recurrence.objects.get(id = t.recurrence_id)
            if r.interval_type <> 0:
                new_datetime = r.next_runtime(s.scheduled_dt)
                newtask = Schedule(task_id = s.task_id, scheduled_dt = new_datetime, status = 1)
                newtask.save()
            else:
                newtask = Schedule(task_id = s.task_id, scheduled_dt = datetime.now(), status = 1)
                newtask.save()
        except self.DoesNotExist:
            print "Unable to update the scheduled date for instance",self.id


    def create(self):
        "Schedule a new task identified by the provided task_id."
        try:
            t = Task.objects.get(pk = self.task_id)
            self.scheduled_dt = t.start_datetime
            self.save()
        except self.DoesNotExist:
            print 'Unable to schedule a new task.'

    def cancel(self):
        "Cancel this task that was scheduled.                       \
         Please note that the status of the task instance must      \
         be 'scheduled' or 'processing'. Note that this does cancel \
         the task from the scheduler tables, however, it does not   \
         cancel the actual program running. "
        try:
            s = Schedule.objects.get(id = self.id, status__in = (1,2))
            s.status = 5
            s.start_dt = datetime.now()
            s.save()
        except self.DoesNotExist:
            print "Unable to cancel the scheduled task for instance",self.id


    def delete(self):
        "Delete this task and its related files.                \
         the task must be 'failed', 'cancelled', or 'completed'."
        try:
            s = Schedule.objects.get(id = self.id, status__in = (3,4,5))
            files = File.objects.filter(schedule = s)
            for f in files:
                file = f.file()
                print 'remove file:', file
                #os.remove(file)
                #os.rmdir()
            super(Schedule, s).delete()
        except self.DoesNotExist:
            print "Unable to delete the task for instance",self.id


    def __unicode__(self):
        return "Schedule: " + str(self.id)



class Log(models.Model):
    schedule        = models.ForeignKey(Schedule)
    log             = models.CharField("Log line", max_length=250)
    timestamp_dttm  = models.DateTimeField()


    def __unicode__(self):
        return "Log: " + str(self.id) + " - " + str(self.schedule_id)



class File(models.Model):
    schedule        = models.ForeignKey(Schedule)
    filename        = models.CharField("File name", max_length=50)
    filepath        = models.CharField("File path", max_length=250)
    filesize        = models.IntegerField(default = 0)


    def file(self):
        return os.path.join(self.filepath, self.filename)


    def createFile(self):
        dir = SCHEDULER_FILE_ROOT+'/'+str(self.schedule_id)
        try:
            os.makedirs(dir, 0777)
        except OSError:
            print 'Directory exists. ('+ dir +')'
        self.filepath = dir
        self.save()
        return self.file()


    def closeFile(self):
        self.filesize = os.stat(self.file()).st_size
        self.save()


    def __unicode__(self):
        return "File: " + str(self.id)
