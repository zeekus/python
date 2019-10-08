#!/usr/bin/python3
#filename: guided_mediation.py
#description: replacing your meditation guide with a shell script.
#author: Teddy Knab
#date: 10/8/2019

import sys,subprocess,time,os.path
import argparse

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='A simple shell script mediation helper.')
parser.add_argument('--timeblock','-b', type=str,help='-b time_available. Takes time time_available in as input. ')

args = parser.parse_args()
time_available = args.timeblock
time_available = int(time_available)

main_wait=time_available-6

print("we will be practicing %s" % str(time_available) )
print("The main mediation time will be %s" % str(main_wait))


###################
def minute_counter(mins):
###################
    print ("#######################")
    print ( str(mins) + " " + "mins")
    seconds = ( 60 * mins )
    print ("sleeping " + str(seconds) + " " + "seconds")
    print ("#######################")
    time.sleep(seconds)

############################################
#modify this if you want to change the waits (x) times 60 seconds
############################################
wait_times_for_each_sequence=[.25,#1
                              .25,#2
                               2, #3
                              .5, #4
                               1, #5
                               main_wait ,#6 main meditation sequence
                               1, #7
                               0] #8 mediation sequences

############################################
#modify this if you want to change the words
############################################
mediation_playbook=["1. Get settled, close your eyes",
        "2. bring your attention to the body",
        "3. scan through the body from head to toe",
        "4. set your intentions for this meditation session",
        "5. attention on the space around you",
        "6. attention on your breathing. count your breaths. let your mind wander if it wants to.",
        "7. attention on the space around you",
        "Thank yourself. Thank the Universe. open your eyes."]

count=0
for sequ in wait_times_for_each_sequence:



  print (mediation_playbook[count]) #counter for mediation_playbook
  cmd_echo="echo \'" + mediation_playbook[count] + "\'"

  if os.path.exists("/usr/bin/festival"):
    #if festival use it
    cmd_talk="festival --tts"
    status = subprocess.call(cmd_echo + "|" + cmd_talk , shell=True)
  elif os.path.exists("/usr/bin/espeak"):
    cmd_talk="espeak -a 500 -p 1 "
    status = subprocess.call(cmd_echo + "|" + cmd_talk , shell=True)
  else:
     print ("sorry this program will not work without festival or espeak. Please install one.\n")
     sys.exit(1)

  minute_counter(sequ)
  print (sequ)
  count = count + 1
