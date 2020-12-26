#filename: get_telemetry.py
#author: Theodore Knab
#date: 12/25/2020
#description: prints kerbal space program ship telemetry to command line

import krpc
from time import localtime, strftime,sleep
import math # for orbital math
from sys import exit #just get exit routine

def print_telemetry(solidfuel,liquidfuel,lfb_is_active,slb_is_active):
   mytime=(strftime("%d %b %Y %H:%M:%S",localtime())) #timestamp
   print('{1} atmosphere_density: {0:1.0f}'.format(adensity(),mytime))
   print('{1} Altitude          : {0:1.0f}'.format(altitude(),mytime))
   print('{1} vertical_speed    : {0:1.0f} m/s'.format(vs(),mytime) )
   if dynamic_pressure() > 15000 :
     print('{1} Speed             : {0:1.0f} m/s *TOO FAST*'.format(math.trunc(srf_speed()),mytime) )
     print('{1} Dynamic Pressure  : {0:1.0f} psi'.format(math.trunc(dynamic_pressure()), mytime) )
   else:
     print('{1} Speed             : {0:1.0f} m/s'.format(math.trunc(srf_speed()), mytime) )
     print('{1} Dynamic Pressure  : {0:1.0f} psi'.format(math.trunc(dynamic_pressure()),mytime) )
   print('{1} mean_altitude     : {0:1.0f}'.format(altitude(),mytime))
   print('{1} apoapsis          : {0:1.0f}'.format(apoapsis(),mytime))
   #passing local variables to next function
   remaining_fuel(lfb_is_active,slb_is_active,mytime, initial_solidfuel=solidfuel,initial_liquidfuel=liquidfuel)
   #print('universal time to warp is %s' % ut() )

def remaining_fuel(lfb_is_active,slb_is_active,mytime, initial_solidfuel,initial_liquidfuel):
   if solid_fuel_level() > 0.1 and slb_is_active is True:
     print ('{2} solid fuel        : {0:1.0f}% or {1:1.0f}'.format((solid_fuel_level()/initial_solidfuel)*100,solid_fuel_level(),mytime)) #percent remaining
     print ('{1} solid fuel used   : {0:1.0f} %'.format(((initial_solidfuel - solid_fuel_level() ) /initial_solidfuel) * 100,mytime)) #percent used
   if liq_fuel_level() > 0.1 and lfb_is_active is True:
      print ('{2} liquid fuel       : {0:1.0f}% or {1:1.0f}'.format((liq_fuel_level()/initial_liquidfuel)*100,liq_fuel_level(),mytime)) #precent remaining
      print ('{1} liquid fuel used  : {0:1.0f}%'.format(((initial_liquidfuel - liq_fuel_level() ) /initial_liquidfuel) * 100,mytime)) #precent used
   if altitude() > 1000 and solid_fuel_level() < 0.1 and liq_fuel_level() < 0.1:
      exit("We ran out of fuel. :'( Exiting")

def solid_fuel_level():
    solidfuel_level=round(vessel.resources.amount('SolidFuel'),2) #get solid fuel level
    return solidfuel_level

def liq_fuel_level():
    liquidfuel_level=round(vessel.resources.amount('LiquidFuel'),2) #get liquidfuel level
    return liquidfuel_level

def basic_telemetry():
     #get basic telmetry from one second ago and pass it back to main
     #1sp = 1 second in past
     sld_fuel_1sp = solid_fuel_level()
     liq_fuel_1sp = liq_fuel_level()
     vertical_speed_1sp = vs()
     altitude_1sp = altitude()
     latitude_1sp=latitude()
     longitude_1sp=longitude()
     ut_1sp=ut()
     sleep(1)
     if sld_fuel_1sp == solid_fuel_level():
       Sfb_active=False
     else:
       Sfb_active=True
     if liq_fuel_1sp == liq_fuel_level():
       Lfb_active=False
     else:
       Lfb_active=True

     return (Lfb_active,Sfb_active,vertical_speed_1sp,altitude_1sp,latitude_1sp,longitude_1sp,ut_1sp)

def are_we_moving():
    print ("todo")
    #need to figure out how to tell if the ship is moving in space



#connect to krpc
conn = krpc.connect(name='Simple Orbit')

#connect to vessel
vessel = conn.space_center.active_vessel

#connect to vessel object holding info
srf_frame = vessel.orbit.body.reference_frame
#flight_info = vessel.flight()

# Set up streams for telemetry
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
srf_speed = conn.add_stream(getattr, vessel.flight(srf_frame), 'speed')
dynamic_pressure = conn.add_stream(getattr, vessel.flight(srf_frame), 'dynamic_pressure')
gforce = conn.add_stream(getattr, vessel.flight(srf_frame), 'g_force')
liquidfuel=vessel.resources.amount('LiquidFuel') #initial_solidfuel
solidfuel=vessel.resources.amount('SolidFuel') #initial_liquidfuel
aero=conn.add_stream(getattr, vessel.flight(srf_frame), 'aerodynamic_force')
vs=conn.add_stream(getattr, vessel.flight(srf_frame), 'vertical_speed')
adensity=conn.add_stream(getattr, vessel.flight(srf_frame), 'atmosphere_density')
longitude=conn.add_stream(getattr, vessel.flight(), 'longitude')
latitude=conn.add_stream(getattr, vessel.flight(), 'latitude')

while altitude() < 190000:
  (lfb_is_active,sfb_is_active,vspeed1sec_ago,alt1sec_ago,lat1sec_ago,long1sec_ago,ut1sec_ago)=basic_telemetry()
  if lfb_is_active is True or sfb_is_active is True:
     print_telemetry(solidfuel,liquidfuel,lfb_is_active,sfb_is_active)
     sleep(5)
