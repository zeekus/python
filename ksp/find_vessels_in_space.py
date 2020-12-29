#!/usr/bin/python
#filename: switch_vessels.py
#Description: changes active vessel and gets list of vessels availabe in KSP

import krpc
conn = krpc.connect()
vessel = conn.space_center.active_vessel


my_target_vessel="Spotnik"


for vessel in conn.space_center.vessels:
    if vessel.name == my_target_vessel:
        print("Switching focust to {}".format(vessel.name))
        ksc.active_vessel = vessel
    else:
        print("Debug: {} is not the target vessel.".format(vessel.name))
