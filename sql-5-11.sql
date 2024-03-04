/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.6.12-log : Database - scps
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`scps` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `scps`;

/*Table structure for table `booking` */

DROP TABLE IF EXISTS `booking`;

CREATE TABLE `booking` (
  `booking_id` int(100) NOT NULL AUTO_INCREMENT,
  `user_id` int(10) DEFAULT NULL,
  `book_date` date DEFAULT NULL,
  `slot_selection` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`booking_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

/*Data for the table `booking` */

insert  into `booking`(`booking_id`,`user_id`,`book_date`,`slot_selection`,`status`) values (12,5,'2022-11-18','3','completed'),(13,6,'2022-05-31','5','pending'),(16,5,'2022-10-16','8','pending');

/*Table structure for table `building` */

DROP TABLE IF EXISTS `building`;

CREATE TABLE `building` (
  `building_id` int(10) NOT NULL AUTO_INCREMENT,
  `building_name` varchar(100) DEFAULT NULL,
  `no_of_floor` int(18) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `post` varchar(100) DEFAULT NULL,
  `pincode` int(10) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`building_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `building` */

insert  into `building`(`building_id`,`building_name`,`no_of_floor`,`place`,`post`,`pincode`,`email`) values (2,'aaa',5,'qwe','jhg',123,'a@'),(4,'ccc',2,'sdfd','ee',4323,'c@'),(7,'kfc',3,'kuttiyattoor','kuttiyattoor.p.o',1234,'admin@gmail.com'),(8,'kfc',3,'kuttiyattoor','kuttiyattoor.p.o',1234,'a@');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaint_id` int(100) NOT NULL AUTO_INCREMENT,
  `user_id` int(10) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `complaint` varchar(100) DEFAULT NULL,
  `reply` varchar(100) DEFAULT NULL,
  `reply_date` date DEFAULT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`complaint_id`,`user_id`,`date`,`complaint`,`reply`,`reply_date`) values (1,5,'2022-12-04','bad service','fddrgrrgg','2022-12-02'),(2,6,'2022-11-09','no security','pending','0000-00-00');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `user_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`user_name`,`password`,`user_type`) values (1,'admin','admin1','admin'),(2,'a@','1','building'),(4,'c@','xcv','building'),(5,'ds@','432','user'),(6,'e@','6546','user'),(7,'admin@gmail.com','1234','building'),(8,'a@','1','building'),(9,'kf@gmail.com','42342343','security'),(10,'kf@gmail.com','42342343','security'),(11,'kf@gmail.com','42342343','security'),(12,'kf@gmail.com','42342343','security'),(13,'kf@gmail.com','42342343','security'),(14,'kf@gmail.com','42342343','security'),(15,'kf@gmail.com','42342343','security'),(16,'kf@gmail.com','42342343','security'),(17,'kf@gmail.com','42342343','security'),(18,'kf@gmail.com','42342343','security'),(19,'kf@gmail.com','42342343','security'),(20,'kf@gmail.com','42342343','security');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` int(10) NOT NULL AUTO_INCREMENT,
  `user_id` int(10) DEFAULT NULL,
  `payment_commission` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `payment` */

/*Table structure for table `rating` */

DROP TABLE IF EXISTS `rating`;

CREATE TABLE `rating` (
  `rating_id` int(10) NOT NULL AUTO_INCREMENT,
  `user_id` int(10) DEFAULT NULL,
  `date_time` datetime DEFAULT NULL,
  `rating` varchar(165) DEFAULT NULL,
  PRIMARY KEY (`rating_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `rating` */

/*Table structure for table `security` */

DROP TABLE IF EXISTS `security`;

CREATE TABLE `security` (
  `security_id` int(10) NOT NULL AUTO_INCREMENT,
  `security_name` varchar(100) DEFAULT NULL,
  `building_id` int(12) DEFAULT NULL,
  `email` varchar(111) DEFAULT NULL,
  `phone_no` int(50) DEFAULT NULL,
  PRIMARY KEY (`security_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;

/*Data for the table `security` */

insert  into `security`(`security_id`,`security_name`,`building_id`,`email`,`phone_no`) values (1,'abc',4,'abc@gmail.com',4278746),(8,'admin',4,'kf@gmail.com',42342343),(15,'admin',4,'kf@gmail.com',42342343),(16,'admin',4,'kf@gmail.com',42342343),(17,'admin',4,'kf@gmail.com',42342343),(18,'admin',4,'kf@gmail.com',42342343),(19,'admin',2,'kf@gmail.com',42342343),(20,'admin',2,'kf@gmail.com',42342343);

/*Table structure for table `services` */

DROP TABLE IF EXISTS `services`;

CREATE TABLE `services` (
  `service_id` int(10) NOT NULL AUTO_INCREMENT,
  `building_id` int(10) DEFAULT NULL,
  `services` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`service_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `services` */

insert  into `services`(`service_id`,`building_id`,`services`) values (1,NULL,NULL),(2,2,'hfwefh');

/*Table structure for table `slot` */

DROP TABLE IF EXISTS `slot`;

CREATE TABLE `slot` (
  `slot_id` int(10) NOT NULL AUTO_INCREMENT,
  `building_id` varchar(100) DEFAULT NULL,
  `num_of_slot` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`slot_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `slot` */

insert  into `slot`(`slot_id`,`building_id`,`num_of_slot`,`status`) values (1,'2','3','0'),(2,'2','3','0'),(3,'2','3','0'),(4,'2','3','0'),(5,'2','5','0'),(6,'2','3','pending'),(7,'2','3','pending'),(8,'2','5','pending'),(9,'4','364523687345','pending'),(10,'4','4','pending');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(100) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `ph_no` bigint(199) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `photo` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`user_name`,`email`,`ph_no`,`place`,`photo`) values (5,'gfdfg','a@',4236265753,'ggrt',NULL),(6,'erd','c@',64548,'hyt',NULL);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
