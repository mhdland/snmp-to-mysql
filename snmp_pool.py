#!/usr/bin/env python3
from easysnmp import Session
from mysql import connector
from datetime import datetime
import configparser
from pathlib import Path

fconf_path = "%s/db.conf" % Path(__file__).parent.absolute()
if Path(fconf_path).exists():
	config = configparser.ConfigParser()
	config.read(fconf_path)
else:
	print ("Error reading config")
	exit()

db = connector.connect(
	host=config['MySQL']['Host'],
	user=config['MySQL']['User'],
	passwd=config['MySQL']['Passwd'],
	database=config['MySQL']['Database']
)

cursor = db.cursor()
cursor.execute("SELECT * FROM snmp_device")
myresult = cursor.fetchall()

sysReset = False

for x in myresult:
	# Create an SNMP session to be used for all our requests
	ip = x[1]
	scomm = x[6]
	sver = int(x[7])
	session = Session(hostname=ip, community=scomm, version=sver)
	db_uptime = x[10]
	sys_uptime = session.get(('sysUpTime','0')).value
	if (int(sys_uptime) < int(db_uptime)):
		sysReset = True
	try:
		cursor.execute("UPDATE snmp_device SET sysUpTime=%s WHERE id=%s",(int(sys_uptime),x[0]))
		db.commit()
	except connector.Error as err:
		print("Update Error: {}".format(err))

	sql = "select * from snmp_interface where device_id="+str(x[0])+" and active='1'"
	cursor.execute(sql)
	intfs = cursor.fetchall()
	for intf in intfs:
		#print(intf)
		hc_in = session.get(('ifHCInOctets', intf[2])).value
		#print(hc_in)
		hc_out = session.get(('ifHCOutOctets', intf[2])).value
		cursor.execute("select * from snmp_last_value where device_id="+str(x[0])+" and interface_id="+str(intf[2]))
		lstval = cursor.fetchone()
		if len(lstval) == 0:
			try:
				cursor.execute("insert into snmp_last_value (device_id,interface_id,last_val_in,last_val_out) values (%s,%s,%s,%s)",(str(x[0]),str(intf[2]),int(hc_in),int(hc_out)))
				db.commit()
			except connector.Error as err:
				print("Insert error: {}".format(err))
		else:
			usageInVal = False
			usageOutVal = False
			if sysReset:
				minIn=0
				minOut=0
			elif (int(hc_in) < lstval[3]):
				#possiby rollover
				usageIn = (18446744073709551615 - lstval[3]) + int(hc_in)
				usageInVal = True
			elif (int(hc_out) < lstval[4]):
				usageOut = (18446744073709551615 - lstval[4]) + int(hc_out)
				usageOutVal = True
			else:
				minIn=lstval[3]
				minOut=lstval[4]

			if not usageInVal:
				usageIn = int(hc_in) - minIn
			if not usageOutVal:
				usageOut = int(hc_out) - minOut
			#print (str(hc_in)+" : "+str(usageIn))
			now = datetime.now()
			sdelta = (now - lstval[5]).total_seconds()
			speedIn = int((usageIn * 8) / sdelta)
			speedOut = int((usageOut * 8) / sdelta)
			#print(speedIn)
			try:
				if speedIn != 0 and speedOut != 0:
					cursor.execute("INSERT INTO snmp_traffic VALUES (%s,%s,%s,%s,%s)",(now.strftime('%Y-%m-%d %H:%M:%S'),lstval[1],lstval[2],speedIn,speedOut))
				cursor.execute("UPDATE snmp_last_value SET last_val_in=%s,last_val_out=%s,date_update=%s WHERE id=%s",(int(hc_in),int(hc_out),now.strftime('%Y-%m-%d %H:%M:%S'),lstval[0]))
				db.commit()
			except connector.Error as err:
				print("Update Error: {}".format(err))
db.close()
