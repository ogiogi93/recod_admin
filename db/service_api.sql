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
  `image_url` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
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
  UNIQUE KEY `api_discipline_id_and_name` (`api_discipline_id`, `name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `games` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform_id` int(11) UNSIGNED NOT NULL,
  `discipline_id` int(11) UNSIGNED NOT NULL,
  `logo_url` varchar(200),
  `home_url` varchar(200),
  `is_active` tinyint(1) DEFAULT '1',
  `date_released` date,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `teams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `date_created` date NOT NULL,
  `description` varchar(1024),
  `is_active` tinyint(1) DEFAULT '1',
  `logo_url` varchar(200),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `game_id_and_name` (`game_id`, `name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `match_formats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `display_name` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
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
  `match_format_id` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
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
  UNIQUE KEY `api_match_id` (`api_match_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `match_teams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `match_id` int(11) UNSIGNED NOT NULL,
  `team_id` int(11) UNSIGNED NOT NULL,
  `result` int(11) UNSIGNED,
  `score` int(11) UNSIGNED,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `match_id_and_team_id` (`match_id`, `team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
