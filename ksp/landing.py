#landing script for krpc and Kerbal Space Program
#copied from whatdmath github
#soure:  https://github.com/whatdamatch
import math
import time
import krpc

conn = krpc.connect(name='Vessel speed')
vessel = conn.space_center.active_vessel
orbital_frame = vessel.orbit.body.non_rotating_reference_frame
surface_frame = vessel.orbit.body.reference_frame
orbital_speed = conn.add_stream(getattr, vessel.flight(orbital_frame), 'speed')
altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
surface_speed = conn.add_stream(getattr, vessel.flight(surface_frame), 'speed')

long = conn.add_stream(getattr, vessel.flight(orbital_frame), 'longitude')

vessel.control.speed_mode = vessel.control.speed_mode.surface
ap = vessel.auto_pilot
ap.sas = True
ap.sas_mode = ap.sas_mode.retrograde
time.sleep(1)

#angle = 66
angle = 62
position = 0
#set location to ksp
ksc_loc = (1.301492-angle*math.pi/180)
while abs(position - ksc_loc) > 0.01:
    position = (long()+180)*math.pi/180
    print(abs(position - ksc_loc))
    time.sleep(1)

time.sleep(1)
#deorbit
while (vessel.orbit.periapsis_altitude > 0):
        vessel.control.throttle = 1.0
vessel.control.throttle = 0.0

#re-entry slowdown for ships without heatshields
while altitude() > 50000:
    pass
while (orbital_speed() > 1500):
        vessel.control.throttle = 1.0
vessel.control.throttle = 0.0

#when over 500 you can crash keep ship under 500
while altitude() > 10000:
    pass
while (surface_speed() > 500):
        vessel.control.throttle = 1.0
vessel.control.throttle = 0.0
while altitude() > 2000:
    pass
while (surface_speed() > 200):
        vessel.control.throttle = 1.0
vessel.control.throttle = 0.0
#1200M is when our slowdown starts
while altitude() > 1200:
    pass
while altitude() > 50:
    #more than 40m/sec
    if surface_speed() > altitude()/5:
        vessel.control.throttle = 0.95
    elif surface_speed() > altitude()/10:
        vessel.control.throttle = 0.1
    #too slow turn off throttle
    elif surface_speed() > altitude()/15:
        vessel.control.throttle = 0

while altitude() > 2:
    if surface_speed() > 7:
        vessel.control.throttle = 0.5
    else:
        vessel.control.throttle = 0
vessel.control.throttle = 0
