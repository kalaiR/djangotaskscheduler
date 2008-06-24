# Django Task Scheduler - settings


# Python location
PYTHON_APP                  = '/usr/bin/env python'

# Tasks file location
SCHEDULER_TASK_ROOT         = 'scheduler.tasks'

SCHEDULER_FILE_ROOT         = '/var/scheduler'
SCHEDULER_FILE_WEBROOT      = 'file://'

# Allow downloads of generated files
#   True:  Files in the scheduler details page are clickable,
#          hyperlink created using SCHEDULER_FILE_WEBROOT
#   False: Filename are shown in the scheduler, no hyperlink provided
SCHEDULER_FILE_DOWNLOADS    = True
