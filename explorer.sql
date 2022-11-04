DROP TABLE IF EXISTS `torrent_information_table`;

CREATE TABLE `torrent_information_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `info_hash` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `torrent_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `torrent_contents` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `torrent_size` bigint NOT NULL,
  `discovered_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `info_hash` (`info_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `torrent_information_table` WRITE;
UNLOCK TABLES;