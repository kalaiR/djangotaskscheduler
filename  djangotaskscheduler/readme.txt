=Instructions=

===Get the source code===
Create a directory in which the schedulerdemo is being downloaded

	mkdir djangotaskscheduler

Get the djangotaskscheduler using subversion


===Create the database===
Create a database schema. The schemaname and userids as defined in the settings file are:
	DATABASE_ENGINE = 'mysql'
	DATABASE_NAME = 'schedulerdemo'
	DATABASE_USER = 'django'       
	DATABASE_PASSWORD = 'django'   
if your database properties are different, adjust accordingly in the settings.py file.


===Update the HTML templates location===
Update your templates location to match your installation location.
See TEMPLATE_DIRS in the settings.py file.


===Update the output file location===
Create the directory where the output files are written.
The standard location is /var/scheduler and the userid running the poller.py program should have read/write access to that directory.
This is set in the scheduler/scheduler_settings.py file.


===Update the poller script===
The poller script is called run_poller. Update this to match your environment.
Alternatively kick the poller.py program using cron. See poller.py for instructions.


===Start the application and run the poller===
Start the application using 
	python manage.py runserver
Start the poller using 
	./run_poller


