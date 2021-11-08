#!/bin/python3
#filename: rewrite_gonf.py
#description: rewrite the file on the clients holding /etc/ganglia/gmond.conf
#
import os.path
import re

#ganglia_conf=open('/etc/ganglia/gmond.conf','r')
ganglia_conf=open('./gmond.conf','r')

def search_for_opening(line):
   regex=re.compile('{') #looking for beginning stanza
   if regex.search(line):
      return 1
   else:
      return 0

def search_for_close(line):
   regex=re.compile('}') #closing of stanza
   if regex.search(line):
      return 1
   else:
      return 0

def ignore_comments(line):
   regex=re.compile('^#') #closing of stanza
   if regex.search(line):
      return 1
   else:
      return 0

def search_keyword(line,keyword):
   #verify no comment in line
   comment_exist=ignore_comments(line)

   regex=re.compile(keyword) #beginning of config stanza detectet
   if regex.search(line) and comment_exist==0:
       print ("match...")
       return 1
   else:
       return 0


words=['cluster {', 'udp_recv_channel {', 'udp_send_channel {']
match_area=0
match_word="none"

for line in ganglia_conf:
   #see if we are at a start of stanza

   for word in words:
     keyword=search_keyword(line,word)
     if keyword == 1:
       match_area=1    #our search has a match
       match_word=line #set match world for tracking current stanza
       break

   b1=search_for_opening(line)
   e1=search_for_close(line)

   if e1 == 1:  #close match area when '{' detected
      match_word="none"
      match_area=0

   mcast_join_search=search_keyword(line,"mcast_join")
   bind_ip_search=search_keyword(line,"bind = ")


   if match_area ==1 and mcast_join_search == 1:
     print(b1,e1,keyword,match_word,match_area,"") #omit line
   elif match_area ==1 and match_word == "udp_recv_channel {" and bind_ip_search == 1:
     print(b1,e1,keyword,match_area,match_word,".*bind = {host_ip}")
   else:
     print(b1,e1,keyword,match_area,match_word,line.rstrip())
