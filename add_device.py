#!/usr/bin/env python3
import easysnmp
from mysql import connector
from datetime import datetime
import sys
import re as regex
import configparser
from pathlib import Path

fconf_path = "%s/db.conf" % Path(__file__).parent.absolute()
if Path(fconf_path).exists():
	config = configparser.ConfigParser()
	config.read(fconf_path)
else:
	print ("Error reading config")
	exit()

if (len(sys.argv) == 4):
	ipaddr = sys.argv[1]
	snmp_comm = sys.argv[2]
	snmp_ver = sys.argv[3]
	ip_patern_check = regex.match('([0-9]{1,3}\.){3}[0-9]{1,3}',ipaddr)
	if ip_patern_check:
		number_check = ip_patern_check.group().split(".")
		number_ok = True
		for number_value in number_check:
			if int(number_value) > 255:
				number_ok = False

		if number_ok:
			session = easysnmp.Session(hostname=ipaddr, community=snmp_comm, version=int(snmp_ver))
			try:
				devDesc = session.get(('sysDescr',0)).value
				devName = session.get(('sysName',0)).value
				db = connector.connect(
					host=config['MySQL']['Host'],
					user=config['MySQL']['User'],
					passwd=config['MySQL']['Passwd'],
					database=config['MySQL']['Database']
				)
				cursor = db.cursor()
				cursor.execute("SELECT * FROM snmp_device WHERE ipAddr=%s",(ipaddr,))
				myresult = cursor.fetchone()
				now = datetime.now()
				if len(myresult) != 0:
					#print("Updating ...")
					cursor.execute("UPDATE snmp_device SET sysDescr=%s,sysName=%s,snmp_community=%s,snmp_version=%s,date_modify=%s WHERE ipAddr=%s",(str(devDesc),str(devName),snmp_comm,snmp_ver,now.strftime('%Y-%m-%d %H:%M:%S'),str(ipaddr)))
				else:
					#print("Inserting ...")
					cursor.execute("INSERT INTO snmp_device (ipAddr,sysDescr,sysName,snmp_community,snmp_version) VALUES (%s,%s,%s,%s,%s)",(str(ipaddr),str(devDesc),str(devName),snmp_comm,snmp_ver))
				db.commit()

				cursor.execute("SELECT id FROM snmp_device WHERE ipAddr=%s",(ipaddr,))
				id_device = cursor.fetchone()
				ifindexes = session.walk('ifIndex')
				for ifindex in ifindexes:
				    idx = ifIdx.value
				    descr = session.get(('ifDescr', idx)).value
					cursor.execute("INSERT IGNORE INTO snmp_interface (device_id,snmp_idx,ifDescr,active) VALUES (%s,%s,%s,%s)",(id_device,idx,descr,1))
				db.commit()

				db.close()
			except easysnmp.exceptions.EasySNMPTimeoutError as serr:
				print("SNMP@{} ERROR: {}".format(ipaddr,serr))
			except connector.Error as dberr:
				print(cursor.statement)
				print("QUERY ERROR: {}".format(dberr))
		else:
			print("IP Address can not over 255!")
	else:
		print("Please input valid IP Address!")
else:
	print ("Usage: addDevice.py <ip_address> <snmp_community> <snmp_version>")
#print ("the script has the name %s" % (sys.argv[1]))
