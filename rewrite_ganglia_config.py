#!/bin/python3
#filename: rewrite_ganglia_config.py
#description: rewrite the file on the clients holding /etc/ganglia/gmond.conf
#
import os.path
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


config_words_to_target=['cluster {', 'udp_recv_channel {', 'udp_send_channel {']

myheadnode_ip=find_head_node_ip("/opt/slurm/etc/slurm_parallelcluster.conf")  
nodetype=get_cnfconfig_info("/etc/parallelcluster/cfnconfig",'^cfn_node_type')
stack_name=get_cnfconfig_info("/etc/parallelcluster/cfnconfig",'^stack_name')
#ganglia_conf=open('/etc/ganglia/gmond.conf','r')
ganglia_conf=read_file('/etc/ganglia/gmond.conf')
linenum=0

myhit=0
keyword=""

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
   elif myhit ==1: #chnages to configuration file
      if re.search("cluster {", keyword):
         print("cluster {")
         edit.append("cluster {")
         print("  name = \"paralelcluster-" + stack_name + "\"")
         edit.append("  name = \"paralelcluster-" + stack_name + "\"")
         print("  owner=\"unspecified\" ")
         edit.append("  owner=\"unspecified\" ")
         print("  latlong=\"unspecified\" ")
         edit.append("  latlong=\"unspecified\" ")
         print("  url=\"unspecified\" ")
         edit.append("  url=\"unspecified\" ")
      elif re.search("udp_recv_channel {", keyword):
         print("udp_recv_channel {")
         edit.append("udp_recv_channel {")
         print("  port = 8659 ")
         edit.append("  port = 8659 ")
         #print("  bind = " + myheadnode_ip )
         #edit.append("  bind = " + myheadnode_ip )
         #print("  retry_bind = true ") 
         #edit.append("  retry_bind = true ") 
      elif re.search("udp_send_channel {", keyword) and not p.match(keyword):
         print("upd_send_channel {")
         edit.append("upd_send_channel {")
         print("  bind_hostname = yes")
         edit.append("  bind_hostname = yes")
         print("  port = 8659 ")
         edit.append("  port = 8659 ")
         print("  bind = " + myheadnode_ip )
         edit.append("  bind = " + myheadnode_ip )
         print("  ttl= 1" )
         edit.append("  ttl= 1" )
   else:
      print( line.rstrip()) #no change to data here
      edit.append( line.rstrip()) #no change to data here
        
#write new file
      
f = open("/etc/ganglia/gmond.conf",mode="w")
for line in edit
  f.write(line.rstrip())
f.close
	
