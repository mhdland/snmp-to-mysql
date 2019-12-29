CREATE TABLE `snmp_device` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ipAddr` varchar(16) NOT NULL,
  `sysDescr` varchar(200) NOT NULL,
  `sysName` varchar(200) NOT NULL,
  `sysContact` varchar(200) DEFAULT NULL,
  `sysLocation` text,
  `snmp_community` varchar(100) DEFAULT NULL,
  `snmp_version` varchar(2) DEFAULT NULL,
  `date_add` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_modify` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `sysUpTime` bigint(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE `snmp_interface` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` int(11) NOT NULL,
  `snmp_idx` int(11) NOT NULL,
  `ifDescr` varchar(100) DEFAULT NULL,
  `date_add` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `active` varchar(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE `snmp_last_value` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` int(11) NOT NULL,
  `interface_id` int(11) NOT NULL,
  `last_val_in` bigint(20) unsigned DEFAULT NULL,
  `last_val_out` bigint(20) unsigned DEFAULT NULL,
  `date_update` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`,`device_id`,`interface_id`)
) ENGINE=InnoDB;

CREATE TABLE `snmp_traffic` (
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `device_id` int(11) NOT NULL,
  `interface_id` int(11) NOT NULL,
  `ifHCIn` bigint(20) unsigned DEFAULT NULL,
  `ifHCOut` bigint(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`timestamp`,`device_id`,`interface_id`)
) ENGINE=InnoDB;
