#!/usr/local/bin/python3.7 
#author: Theodore Knab
#description: creates a connection the hosts in the list. Drops user off at root prompt if automated_update_mode not 1. 
#file: connect_to_host_and_run_update.py

import pexpect
import os 

list_of_hosts=["server1","server2","server3" ]
automated_update_mode=0 #no automated upates

PROMPT_LIST=["# ",">>>", "> ", "\$ "]

############
def send_command(child,cmd):
############
  child.sendline(cmd)
  child.expect(PROMPT_LIST)
  print("debug: command and result")
  print(child.before.decode("utf-8"))

############
def send_sudo(child,cmd,mypass):
############
  child.sendline(cmd)
  child.expect('password for') #password prompt
  print(child.before.decode("utf-8"))

  child.sendline(mypass)
  print(child.before.decode("utf-8"))

  child.expect(PROMPT_LIST)
  print(child.before.decode("utf-8"))

############
def connect_to_host(login,mypass,server,automated_update_mode):
############
  print ("...connecting to " + str(host) + " using login of " + str(login) )
  ssh_newkey_message=("Are you sure you want to continue connecting")
  connect_string=str("/usr/bin/ssh -q " + login + "@" + server)
  print ("...using " + connect_string)
  child_process= pexpect.spawn(connect_string)
  expected_strings=[pexpect.TIMEOUT, ssh_newkey_message, "[P|p]assword:"] + PROMPT_LIST #strings we expect to see stored as a long list
  ret = child_process.expect(expected_strings ) #what we expect on return
  print(f"Return value Ret: {ret}")  
   
  if ret ==0 : #timeout seen
    print("[-] Error connecting timeout message recieved..") 
  if ret ==1 : #ssh key needed
    child_process.sendline("yes")  #ssh key needed to be accepted
    ret2 = child_process.expect([pexpect.TIMOUT, "[P|p]assword:"] )
    if ret2 == 0:
      print("[-] Error connecting") 
      return
  if ret == 2: #password prompt seen typing in password
    print ("password is being requsted")
    child_process.sendline(mypass)
    
  if ret > 2: #all good running commands
    print ("sucessful connection running..")
    send_command(child_process,"touch ~/.hushlogin") #hushlogin
    send_sudo(child_process,"sudo su -", mypass) #type sudo and give pass

    if automated_update_mode != 1:
      child_process.interact() #to break out to in active shell
    else:
      send_command(child_process,"yum update -y") #run update
      #logout of root user
      child_process=logout(child_process)

      #logoff 
      child_process=logout(child_process)


    return child_process

def logout(child_process):
    #logout of user shell
    child_process.sendcontrol("d")
    print(child_process.before.decode("utf-8"))
    return child_process


def getpass(prompt="Password: "):
  #gets password with no stdin on screen
  import termios, sys
  fd = sys.stdin.fileno()
  old = termios.tcgetattr(fd)
  new = termios.tcgetattr(fd)
  new[3] = new[3] & ~termios.ECHO          # lflags
  try:
    termios.tcsetattr(fd, termios.TCSADRAIN, new)
    passwd = input(prompt)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old)
  return passwd


############
#main
############
login=(os.getlogin()) #get login of current user
#mypass=input(f"{login} Please Type in your password:") #get pass
mypass=getpass()

for host in list_of_hosts:
  connect_to_host(login,mypass,host,automated_update_mode)


