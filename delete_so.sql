SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS  `accomments`;
CREATE TABLE `accomments` (
  `cid` int(15) NOT NULL,
  `content` text NOT NULL,
  `userName` tinytext NOT NULL,
  `layer` int(10) NOT NULL,
  `acid` int(15) NOT NULL,
  `isDelete` tinyint(10) NOT NULL,
  `siji` tinyint(10) NOT NULL,
  `checkTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `page` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`page`),
  KEY `acid` (`acid`),
  CONSTRAINT `accomments_ibfk_1` FOREIGN KEY (`acid`) REFERENCES `accommentsinfo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

DROP TABLE IF EXISTS  `accomments_delete`;
CREATE TABLE `accomments_delete` (
  `cid` int(15) NOT NULL,
  `content` text NOT NULL,
  `userName` tinytext NOT NULL,
  `layer` int(10) NOT NULL,
  `acid` int(15) NOT NULL,
  `isDelete` tinyint(10) NOT NULL,
  `siji` tinyint(10) NOT NULL,
  `checkTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`cid`),
  KEY `acid` (`acid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

DROP TABLE IF EXISTS  `accomments_siji`;
CREATE TABLE `accomments_siji` (
  `cid` int(15) NOT NULL,
  `content` text NOT NULL,
  `userName` tinytext NOT NULL,
  `layer` int(10) NOT NULL,
  `acid` int(15) NOT NULL,
  `isDelete` tinyint(10) NOT NULL,
  `siji` tinyint(10) NOT NULL,
  `checkTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`cid`),
  KEY `acid` (`acid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

DROP TABLE IF EXISTS  `accommentsinfo`;
CREATE TABLE `accommentsinfo` (
  `id` int(15) NOT NULL,
  `type` varchar(10) NOT NULL,
  `title` tinytext NOT NULL,
  `up` tinytext NOT NULL,
  `postTime` date NOT NULL,
  `url` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

DROP TABLE IF EXISTS  `accommentsstore`;
CREATE TABLE `accommentsstore` (
  `cid` int(15) NOT NULL,
  `name` varchar(50) NOT NULL,
  `content` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

DROP TABLE IF EXISTS  `acrefresh`;
CREATE TABLE `acrefresh` (
  `id` int(15) NOT NULL,
  `createTime` datetime DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS  `comment2db`;
CREATE TABLE `comment2db` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) NOT NULL,
  `userName` text,
  `postDate` datetime NOT NULL,
  `contents` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=808 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

DROP TABLE IF EXISTS  `commentdb`;
CREATE TABLE `commentdb` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `userName` text NOT NULL,
  `postDate` datetime NOT NULL,
  `sortDate` datetime NOT NULL,
  `contents` text NOT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=749 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

DROP TABLE IF EXISTS  `commentdb_test`;
CREATE TABLE `commentdb_test` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `userName` text NOT NULL,
  `postDate` datetime NOT NULL,
  `sortDate` datetime NOT NULL,
  `contents` text NOT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=655 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

DROP TABLE IF EXISTS  `comment2db_test`;
CREATE TABLE `comment2db_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) NOT NULL,
  `userName` text,
  `postDate` datetime NOT NULL,
  `contents` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=662 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

DROP TABLE IF EXISTS  `status`;
CREATE TABLE `status` (
  `name` varchar(16) NOT NULL,
  `status` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `score` int(11) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;

