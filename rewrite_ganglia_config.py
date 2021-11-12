#!/usr/bin/python3
#filename: rewrite_ganglia_config.py
#author: Theodore Knab
#date: 11/8/2021
#description: rewrite the file on the clients holding /etc/ganglia/gmond.conf
#
# import os.path
import os
import re

def read_file(myfile):
  with open(myfile) as f:
    lines = f.readlines()
  f.close()

  return lines

def find_head_node_ip(filename):
   mylines=read_file(filename)
   for line in mylines:
     #print("debug %s" % line.rstrip())
     p = re.compile('SlurmctldHost=*',re.IGNORECASE)
     if p.match(line):
        return line.split("=")[1].split("(")[1].split(')')[0] #tripple split on line 1. get second field after "=', 2. get second field after '(', 3. drop last ")' character

def get_cnfconfig_info(filename,regex):
  mylines=read_file(filename)
  for line in mylines:
    p = re.compile(regex,re.IGNORECASE)
    if p.match(line):
     return line.strip().split("=")[1]


config_words_to_target=['cluster {', 'host {', 'udp_recv_channel {', 'udp_send_channel {']

myheadnode_ip=find_head_node_ip("/opt/slurm/etc/slurm_parallelcluster.conf")  
nodetype=get_cnfconfig_info("/etc/parallelcluster/cfnconfig",'^cfn_node_type')
stack_name=get_cnfconfig_info("/etc/parallelcluster/cfnconfig",'^stack_name')
#ganglia_conf=open('/etc/ganglia/gmond.conf','r')
ganglia_conf=read_file('/etc/ganglia/gmond.conf')
linenum=0

myhit=0
keyword=""
myport=8649

edit=[] #new version of config

######################
#main area to modify
######################

for line in ganglia_conf:
   #see if we are at a start of stanza
   linenum+=1
   num = str(linenum)
   
   p=re.compile('#.*')

   #logic for match areas to target for a change
   for test in config_words_to_target:
      if re.search(test,line) and not p.match(line):
        myhit=1
        keyword=test
        break #we found a match start stuff
      else:
        keyword=""

   if myhit ==1 and re.search("}", line):
      edit.append(line) #closing line
      print (line) #closing line
      myhit=0
   elif myhit ==1: #changes to configuration file
      if re.search("cluster {", keyword):
         print("cluster {")
         edit.append("cluster {")
         print("  name = \"paralelcluster-%s\"" % stack_name )
         edit.append("  name = \"paralelcluster-%s\"" % stack_name )
         print("  owner=\"unspecified\" ")
         edit.append("  owner=\"unspecified\" ")
         print("  latlong=\"unspecified\" ")
         edit.append("  latlong=\"unspecified\" ")
         print("  url=\"unspecified\" ")
         edit.append("  url=\"unspecified\" ")
      elif re.search("host {",keyword):
         print("host {")
         edit.append("host {")
         print("location = \"us-east-1c\"")
         edit.append("location = \"us-east-1c\"")
      elif re.search("udp_recv_channel {", keyword):
         print("udp_recv_channel {")
         edit.append("udp_recv_channel {")
         print("  port = %s" % myport)
         edit.append("  port = %s" % myport)
      elif re.search("udp_send_channel {", keyword) and not p.match(keyword):
         print("udp_send_channel {")
         edit.append("udp_send_channel {")
         print("  port = %s" % myport )
         edit.append("  port = %s" % myport)
         #compute nodes use host while headnode uses bind
         if nodetype=="ComputeFleet":
            print("  host = %s" % myheadnode_ip )
            edit.append("  host = %s" % myheadnode_ip )
         else:
            print("  bind = %s" % myheadnode_ip )
            edit.append("  bind = %s" % myheadnode_ip )
         print("  ttl= 1" )
         edit.append("  ttl= 1" )
   else:
      print( line.rstrip()) #no change to data here
      edit.append( line.rstrip()) #no change to data here
        
#write new file
      
f = open("/etc/ganglia/gmond.conf",mode="w")
for line in edit:
  f.write(line.rstrip()+"\n") #fix any potential formatting issues
f.close
	
# we should restart things at this point
os.system("systemctl restart gmond.service gmetad.service httpd")

