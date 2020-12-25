#!/usr/bin/python
#filename: simple_ksp_launch
#description: basic simple simple ksp launch

#get krpc suff
import krpc

#connect to server aka ksp plugin
conn = krpc.connect()

#get vessel info
vessel = conn.space_center.active_vessel

#set throttle to full
vessel.control.throttle =1

#turn on sas
vessel.control.sas = True

#turn on rcs
vessel.control.rcs = True

#initiate next stage
vessel.control.activate_next_stage()
