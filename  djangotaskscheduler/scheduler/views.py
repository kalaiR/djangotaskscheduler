from schedulerdemo.scheduler.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from django import newforms as forms
from django.newforms.util import ValidationError
from django.newforms import widgets
import calendar, datetime


class NewScheduleForm(forms.Form):
    task = forms.ChoiceField()


def add_schedule(request):

   # --- Cancel
    if request.POST.getlist('_cancel'):
        return HttpResponseRedirect("/admin/scheduler")

    # --- Save
    if request.POST.getlist('_save'):
        tid = int(request.POST.getlist('task')[0])
        if tid <> 0:
            newtask = Schedule(task_id = tid).create()

        return HttpResponseRedirect("/admin/scheduler")

    # --- Build the page
    tl = Task.objects.filter().order_by('description')
    tasklst = []
    tasklst.append((0,'-Select one-'))
    for t in tl:
        ti = (t.id, t.description+' ('+t.recurrence.description+')')
        tasklst.append(ti)

    form = NewScheduleForm()
    form.base_fields['task'].choices = tasklst

    # Setup template and context
    t = loader.get_template('scheduler/add_schedule.html')
    c = Context({'form': form,
                })

    return HttpResponse(t.render(c))



def show_scheduler(request):

    if request.POST.getlist('_schedule'):
        return HttpResponseRedirect("/schedule/add")

    scheduled_set = Schedule.objects.filter(status__in=(1,2)).order_by('-scheduled_dt')
    completed_set = Schedule.objects.filter(status__in=(3,4,5)).order_by('-start_dt')[0:15]

    # Setup template and context
    t = loader.get_template('scheduler/scheduler.html')
    c = Context({'scheduled_set': scheduled_set,
                 'completed_set': completed_set,
                })

    return HttpResponse(t.render(c))



ACTION_TYPES = (
    (0,'----------'),
    (1,'Run now'),
    (2,'Reschedule'),
    (3,'Cancel'),
    (4,'Delete'),
)


class EditScheduleForm(forms.Form):
    action  = forms.ChoiceField(choices = ACTION_TYPES)


def edit_schedule(request, schedule_id):

    schedule = Schedule.objects.get(pk = schedule_id)

    # --- Cancel
    if request.POST.getlist('_cancel'):
        return HttpResponseRedirect("/admin/scheduler")

    # --- Save
    if request.POST.getlist('_save'):
        thistask = Schedule(pk = schedule_id)
        action = int(request.POST.getlist('action')[0])
        if action == 1:   # Run Now
            thistask.runnow()
        elif action == 2: # Reschedule
            thistask.reschedule()
        elif action == 3: # Cancel
            thistask.cancel()
        elif action == 4: # Delete
            thistask.delete()
        return HttpResponseRedirect("/admin/scheduler")

    # Setup form
    form = EditScheduleForm()

    # Get file data
    files = File.objects.filter(schedule = schedule_id).order_by('id')

    # Get log
    log = Log.objects.filter(schedule = schedule_id).order_by('id')

    # Setup template and context
    t = loader.get_template('scheduler/edit_schedule.html')
    c = Context({'schedule': schedule,
                 'form': form,
                 'files': files,
                 'log': log,
                })

    return HttpResponse(t.render(c))
