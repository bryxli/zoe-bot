CREATE TABLE IF NOT EXISTS `serverlist` (
  `guild_id` varchar(255) NOT NULL,
  `channel_id` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `region` varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS `recent` (
  `message` varchar(255) NOT NULL
);