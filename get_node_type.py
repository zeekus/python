#!/usr/bin/python3
#filename: get_node_type.py
#description: get node type from configuration file
#author: Theodore Knab
#date: 11/8/21

import re

def get_node_type():

  with open('/etc/parallelcluster/cfnconfig') as f:
    lines = f.readlines()
  f.close()

  for line in lines:
    p = re.compile('^cfn_node_type*',re.IGNORECASE)

    if p.match(line):
     return line.strip().split("=")[1]


node_type = get_node_type()

print ("node type is '%s'" % node_type)
