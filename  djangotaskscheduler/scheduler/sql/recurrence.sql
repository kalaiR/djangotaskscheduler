LOCK TABLES `scheduler_recurrence` WRITE;

INSERT INTO `scheduler_recurrence`
    VALUES  (1,'Every 5 minutes',5,1),
            (2,'Every 30 minutes',30,1),
            (3,'Once',0,0),
            (4,'Every 15 minutes',15,1),
            (5,'Every 1 hour',1,2),
            (6,'Every week',1,4);

UNLOCK TABLES;
