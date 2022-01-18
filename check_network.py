#!/usr/bin/python3
#filename: monitor_outbound_links.py
#description: monitor the outbound connection.

import subprocess
import sys

destination="google.com"

def get_next_hop(destination):
  last_line=""
  traceroute_cmd=("traceroute -m 4 %s" % destination) 
  proc = subprocess.Popen(traceroute_cmd, shell=True,stdout=subprocess.PIPE)
  traceroute = proc.stdout.read()
  for line in traceroute:
      last_line=line
  return last_line

#def ping_next_hop():

last_line=get_next_hop(destination)
print (last_line)




