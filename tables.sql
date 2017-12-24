/*
MySQL Data Transfer
Target Database: todo
Date: 2017/12/12 14:12:25
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for case_list
-- ----------------------------
DROP TABLE IF EXISTS `case_list`;
CREATE TABLE `case_list` (
  `id` int(10) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `pid` int(10) DEFAULT NULL,
  `user_id` int(10) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` int(10) DEFAULT NULL,
  `project_id` bigint(20) DEFAULT NULL,
  `entry` bigint(20) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`entry`)
) ENGINE=InnoDB AUTO_INCREMENT=4011 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for interface_list
-- ----------------------------
DROP TABLE IF EXISTS `interface_list`;
CREATE TABLE `interface_list` (
  `entry` int(10) NOT NULL AUTO_INCREMENT,
  `test_name` varchar(255) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `method` varchar(255) DEFAULT NULL,
  `parms` varchar(2000) DEFAULT NULL,
  `verif_code` int(10) DEFAULT NULL,
  `need_save_response` int(10) DEFAULT NULL,
  `need_verif_value` int(10) DEFAULT NULL,
  `verif_key` varchar(255) DEFAULT NULL,
  `verif_value_from_file` int(10) DEFAULT NULL,
  `verif_value` varchar(255) DEFAULT NULL,
  `test_description` varchar(255) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `project` varchar(255) DEFAULT NULL,
  `datatype` varchar(255) DEFAULT NULL,
  `verif_parms` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`entry`)
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for interface_task_list
-- ----------------------------
DROP TABLE IF EXISTS `interface_task_list`;
CREATE TABLE `interface_task_list` (
  `entry` int(10) NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) DEFAULT NULL,
  `create_user` varchar(255) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `task_status` int(10) unsigned zerofill DEFAULT NULL,
  `case_id` varchar(2000) DEFAULT NULL,
  `base_host` varchar(255) DEFAULT NULL,
  `is_settime_task` int(10) unsigned zerofill DEFAULT '0000000000',
  `start_time` varchar(255) DEFAULT NULL,
  `settime_task_status` int(10) unsigned zerofill DEFAULT NULL,
  PRIMARY KEY (`entry`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for list
-- ----------------------------
DROP TABLE IF EXISTS `list`;
CREATE TABLE `list` (
  `entry` int(10) NOT NULL AUTO_INCREMENT,
  `pid` int(10) unsigned zerofill DEFAULT NULL,
  `labelname` varchar(100) DEFAULT NULL,
  `userId` int(10) unsigned zerofill DEFAULT NULL,
  `flag` float DEFAULT NULL,
  `mainpid` int(10) unsigned zerofill DEFAULT NULL,
  `haschildren` int(10) unsigned zerofill DEFAULT NULL,
  `testflag` tinyint(10) unsigned zerofill DEFAULT NULL COMMENT '试测版是否完成',
  `isdone` int(10) unsigned zerofill DEFAULT NULL COMMENT '主任务完成标签',
  `imageUrl` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`entry`)
) ENGINE=InnoDB AUTO_INCREMENT=1905 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for project_list
-- ----------------------------
DROP TABLE IF EXISTS `project_list`;
CREATE TABLE `project_list` (
  `entry` int(11) NOT NULL AUTO_INCREMENT,
  `project_key` varchar(255) DEFAULT NULL,
  `create_user` varchar(255) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`entry`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(40) DEFAULT NULL,
  `hash_password` varchar(80) DEFAULT NULL,
  `salt` varchar(80) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
