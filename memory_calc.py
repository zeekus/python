#!/usr/bin/python
#filename: memory_calc.py
#description: checks processes in tree and calculated memory use.
#written for Python 2
import subprocess
import re

def get_procs():
  proc=subprocess.Popen("ps efux",shell=True,stdout=subprocess.PIPE) #get memory fields
  running_procs=proc.stdout.readlines()
  return running_procs
  
 
total_resident_memory_used=0
total_virt_memory_used=0
running_procs=get_procs()
 
for line in running_procs:
  array_of_ps_output=[]
  array_of_ps_output=line.split() 
  matchObj = re.search(r'\d',array_of_ps_output[5]) #look for digits on 5th column of output Resident memory
  matchObj1 = re.search(r'\d',array_of_ps_output[4]) #look for digits on 4th column of output Virtual memory
   
  if matchObj:
   resident_mem=array_of_ps_output[5]
   total_resident_memory_used = ( total_resident_memory_used + int(resident_mem)) 

  if matchObj1:
   vmem=array_of_ps_output[4]
   total_virt_memory_used = ( total_virt_memory_used + int(vmem)) 
     
print "total resident memory used by applications from process tree: " + str(total_resident_memory_used/1024) + " Mb"
print "total virtual memory used by applications from process tree: " + str(total_virt_memory_used/1024) + " Mb"
