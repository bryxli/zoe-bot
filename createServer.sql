CREATE DATABASE IF NOT EXISTS db;

USE db;

CREATE TABLE IF NOT EXISTS `serverlist` (
  `guild_id` varchar(255) NOT NULL,
  `channel_id` varchar(255) NOT NULL,
  `region` varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS `recent` (
  `message` varchar(255) NOT NULL
);