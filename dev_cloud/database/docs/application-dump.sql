-- MySQL dump 10.13  Distrib 5.6.19, for linux-glibc2.5 (x86_64)
--
-- Host: 192.245.169.169     Database: Dev_Cloud_db
-- ------------------------------------------------------
-- Server version	5.5.49-MariaDB-1ubuntu0.14.04.1

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
-- Dumping data for table `Applications`
--

LOCK TABLES `Applications` WRITE;
/*!40000 ALTER TABLE `Applications` DISABLE KEYS */;
INSERT INTO `Applications` VALUES (1,'mysql','',2048,1300,2,'2015-02-20 23:01:11','juju deploy mysql'),(2,'tomcat','',1024,500,1,'2015-02-23 10:31:45','juju deploy tomcat'),(3,'juju-gui','Web GUI for Juju',8192,8000,6,'2016-06-29 14:14:25','juju deploy juju-gui'),(4,'memcached','',256,500,1,'2016-07-04 16:15:38','juju deploy memcached'),(5,'mariadb','',2048,1300,2,'2016-07-04 14:17:51','juju deploy mariadb'),(6,'postgresql','',2048,1500,2,'2016-07-04 16:18:27','juju deploy postgresql pg-a'),(7,'mongodb','',4096,1200,4,'2016-07-04 14:20:21','juju deploy mongodb'),(8,'cassandra','',16384,4000,12,'2016-07-04 16:29:53','juju deploy --repository . local:cassandra'),(9,'zend-server','',2048,1024,1,'2016-07-04 16:35:58','juju deploy zend-server'),(10,'nginx','',1024,512,1,'2016-07-04 16:39:57','juju deploy nginx'),(11,'apache2','',256,250,1,'2016-07-04 16:42:44','juju deploy apache2'),(12,'python-django','',2048,1501,2,'2016-07-04 16:45:05','juju deploy python-django'),(13,'rails','',2048,2048,2,'2016-07-04 16:47:00','juju deploy rails');
/*!40000 ALTER TABLE `Applications` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-07-04 20:50:33