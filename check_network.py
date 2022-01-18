#!/usr/bin/python3
#filename: monitor_outbound_links.py
#description: monitor the outbound connection.

import subprocess
import sys

destination="google.com"

def get_next_hop(destination):
  last_line=""
  traceroute_cmd=("traceroute -m 4 %s| awk {'print $2'}" % destination) #get the ip
  proc = subprocess.Popen(traceroute_cmd, shell=True,stdout=subprocess.PIPE)
  traceroute = proc.stdout.readlines()
  for line in traceroute:
      #print(line)
      last_line=line.decode("utf-8").rstrip()

  return last_line

def ping_last(ip):
  ping_cmd=("ping -c 3 %s" % ip) #ping ip
  proc = subprocess.Popen(ping_cmd, shell=True,stdout=subprocess.PIPE)
  ping = proc.stdout.readlines()
  for line in ping:
      print(line)

my_ip=get_next_hop(destination)
print ("ip is '%s'" % my_ip)
ping_last(my_ip)




