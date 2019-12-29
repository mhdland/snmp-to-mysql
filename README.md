# snmp-to-mysql

This is utility for saving SNMP data to MySQL database periodically.

PREREQUISITES
=============
Able to do basic MySQL administration, such as importing sql script, create schema, create table, edit table

INSTALL USING PIP
=================
Using python3 as pooler script, it needs few packages to be added:
- easysnmp
- mysql-connector
- configparser

MYSQL TABLES
==================
Create tables in your own schema, using sql file supplied.

Set **active** flag to **0** in **snmp_interface** tables, for skipping snmp query to certain interfaces 

SET EXECUTABLE
======
Set executable for both python3 script files.

CONFIG
====
Fill all necessary information to **db.conf** file

USAGE
=====
**add_device.py <ip_addr> <snmp_community> <snmp_version>** before adding pooler to cron job

Add **snmp_pool.py** to cron job for running periodically

NOTES
======
Only support SNMP version 2c, please use **2** as snmp_version
