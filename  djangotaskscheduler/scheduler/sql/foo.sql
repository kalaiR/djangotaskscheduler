-- MySQL dump 10.11
--
-- Host: localhost    Database: docudeck
-- ------------------------------------------------------
-- Server version	5.0.51a-3ubuntu5.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `scheduler_recurrence`
--

DROP TABLE IF EXISTS `scheduler_recurrence`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `scheduler_recurrence` (
  `id` int(11) NOT NULL auto_increment,
  `description` varchar(50) NOT NULL,
  `interval` int(11) NOT NULL,
  `interval_type` int(11) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `scheduler_recurrence`
--

LOCK TABLES `scheduler_recurrence` WRITE;
/*!40000 ALTER TABLE `scheduler_recurrence` DISABLE KEYS */;
INSERT INTO `scheduler_recurrence` VALUES (1,'Every 5 minutes',5,1),(2,'Every 30 minutes',30,1),(3,'Once',0,0),(4,'Every 15 minutes',15,1),(5,'Every 1 hour',1,2),(6,'Every week',1,4);
/*!40000 ALTER TABLE `scheduler_recurrence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scheduler_job`
--

DROP TABLE IF EXISTS `scheduler_job`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `scheduler_job` (
  `id` int(11) NOT NULL auto_increment,
  `description` varchar(50) NOT NULL,
  `program` varchar(50) NOT NULL,
  `longdescription` varchar(250) NOT NULL,
  `recurrence_id` int(11) NOT NULL,
  `start_datetime` datetime NOT NULL,
  `user_id` int(11) NOT NULL default '1',
  PRIMARY KEY  (`id`),
  KEY `scheduler_job_recurrence_id` (`recurrence_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `scheduler_job`
--

LOCK TABLES `scheduler_job` WRITE;
/*!40000 ALTER TABLE `scheduler_job` DISABLE KEYS */;
INSERT INTO `scheduler_job` VALUES (1,'Example task two','test2','Example task two kicks off test2.py',4,'2008-05-01 00:02:00',1),(2,'Example task one','test1','Example task 1, kicks off test1.py',2,'2008-05-01 00:00:00',1),(3,'Tag Cleanup','tag_cleanup','Tag cleanup program',5,'2008-05-05 00:00:00',1),(4,'Purge Scheduler','purge_scheduler','Purge completed scheduler rows',6,'2008-06-09 21:00:00',1),(5,'List tasks','test3','Output tasks found in the system to a file.',3,'2008-06-17 22:00:00',1);
/*!40000 ALTER TABLE `scheduler_job` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2008-06-22  7:40:06
