#!/usr/bin/python
import subprocess
import sys
whitelist=['156.119.190.184','156.119.195.42','10.162.61.79','127.0.0.1'] #base whitelist
whitelist.append('149.101.1.118') #DOJ added 8/15/2017


##############################
#variables to change
##############################
admin_email="ted_knab@mdb.uscourts.gov" # to and from email address
my_host="ecf.mdb.uscourts.gov" 
carbon_copy_email=["john_held@mdb.uscourts.gov","Peter_Smolianski@mdb.uscourts.gov"]


#for x in whitelist:
#    print "debug: white listed hosts - " + x

blockvalue=200 #default 2
alertvalue=5
proc = subprocess.Popen("netstat -ntu | awk '{print $5}' | cut -d: -f1 | grep -v '[ervers|ddress]' |sort | uniq -c | sort -n", shell=True,stdout=subprocess.PIPE)
running = proc.stdout.read()
sorted_ips_running = running.split('\n')

#########################################
#functions
#########################################
def block_ip(ip):

  #check for valid ip
  oct1,oct2,oct3,oct4=ip.split(".")
 
  print "debug blocking " + oct1 + "." + oct2 + "." + oct3 + "." + oct4 

  if ( oct1>0 and len(ip)>8):
     #print "debug ok4"
     print"running firewall block rule..."
     mycmd = "/sbin/iptables -I INPUT 1 -s " + ip + " -j DROP"
     print mycmd
     subprocess.Popen(mycmd ,shell=True,stdout=subprocess.PIPE)
#########################################

##################################################
def write_message_to_log(first_part,second_part):
##################################################
   print "debug write_message_to_log function\n"
   d=get_date("2") #dates with seconds
   f = open('/var/tmp/logfile_block_me.txt', 'a')
   if first_part=="":
     #log entry without colon 
     line_string = d + "," + str(second_part) + "\n"
   else:
     line_string = d + ":" + first_part + " " + str(second_part) + "\n"
   
   f.write(line_string)
   f.close()
   print "debug write message to log finished.\n"

def get_logs_of_connections(ip):
  #todo
  exit
#########################################

##################################################
def get_date(a):
##################################################
 import datetime

 if a == "1":
   #get date with seconds
   now = datetime.datetime.now()
   d = now.strftime("%Y-%m-%d_%H:%M:%S ")
   ##d="2009-12-10" #debug date static

 elif a=="2":
   now = datetime.datetime.now()
   d = now.strftime("%Y-%m-%d,%H:%M:%S")
 else:
   #regular date for email
   d = datetime.date.today() #dyanmic
   ##d="2009-12-10" #debug date static

 #print "debug get_date date is " + str(d)
 return str(d) #return as string
##################################################


##################################################
def write_to_mailclient(mycount,ip):
##################################################
 print "did we get this far"
 import smtplib
 import re

 cc_list_count=0
 cc_header=[] #carbon copy header info for email
 
 for email_address in carbon_copy_email:
   cc_list_count=cc_list_count+1
   cc_header.append("cc: <" + str(email_address) + ">\r\n")

 new_msg=[] #new message

 #message header info
 fromaddr = ("From: " + my_host + " <" + str(admin_email) + ">" )
 toaddr=("To: <" + str(admin_email) + ">" )

 print "\t Attempting to send message...\n"
 today=get_date("any")
 subject="Subject: blocking ip " + ip 
 total_addrs=[] #mulple email addresses
 total_addrs.append(admin_email)
 #if we have carbon copy info add it in
 if cc_list_count>0:
   for cc_email in carbon_copy_email:
     total_addrs.append(cc_email)
 

 header= fromaddr + "\r\n" 
 header= header + toaddr + "\r\n" 
 if cc_list_count>0:
   for cc_email in cc_header:
     header= header + cc_email  
 header= header + subject + "\r\n"  
   
 print "debug: (header)  " + header 
 

 new_msg = (header + "Hello,\r We detected an LARGE AMOUNT of tcp connections to " + my_host + "  There are " + mycount + " connections from " + ip + " so we blocked them.\r\n\r\n")
 body=""
 body = body + "************************ \r\n"
 ###########
 #add header and subject to the message
 ###########
 body = new_msg + body
 ###########
 #add signiture to mail message
 ###########
 body = body + "##########\r\nUSBC\r\nMDB Systems\r\nTel: 410-962-0834\r\n###########"
 #####
 #end of message
 #####

 #tmp1=" address " + admin_email 
 #tmp2=str(len(body)) + " characters" 
 #write_message_to_log(tmp1,tmp2)  

 print "\t....Attempting to send the message to " + admin_email
 print "\t....Opening connection to server...\n"
 server = smtplib.SMTP('smtp.uscourts.gov')
 server.set_debuglevel(1)
 print "\t....sending email\n"
 server.sendmail(fromaddr, total_addrs, body)
 print "\t....attempting to end connection with the server\n"
 server.quit()


#########################################


#########################################
#MAIN AREA
#remove whitelisted ips from list
for r in sorted_ips_running:
  match=0
  con=r.split()

  if len(con)==2:
    for wip in whitelist:
      if wip==con[1]:
        #print "match found " + wip + " = " + con[1]
        match=1

    if match==0:
       #print "no match for ip " +  con[1]
       if int(con[0]) > blockvalue:
         #process new firewall rules
         tmp1=con[0] + " TCP connections "
         tmp2=" from " + con[1] 
         print "appending values " + tmp1 + ":" + tmp2 + " to list"
        

         tmp3=con[1] + "," + con[0] #format of log file is ALERT,IP
         write_message_to_log("BLOCKED",tmp3)

         print "sending message " + tmp1 + ":" + tmp2 + " to list"
         write_to_mailclient(con[0],con[1])
         #send email about blocking before we block it
         print "BLOCKING " + str(con[1])+ " - " + str(con[0]) 
         block_ip(str(con[1]))
       elif int(con[0]) > alertvalue:
         print "ALERT " + str(con[1])+ " - " + str(con[0]) 
         a=get_date("2")#standard format
         tmp_info="ALERT," + str(con[1])+ "," + str(con[0])
         write_message_to_log("",tmp_info)
       else:
         a=get_date("2")#standard format
         print str(a) + "," + str(con[0]) +  ",connections from," + str(con[1]) 
