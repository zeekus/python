#!/bin/ython3
#filename: rewrite_gonf.py
#description: rewrite the file on the clients holding /etc/ganglia/gmond.conf
#
import os.path
import re

ganglia_conf=open('/etc/ganglia/gmond.conf','r')

def search_for_end(line):
   regex=re.compile('{') #looking for beginning stanza
   if regex.search(line):
      return 1
   else:
      return 0

def search_for_beginning(line):
   regex=re.compile('}') #closing of stanza
   if regex.search(line):
      return 1
   else:
      return 0

def search_keyword(line,keyword):
   regex=re.compile(keyword) #beginning of config stanza detected
   if regex.search(line):
       print ("match...")
       return 1
   else:
       return 0


words=['cluster {', 'udp_recv_channel {', 'upd_send_channel {']

for line in ganglia_conf:
   #see if we are at a start of stanza

   for word in words:
     keyword=search_keyword(line,word)
     if keyword == 1:
       break

   b1=search_for_beginning(line)
   e1=search_for_end(line)

   print(b1,e1,keyword,line.rstrip())