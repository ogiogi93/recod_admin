CREATE TABLE `account_customuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `is_admin` tinyint(1) DEFAULT '0',
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `nickname` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `image` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`idx_is_active`),
  KEY (`idx_is_admin`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `platforms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `display_name` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`idx_is_active`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `disciplines` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `api_discipline_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `short_name` varchar(30),
  `copy_rights` varchar(255),
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`idx_is_active`),
  UNIQUE KEY `api_discipline_id_and_name` (`api_discipline_id`, `name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `games` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform_id` int(11) UNSIGNED NOT NULL,
  `discipline_id` int(11) UNSIGNED NOT NULL,
  `thumbnail_url` varchar(200),
  `home_url` varchar(200),
  `is_active` tinyint(1) DEFAULT '1',
  `date_released` date,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`idx_platform_id`),
  KEY (`idx_discipline_id`),
  KEY (`idx_is_active`),
  UNIQUE KEY `platform_id_and_discipline_id` (`platform_id`,`discipline_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `team_members` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) UNSIGNED NOT NULL,
  `team_id` int(11) UNSIGNED NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `is_admin` tinyint(1) DEFAULT '0',
  `date_joined` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
  key (`idx_user_id`),
  KEY (`idx_team_id`),
  KEY (`idx_is_active`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `teams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `date_created` date NOT NULL,
  `description` varchar(1024),
  `is_active` tinyint(1) DEFAULT '1',
  `thumbnail_url` varchar(200),
  `website` varchar(200),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`idx_game_id`),
  KEY (`idx_is_active`),
  UNIQUE KEY `game_id_and_name` (`game_id`, `name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `match_formats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `display_name` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`idx_is_active`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `tournaments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `api_tournament_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `game_id` int(11) UNSIGNED NOT NULL,
  `size` int(11) UNSIGNED NOT NULL,
  `participant_type` varchar(255),
  `full_name` varchar(80),
  `organization` varchar(255),
  `website` varchar(200),
  `date_start` date NOT NULL,
  `date_end` date NOT NULL,
  `online` tinyint(1) DEFAULT '1',
  `public` tinyint(1) DEFAULT '1',
  `location` varchar(255),
  `country` varchar(2) DEFAULT 'JP',
  `description` varchar(1500),
  `rules` varchar(10000),
  `prize` varchar(1500),
  `is_active` tinyint(1) DEFAULT '1',
  `image` varchar(200),
  `match_format_id` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`idx_game_id`),
  KEY (`idx_is_active`),
  KEY (`idx_date_start`),
  KEY (`idx_is_active`),
  UNIQUE KEY `api_tournament_id` (`api_tournament_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `stages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `api_stage_id` int(11) UNSIGNED NOT NULL,
  `tournament_id` int(11) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`idx_tournament_id`),
  UNIQUE KEY `api_stage_id` (`api_stage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `participates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `api_participate_id` varchar(255) NOT NULL,
  `tournament_id` int(11) UNSIGNED NOT NULL,
  `team_id` int(11) UNSIGNED NOT NULL,
  `date_joined` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`idx_tournament_id`),
  UNIQUE KEY `tournament_id_and_team_id` (`tournament_id`, `team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `matches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `api_match_id` varchar(255) NOT NULL,
  `game_id` int(11) UNSIGNED NOT NULL,
  `tournament_id` int(11) UNSIGNED NOT NULL,
  `stage_id` int(11) UNSIGNED NOT NULL,
  `group_number` int(11) UNSIGNED NOT NULL,
  `round_number` int(11) UNSIGNED NOT NULL,
  `match_format_id` int(11) UNSIGNED NOT NULL,
  `status` varchar(80) DEFAULT 'pending',
  `start_date` date,
  `start_time` time,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`idx_game_id`),
  KEY (`idx_tournament_id`),
  KEY (`idx_stage_id`),
  KEY (`idx_start_date`),
  KEY (`idx_start_time`),
  KEY (`idx_is_active`),
  UNIQUE KEY `api_match_id` (`api_match_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `match_teams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `match_id` int(11) UNSIGNED NOT NULL,
  `team_id` int(11) UNSIGNED NOT NULL,
  `api_opponent_id` int(11) UNSIGNED NOT NULL,
  `result` int(11) UNSIGNED,
  `score` int(11) UNSIGNED,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`idx_match_id`),
  KEY (`idx_team_id`),
  KEY (`idx_is_active`),
  UNIQUE KEY `match_id_and_team_id` (`match_id`, `team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `maps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `thumbnail_url` varchar(200),
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY (`idx_game_id`),
  KEY (`idx_is_active`),
  UNIQUE KEY `game_id_and_name` (`game_id`, `name`)
)


CREATE TABLE `articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) UNSIGNED NOT NULL,
  `game_id` int(11) UNSIGNED NOT NULL,
  `url` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `content` text,
  `thumbnail_url` varchar(255) DEFAULT NULL,
  `original_image` varchar(255) DEFAULT '',
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `image_width` float DEFAULT '0',
  `image_height` float DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_articles_on_url` (`url`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_game_id` (`game_id`),
  KEY `idx_is_active` (`is_active`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `video_authors` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `platform_id` int(10) unsigned NOT NULL,
  `platform_author_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `home_url` varchar(255) DEFAULT NULL,
  `thumbnail_url` varchar(255) DEFAULT NULL,
  `enabled` bit(1) NOT NULL,
  `view_count` bigint(20) DEFAULT NULL,
  `comment_count` bigint(20) DEFAULT NULL,
  `subscriber_count` bigint(20) DEFAULT NULL,
  `video_count` int(10) unsigned DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_platform_author_id_and_platform_id` (`platform_author_id`,`platform_id`),
  KEY `idx_platform_id_and_enabled` (`platform_id`,`enabled`),
  KEY `idx_name` (`name`),
  KEY `idx_home_url` (`home_url`),
  KEY `idx_enabled` (`enabled`),
  KEY `idx_updated_at` (`updated_at`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `video_platforms` (
  `id` int(10) unsigned NOT NULL,
  `name` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `video_tags` (
  `video_id` bigint(20) NOT NULL,
  `tags` text NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`video_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `videos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `article_id` bigint(20) NOT NULL,
  `platform_id` int(10) unsigned NOT NULL,
  `platform_video_id` varchar(255) NOT NULL,
  `video_author_id` bigint(20) NOT NULL,
  `thumbnail_url` varchar(1024) NOT NULL,
  `thumbnail_width` int(10) NOT NULL,
  `thumbnail_height` int(10) NOT NULL,
  `duration` int(11) DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `view_count` bigint(20) DEFAULT NULL,
  `like_count` bigint(20) DEFAULT NULL,
  `dislike_count` bigint(20) DEFAULT NULL,
  `comment_count` bigint(20) DEFAULT NULL,
  `published_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_article_id` (`article_id`),
  UNIQUE KEY `idx_platform_video_id_and_platform_id` (`platform_video_id`,`platform_id`),
  KEY `idx_platform_id` (`platform_id`),
  KEY `idx_video_author_id_and_published_at` (`video_author_id`, `published_at`),
  KEY `idx_published_at` (`published_at`),
  KEY `idx_updated_at` (`updated_at`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `forums` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `title` varchar(30) NOT NULL,
  `description` varchar(1500),
  `is_active` tinyint(1) DEFAULT '1',
  `updated_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_is_active` (`is_active`),
  KEY `idx_updated_at` (`updated_at`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `topics` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `forum_id` bigint(20) NOT NULL,
  `title` varchar(30) NOT NULL,
  `description` varchar(1500),
  `is_active` tinyint(1) DEFAULT '1',
  `updated_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_forum_id` (`forum_id`),
  KEY `idx_is_active` (`is_active`),
  KEY `idx_updated_at` (`updated_at`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `threads` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `topic_id` bigint(20) NOT NULL,
  `description` varchar(1500) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `updated_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_topic_id` (`topic_id`),
  KEY `idx_is_active` (`is_active`),
  KEY `idx_updated_at` (`updated_at`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
