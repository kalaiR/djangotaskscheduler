### DjangoTaskScheduler ###
This Django project provides an extension to the excellent Django Admin interface from which a system administrator can start and manage scheduled tasks.

Tasks are defined as Python programs that can utilize the Django models for the main application. The tasks need to interact with the task scheduler to report its status and request file locations for its output files. Example task programs are provided with the source code.

Non python programs can be kicked of from a python wrapper that follows the task scheduler conventions.

![http://djangotaskscheduler.googlecode.com/files/screenshot.png](http://djangotaskscheduler.googlecode.com/files/screenshot.png)


### The code ###
The code that you can obtain through the source tab contains a full Django application.
The application consists of two Django apps:
  1. demo
  1. scheduler

the demo app is empty and does nothing.
After installing and starting the webserver, pointing your webbrowser to http://localhost:8000 will not show anything. This starts the demo app which is empty.

The scheduler has another url: point the browser to http://localhost:8000/scheduler and you end up in the main scheduler page. From here you can schedule a new task, refresh the page or go into details on the scheduled or completed tasks.

Each task can have one of many statuses (queued, processing, completed or failed). As each task is run the status is shown in the main scheduler page. Each task can provide custom status messages (in example a progress message) that shows on the main page.

Each task can create output files. These are created and kept in a predefined place. If you spend some extra time setting up a secure webserver, an administrator can download the outputfiles right from the task details page.

A poller program is provided that

### The status ###
The status of this project is that it is under development. The main functionality is available in the current code. However, some additional code has to be completed. SOme outstanding tasks on the todo list are:
  * Include security for the scheduler. Typically normal visitors to the website have no reason to view/manage the scheduler.
  * Include instructions for setting up a file server to serve the output files in a secure manor.
  * Include a more robust way of tracking whether the task program is still running or failed.
  * ~~Switch from old-style admin to newforms admin for new task definitions and recurrences~~

