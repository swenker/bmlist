
CREATE DATABASE  IF NOT EXISTS `bmlist-test` DEFAULT CHARACTER SET utf8;

GRANT ALL ON bmlist-test.* TO 'bmlist'@'%';
GRANT ALL ON bmlist-test.* TO 'bmlist'@'localhost';


USE bmlist-test;

CREATE TABLE IF NOT EXISTS `bm_book`(
`bid` INT(9) NOT NULL AUTO_INCREMENT,
`isbn10` CHAR(10),
`isbn13` CHAR(13),
`title` VARCHAR(80),
`subtitle` VARCHAR(80),
`translators` VARCHAR(80),
`author` VARCHAR(80),
`publisher` VARCHAR(80),
`pubdate` VARCHAR(20),
`price` DECIMAL(6,2),
`pages` SMALLINT(2),
`update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
`create_time` TIMESTAMP NOT NULL DEFAULT 0,
`quantity` SMALLINT(2),
`series` VARCHAR(80),
`keywords` VARCHAR(80),
`summary`  VARCHAR(500),
`author_intro` VARCHAR(500),
`status` TINYINT(1) DEFAULT 1,
 PRIMARY KEY(`bid`)
) ENGINE=Innodb DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `bm_user_book`(
`uid` INT(9) NOT NULL, 
`bid` INT(9) NOT NULL,
`add_time` TIMESTAMP NOT NULL DEFAULT 0, 
`status` TINYINT(1) DEFAULT 1
) ENGINE=Innodb DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `bm_user`(
`uid` INT(9) NOT NULL AUTO_INCREMENT, 
`update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
`create_time` TIMESTAMP NOT NULL DEFAULT 0, 
`email` varchar(50) not null,
`passwd` varchar(64) not null,
`nickname` varchar(50),
`cellphone` varchar(20),
`status` TINYINT(1) DEFAULT 1,
PRIMARY KEY(`uid`)
) ENGINE=Innodb DEFAULT CHARSET=utf8;

INSERT INTO bm_user(create_time,email,passwd,nickname,cellphone)VALUES(now(),'swenker@126.com',MD5('koob'),'swenker','18601203570');

