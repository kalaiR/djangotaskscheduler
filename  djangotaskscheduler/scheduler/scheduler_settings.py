# Django Task Scheduler - settings


# Python location
# Linux
#PYTHON_APP                  = '/usr/bin/env python'
# Windows
PYTHON_APP                  = 'python.exe'

# Tasks file location
SCHEDULER_TASK_ROOT         = 'scheduler.tasks'

# Allow downloads of generated files
# Linux
#SCHEDULER_FILE_ROOT         = '/var/scheduler'
# Windows
SCHEDULER_FILE_ROOT         = 'C:\django-scheduler'

SCHEDULER_FILE_DOWNLOADS    = True
