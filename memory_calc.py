#!/usr/bin/python
#filename: memory_calc.py
#description: checks processes in tree and calculated memory use.
import subprocess
import re
list_of_processes=[]

def get_processes:
  proc=subprocess.Popen("ps efux",shell=True,stdout=subprocess.PIPE) #get memory fields
  running_procs=proc.stdout.readlines()
  return running_procs
  
 
 total_mem_used=0
 running_procs=get_processes()
 
 for line in running_procs:
   array_of_ps_output=[]
   array_of_ps_output=line.split() 
   matchObj = re.search(r'\d',array_of_ps_output[5]) #look for digits on 5th column of output
   
   if matchObj:
     resident_mem=array_of_ps_output[5]
     total_mem_used = ( total_mem_used + int(resident_mem)) 
     
 print "total memory used by applications : " + str(total_mem_used/1024) + " Mb"


