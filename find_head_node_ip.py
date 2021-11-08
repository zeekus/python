#!/usr/bin/python
#filename: find_head_node_ip.py
#author: Theodore Knab
#date: 11/8/21
#description: get hode node IP from the slurm config
#bash equivalent get_head_nodeip=$( cat /opt/slurm/etc/slurm_parallelcluster.conf | grep -i ^SlurmctldHost | sed -e s/.*\(//g | sed -e s/\)//g)

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
        return line.split("=")[1].split("(")[1].split(')')[0] #trippl split on line 1. get second field after "=', 2. get second field after '(', 3. drop last ")' character

myvalue=find_head_node_ip("/opt/slurm/etc/slurm_parallelcluster.conf")
print(myvalue)
