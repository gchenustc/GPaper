-- Active: 1693989765579@@127.0.0.1@3306
CREATE DATABASE db_data DEFAULT CHARACTER SET = 'utf8mb4';

db_data


/*paperType*/
CREATE TABLE `t_papertype` (
    `id` int(11) NOT NULL AUTO_INCREMENT, `paperTypeName` varchar(200) DEFAULT NULL, `paperTypeDesc` varchar(1000) DEFAULT NULL, PRIMARY KEY (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 6 DEFAULT CHARSET = utf8;


/*paper*/
CREATE TABLE `t_paper` (
    `id` int(11) NOT NULL AUTO_INCREMENT, `folderPath` varchar(100) DEFAULT NULL, `fileName` varchar(200) DEFAULT NULL, `paperName` varchar(200) DEFAULT NULL, `paperTypeId` int(11) DEFAULT NULL, `title` varchar(200) DEFAULT NULL, `author` varchar(200) DEFAULT NULL, `abstract` text DEFAULT NULL, `text` MEDIUMTEXT DEFAULT NULL, `journal` varchar(100) DEFAULT NULL, `issue` int(11) DEFAULT NULL, `volume` int(11) DEFAULT NULL, `page` varchar(100) DEFAULT NULL, `date` date DEFAULT NULL, `url` varchar(100) DEFAULT NULL, `doi` varchar(100) DEFAULT NULL, `issn` varchar(100) DEFAULT NULL, `isReferencedByCount` int(11) DEFAULT NULL, PRIMARY KEY (`id`), KEY `paperTypeId` (`paperTypeId`), CONSTRAINT `t_paper_ibfk_1` FOREIGN KEY (`paperTypeId`) REFERENCES `t_papertype` (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 3 DEFAULT CHARSET = utf8;


/*paperSection*/
CREATE TABLE `t_papersection` (
    `id` int(11) NOT NULL AUTO_INCREMENT, `paperSectionText` text DEFAULT NULL, `paperSectionVector` MEDIUMBLOB DEFAULT NULL, `paperNameId` int(11) DEFAULT NULL, PRIMARY KEY (`id`), KEY `paperNameId` (`paperNameId`), CONSTRAINT `t_papersection_ibfk_1` FOREIGN KEY (`paperNameId`) REFERENCES `t_paper` (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 3 DEFAULT CHARSET = utf8;