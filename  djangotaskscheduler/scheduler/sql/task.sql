LOCK TABLES `scheduler_task` WRITE;

INSERT INTO `scheduler_task`
    VALUES  (1,'Example task two','test2','Example task two kicks off test2.py',4,'2008-05-01 00:02:00',1),
            (2,'Example task one','test1','Example task 1, kicks off test1.py',2,'2008-05-01 00:00:00',1),
            (3,'Purge Scheduler','purge_scheduler','Purge completed scheduler rows',6,'2008-06-09 21:00:00',1);

UNLOCK TABLES;
