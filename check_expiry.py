#!/usr/bin/env python
#Joe Dugdale, check tower expiry 24/02.2017
import json
import sys
import subprocess
from datetime import date
from datetime import datetime,timedelta
try:
  warn = int(sys.argv[1])
  crit = int(sys.argv[2])
  ip_addr = str(sys.argv[3])
  passwd = str(sys.argv[4])
except IndexError:
  print "Usage: check_tower_license.py <warn> <crit> <ipaddress> <passwd>"
  sys.exit(1)
command = "curl  -ks -u apiuser:"+passwd+" -X GET  -H \"Accept: application/json\" https://"+ip_addr+"/api/v1/config/"
#print command
var = subprocess.check_output(command, shell = True)
try:
  json1_data = json.loads(var)
except ValueError:
  print 'Decoding JSON has failed'
  rc = 3
  sys.exit(rc)
#print json1_data
json2_data = json1_data['license_info']['time_remaining']
current_instances = json1_data['license_info']['current_instances']
instance_count = json1_data['license_info']['instance_count']
daysleft= json2_data /60/24/60
expirydate = datetime.today() + timedelta(days=daysleft)
perfdata= str(current_instances)+" nodes used |used="+str(current_instances)+";;;;"+str(instance_count)
if int(daysleft) < crit:
        print "CRITICAL - less than " + str(crit) + " Days till license expires, it expires " + expirydate.strftime('%m/%d/%Y') + ", " + str(daysleft) + " days left till expiry "+perfdata
        sys.exit(2)
elif int(daysleft) < warn:
        print "WARNING - less than " + str(warn) + " Days till license expires, it expires " + expirydate.strftime('%m/%d/%Y') + ", " + str(daysleft) + " days left till expiry "+perfdata
        sys.exit(1)
else:
        print "OK - License expires " + expirydate.strftime('%m/%d/%Y') + ", " + str(daysleft) + " days left till expiry "+perfdata
        sys.exit(0)
