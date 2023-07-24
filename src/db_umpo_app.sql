-- Adminer 4.6.2 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `alembic_version` (`version_num`) VALUES
('3ae7de621980');

DROP TABLE IF EXISTS `jadwal`;
CREATE TABLE `jadwal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mata_kuliah_id` int(11) NOT NULL,
  `kelas_id` int(11) NOT NULL,
  `hari` enum('SENIN','SELASA','RABU','KAMIS','JUMAT','SABTU','MINGGU') NOT NULL,
  `jam_mulai` time NOT NULL,
  `jam_selesai` time NOT NULL,
  `presensi_status` int(11) NOT NULL DEFAULT '0',
  `flag` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `jadwal_ibfk_1` (`mata_kuliah_id`),
  KEY `kelas_id` (`kelas_id`),
  CONSTRAINT `jadwal_ibfk_1` FOREIGN KEY (`mata_kuliah_id`) REFERENCES `mata_kuliah` (`id`),
  CONSTRAINT `jadwal_ibfk_2` FOREIGN KEY (`kelas_id`) REFERENCES `kelas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `jadwal` (`id`, `mata_kuliah_id`, `kelas_id`, `hari`, `jam_mulai`, `jam_selesai`, `presensi_status`, `flag`) VALUES
(3,	2,	2,	'SENIN',	'09:00:00',	'10:00:00',	0,	0),
(4,	2,	2,	'SENIN',	'10:25:00',	'12:00:00',	0,	0),
(5,	2,	2,	'SENIN',	'10:00:00',	'12:00:00',	0,	0),
(6,	2,	2,	'SENIN',	'09:00:00',	'10:00:00',	0,	0),
(7,	3,	2,	'SENIN',	'08:00:00',	'08:30:00',	0,	0),
(8,	2,	2,	'SENIN',	'09:01:00',	'10:00:00',	1,	1),
(9,	3,	2,	'SENIN',	'08:00:00',	'09:00:00',	0,	1);

DROP TABLE IF EXISTS `kelas`;
CREATE TABLE `kelas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fakultas` varchar(250) NOT NULL,
  `prodi` varchar(250) NOT NULL,
  `kelas` varchar(250) NOT NULL,
  `flag` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `kelas` (`id`, `fakultas`, `prodi`, `kelas`, `flag`) VALUES
(1,	'TEKNIK',	'TEKNIK INFORMATIKA',	'2020',	0),
(2,	'TEKNIK',	'TEKNIK INFORMATIKA',	'2021',	1);

DROP TABLE IF EXISTS `kelas_mhs`;
CREATE TABLE `kelas_mhs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kelas_id` int(11) NOT NULL,
  `mahasiswa_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `kelas_mhs_ibfk_1` (`kelas_id`),
  KEY `kelas_mhs_ibfk_2` (`mahasiswa_id`),
  CONSTRAINT `kelas_mhs_ibfk_1` FOREIGN KEY (`kelas_id`) REFERENCES `kelas` (`id`),
  CONSTRAINT `kelas_mhs_ibfk_2` FOREIGN KEY (`mahasiswa_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `kelas_mhs` (`id`, `kelas_id`, `mahasiswa_id`) VALUES
(1,	2,	6),
(2,	2,	5),
(3,	2,	7),
(4,	2,	32),
(6,	2,	33),
(7,	2,	34),
(8,	2,	35);

DROP TABLE IF EXISTS `mata_kuliah`;
CREATE TABLE `mata_kuliah` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(250) NOT NULL,
  `flag` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `mata_kuliah` (`id`, `nama`, `flag`) VALUES
(1,	'Pemrograman Dasar',	0),
(2,	'Algoritma',	1),
(3,	'Matematika Diskrit',	1);

DROP TABLE IF EXISTS `presensi`;
CREATE TABLE `presensi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `kelas_id` int(11) NOT NULL,
  `jadwal_id` int(11) NOT NULL,
  `mata_kuliah_id` int(11) NOT NULL,
  `tanggal` date NOT NULL,
  `jam` time NOT NULL,
  `photo` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `presensi_ibfk_3` (`jadwal_id`),
  KEY `presensi_ibfk_2` (`kelas_id`),
  KEY `presensi_ibfk_4` (`mata_kuliah_id`),
  KEY `presensi_ibfk_1` (`user_id`),
  CONSTRAINT `presensi_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `presensi_ibfk_2` FOREIGN KEY (`kelas_id`) REFERENCES `kelas` (`id`),
  CONSTRAINT `presensi_ibfk_3` FOREIGN KEY (`jadwal_id`) REFERENCES `jadwal` (`id`),
  CONSTRAINT `presensi_ibfk_4` FOREIGN KEY (`mata_kuliah_id`) REFERENCES `mata_kuliah` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `presensi` (`id`, `user_id`, `kelas_id`, `jadwal_id`, `mata_kuliah_id`, `tanggal`, `jam`, `photo`) VALUES
(1,	32,	2,	8,	2,	'2023-07-24',	'18:32:48',	'null'),
(2,	35,	2,	8,	2,	'2023-07-24',	'18:40:36',	'null');

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(250) NOT NULL,
  `name` varchar(250) NOT NULL,
  `role` enum('ADMIN','MAHASISWA') NOT NULL,
  `flag` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `users` (`id`, `username`, `password`, `name`, `role`, `flag`) VALUES
(4,	'admin',	'21232f297a57a5a743894a0e4a801fc3',	'Admin',	'ADMIN',	1),
(5,	'00001',	'd41d8cd98f00b204e9800998ecf8427e',	'Sindi3',	'MAHASISWA',	0),
(6,	'20332018',	'691f652625bbd30315f13fe522ad5a08',	'20332018',	'MAHASISWA',	0),
(7,	'00001',	'd41d8cd98f00b204e9800998ecf8427e',	'Sindi2',	'MAHASISWA',	0),
(8,	'20332018',	'691f652625bbd30315f13fe522ad5a08',	'20332018',	'MAHASISWA',	0),
(10,	'00001',	'd41d8cd98f00b204e9800998ecf8427e',	'Sindi2',	'MAHASISWA',	0),
(11,	'20332018',	'691f652625bbd30315f13fe522ad5a08',	'20332018',	'MAHASISWA',	0),
(12,	'00001',	'd41d8cd98f00b204e9800998ecf8427e',	'Sindi2',	'MAHASISWA',	0),
(13,	'20332018',	'691f652625bbd30315f13fe522ad5a08',	'20332018',	'MAHASISWA',	0),
(17,	'00001',	'd41d8cd98f00b204e9800998ecf8427e',	'Sindi2',	'MAHASISWA',	0),
(18,	'20332018',	'691f652625bbd30315f13fe522ad5a08',	'20332018',	'MAHASISWA',	0),
(19,	'00001',	'd41d8cd98f00b204e9800998ecf8427e',	'Sindi2',	'MAHASISWA',	0),
(20,	'20332018',	'691f652625bbd30315f13fe522ad5a08',	'20332018',	'MAHASISWA',	0),
(21,	'00001',	'd41d8cd98f00b204e9800998ecf8427e',	'Sindi2',	'MAHASISWA',	0),
(22,	'20332018',	'691f652625bbd30315f13fe522ad5a08',	'20332018',	'MAHASISWA',	0),
(23,	'00001',	'd41d8cd98f00b204e9800998ecf8427e',	'Sindi2',	'MAHASISWA',	0),
(24,	'20332018',	'691f652625bbd30315f13fe522ad5a08',	'20332018',	'MAHASISWA',	0),
(32,	'20332018',	'691f652625bbd30315f13fe522ad5a08',	'Defri Indra Mahardika',	'MAHASISWA',	1),
(33,	'0002',	'fcd04e26e900e94b9ed6dd604fed2b64',	'Marmoyo',	'MAHASISWA',	1),
(34,	'0003',	'7cd86ecb09aa48c6e620b340f6a74592',	'Wahid',	'MAHASISWA',	1),
(35,	'0005',	'd39934ce111a864abf40391f3da9cdf5',	'Dani',	'MAHASISWA',	1);

DROP TABLE IF EXISTS `user_training`;
CREATE TABLE `user_training` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `path` varchar(250) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_training_ibfk_1` (`user_id`),
  CONSTRAINT `user_training_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- 2023-07-24 12:19:51
