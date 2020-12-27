"""
kRPC simple kerbal_launcher.py
Contributors: Theodore Knab

credits: Anton Petrov 'What da Math' for pointing in me in the direction.
source https://github.com/whatdamath/KerbalSpaceprogram

Requirements: If in career mode of KSP, you need to upgrade the tracking station.
              A level 2 tracking facilty is needed to track retrograde and prograde orbital paths.

MyShip: 3 stages:  cost 11,457
     Stage1: 2 RT-10 solid boosters on the side for the first stage. 1-5000
     Stage2: 1 LV-T45 attached to 3 FL-T200 Tanks 5000-20000
     Final Stage: 1 LV-T45 attached to 1 FL-T200 Tank 20000 - orbit

Description:
Python program to bring my rocket into orbit in Kerbal Space Program.

Limitations: During the Orbit circularization it needs a lot of fuel.
Rockets with a lot of mass may fail to reach orbit with this script.

To run this KSP kRPC Python program you need:
- Kerbal Space Program (tested in 1.5.12335) (Linux Player)
- kRPC 0.4.8 (https://mods.curse.com/ksp-mods/kerbal/220219-krpc-control-the-game-using-c-c-java-lua-python)
  Use the install guide on https://krpc.github.io/krpc/getting-started.html
- I've also installed the Python client library (https://pypi.python.org/pypi/krpc)
- Python 3.8 (https://www.python.org/download/releases/3.8/)
"""
import krpc
from time import localtime, strftime, sleep
import math # for orbital math
from sys import exit #for exit routine

conn = krpc.connect(name='Simple Kerbal Launcher')
canvas = conn.ui.stock_canvas

# Get the size of the game window in pixels
screen_size = canvas.rect_transform.size

# Add a panel to contain the UI elements
panel = canvas.add_panel()

# Position the panel on the left of the screen
#ksp conversion center of screen is 0,0
rect = panel.rect_transform
screen_x=(screen_size[0]/2)-200
print ('screen size is {0} x is {1} y is {2}'.format(screen_size,screen_size[0],screen_size[1]))

# Settings for text in the panel on screen
 #14 character limit in each line of the text box with size 20 text
text1=panel.add_text('Simple Kerbal')
text1.rect_transform.position = (0, 20)
text1.color = (1, 2, 1)
text1.size = 20
text2 = panel.add_text('Launcher')
text2.rect_transform.position = (0, 0)
text2.color = (1, 2, 1)
text2.size = 20
text3 = panel.add_text('started')
text3.rect_transform.position = (0, -20)
text3.color = (1, 2, 1)
text3.size = 20
text4 = panel.add_text('')
text4.rect_transform.position = (0, -40)
text4.color = (1, 2, 1)
text4.size = 20
rect.position=(-screen_x,300 )

sleep(2)


# Some values for altitudes
turn_start_altitude = 10000
turn_end_altitude = 40000
target_altitude=225000 #target_apoapsis
target_periapsis=80000
gravity_turn_limit=40 # don't go lower than 35 degrees
                      # With heavier ships setting a gravity turn limit of 45-60 may prevent orbital failures.

# Now we're actually starting
vessel = conn.space_center.active_vessel
refframe = vessel.orbit.body.reference_frame

# Set up streams for telemetry
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
srf_speed = conn.add_stream(getattr, vessel.flight(refframe), 'speed')
dynamic_pressure = conn.add_stream(getattr, vessel.flight(refframe), 'dynamic_pressure')
gforce = conn.add_stream(getattr, vessel.flight(refframe), 'g_force')
liquidfuel=vessel.resources.amount('LiquidFuel') #initial_liquidfuel cummulative amount
solidfuel=vessel.resources.amount('SolidFuel')   #initial_solidfuel  cummulative amount
aero=conn.add_stream(getattr, vessel.flight(refframe), 'aerodynamic_force')
vs=conn.add_stream(getattr, vessel.flight(refframe), 'vertical_speed')
longitude=conn.add_stream(getattr, vessel.flight(), 'longitude')
latitude=conn.add_stream(getattr, vessel.flight(), 'latitude')
position = conn.add_stream(vessel.position, refframe)
#top to bottom see https://krpc.github.io/krpc/cnano/api/space-center/parts.html
stage1_resources = vessel.resources_in_decouple_stage(stage=1, cumulative=False) #just first stage liquidfuel
liq_fuel1 = conn.add_stream(stage1_resources.amount, 'LiquidFuel')
liquidfuel_stage1=liq_fuel1() #intial stage 1 liquid fuel

def print_telemetry(solidfuel,liquidfuel,lfb_active,slb_active,status):
   mytime=(strftime("%d %b %Y %H:%M:%S",localtime())) #timestamp
   print('{1} status            : {0}'.format(status,mytime))
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
   remaining_fuel(lfb_active,slb_active,mytime, initial_solidfuel=solidfuel,initial_liquidfuel=liquidfuel)
   #print('universal time to warp is %s' % ut() )

def check_if_liquid_booster_is_empty(mystage):

      value_of_thrust_avail=vessel.available_thrust
      print("debug1: check_if_liquid_booster_is_empty  value of thrust available {}".format(value_of_thrust_avail))

      status="same" #same as before
      (lfb_active,sfb_active,sfb_past,lfb_past,vs_past,alt_past,lat_past,long_past,ut_past)=basic_telemetry()

      #no fuel left on current liquid stage
      if liq_fuel_level() == lfb_past :
         vessel.control.activate_next_stage() #drop stage
         if vessel.available_thrust == 0: #no thurst will be register if the booster is not active
           print("debug2: check_if_liquid_booster_is_empty value of thrust available {}".format(0))
           vessel.control.activate_next_stage() #activate booster
         mystage=mystage+1
         status="out of fuel on liquid fuel booster"
      return (status,mystage)


def remaining_fuel(lfb_active,slb_active,mytime, initial_solidfuel,initial_liquidfuel):
   if solid_fuel_level() > 0.1 and slb_active is True:
     print ('{2} solid fuel        : {0:1.0f}% or {1:1.0f}'.format((solid_fuel_level()/initial_solidfuel)*100,solid_fuel_level(),mytime)) #percent remaining
     print ('{1} solid fuel used   : {0:1.0f} %'.format(((initial_solidfuel - solid_fuel_level() ) /initial_solidfuel) * 100,mytime)) #percent used
   if liq_fuel_level() > 0.1 and lfb_active is True:
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
     mydelay=.5
     #get basic telmetry from 'mydelay' seconds ago and compare with now
     sfb_past = solid_fuel_level()
     lfb_past = liq_fuel_level()
     vertical_speed_past = vs()
     altitude_past = altitude()
     latitude_past=latitude()
     longitude_past=longitude()
     ut_past=ut()
     sleep(mydelay)
     if sfb_past == solid_fuel_level():
       sfb_active=False
     else:
       sfb_active=True
     if lfb_past == liq_fuel_level():
       lfb_active=False
     else:
       lfb_active=True

     return (lfb_active,sfb_active,sfb_past,lfb_past,vertical_speed_past,altitude_past,latitude_past,longitude_past,ut_past)


def dynamic_throttle_control(override):

  if override > 0: #manual overide
      x = override
  elif dynamic_pressure()/4000 < 0.8 or altitude() < 10000:
     #low resistance or too altitude run at full power
     #gravity sucks
     x = 1
  elif dynamic_pressure()/19000 >1 and vs() > 10000:
      #too fast wasting fuel during ascent
      x = 0.5
  elif dynamic_pressure()/10000 > 1:
     #moderate atmospheric resistance
     x = .8
  else:
     x =.75

  return x # we need to know the thottle settings

vessel.auto_pilot.engage() #enable auto_pilot

# Launch Countdown
for i in range ( 3, 0 , -1):
  text1.content = ('%s...' % i)
  print('%s...' % i)
  sleep(1)

# Set Pitch = Heading 90/90 is stright up
text1.content = 'Autopilot enabled'
text2.content = 'Engines:on'
text3.content = 'Pitch 90/90'
text4.content = 'Stage 0'

print('Set pitch straight up. 90/90')
sleep(1)
#90,90 is stright up
#90,45 is west
#90,270 is east
vessel.auto_pilot.target_pitch_and_heading(90,90)# 90,90


print('Launch!')

mystage=0 # tracking the stage
mystage0_mass = vessel.mass


#solid booster check
if solid_fuel_level() > 0.1:
  solid_booster_attached=True # we assume one is not attached
  solid_booster_seperated=False
  text3.content = 'SolidFuel on'
else:
  solid_booster_attached=False
  solid_booster_seperated=True
  text3.content = 'LiquidFuel on'

#ativate first stage engage boosters
vessel.control.throttle = 1
vessel.control.activate_next_stage()
mystage=mystage+1
text4.content = 'Stage {}'.format(mystage)
mystage1_mass = vessel.mass
turn_angle=90 #no turn on start

loop_counter=0 #loop counter

#ascent loop start
while True:

    status="loop {}".format(loop_counter)
    #load basic telemtry values
    (lfb_active,sfb_active,sfb_past,lfb_past,vs_past,alt_past,lat_past,long_past,ut_past)=basic_telemetry()


    ####
    ##booster type detection and burn
    ####
    #solid booster attached and with fuel
    if solid_fuel_level() > 0.1 and sfb_active is True:
      text3.content = 'SolidFuel burning' #launches solid fuel
      text4.content = 'SB Stage {}'.format(mystage)
      throttle=dynamic_throttle_control(0)
      vessel.control.throttle = throttle
      status= 'Solid Booster Active. Throttle set at {}'.format(throttle)
    #solid booster attached but solid booster fuel is spent
    elif solid_fuel_level() < 0.1 and solid_booster_attached is True:
      text2.content = 'SolidFuel spent' #launches solid fuel
      vessel.control.activate_next_stage()
      text3.content = 'SolidFuel dropped' #launches solid fuel
      mystage=mystage+1
      text4.content = 'LB Stage {}'.format(mystage)
      solid_booster_attached=False
      status= 'Solid Booster spent. next_stage pressed'

    #solid booster absent and liquid fuel is greater than zero
    elif solid_booster_attached is False and liq_fuel_level() > 0.1:
      text2.content = 'LiquidFuel burn'
      throttle=dynamic_throttle_control(0)
      vessel.control.throttle = throttle
      status= 'Liquid Booster Active throttle set at {}'.format(throttle)
      (status1,mystage1)=check_if_liquid_booster_is_empty(mystage)
      if status1 != "same":
        #out of Fuel booster cycled
        status=status1
        text3.content=status
        mystage=mystage1
        text4.content = 'LB Stage {}'.format(mystage)

    #no fuel
    #at heights above turn_end_altitude the gravity
    # elif solid_booster_attached is False and liq_fuel_level() > 0.1 and altitude() > turn_end_altitude:
    #     status= 'Gravity Turn completed. Climbing.'
    else:
      text1.content = 'Fuel problem.'
      text2.content = 'exiting.'
      text3.content = status
      text4.content = 'Stage {}'.format(mystage)
      (lfb_active,sfb_active,sfb_past,lfb_past,vs_past,alt_past,lat_past,long_past,ut_past)=basic_telemetry()
      status='Error No fuel.'
      print_telemetry(solidfuel,liquidfuel,lfb_active,sfb_active,status) #print telemetry
      sleep(5)
      exit("out of fuel")

    # print telemetry and status messages defined above
    print_telemetry(solidfuel,liquidfuel,lfb_active,sfb_active,status)

    # Gravity turn logic
    if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
      frac = ((altitude() - turn_start_altitude) /
                (turn_end_altitude - turn_start_altitude))
      new_turn_angle = frac * 90
      if abs(new_turn_angle - turn_angle) > 1: #only add turn when greater than 1
        turn_angle = round(new_turn_angle) #new turn angle

        #without a limit the ship will never reach orbit. Gravity will pull greater the ascent vector.
        if (90-turn_angle) > gravity_turn_limit: #limit max turn angle to pre-set
          vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, 90)
          status= 'Gravity Turn Active. Pitch at {}'.format(90-turn_angle)
          text1.content = "Gravity Turn deeper"
          text2.content = "Pitch is {0}".format(90-turn_angle)
          (lfb_active,sfb_active,sfb_past,lfb_past,vs_past,alt_past,lat_past,long_past,ut_past)=basic_telemetry()
          print_telemetry(solidfuel,liquidfuel,lfb_active,sfb_active,status) #print telemetry
    #end of Gramvity turn logic

    # slow ship when we get near the desired apoapsis. This helps prevent overshoots.
    if apoapsis() > target_altitude*0.80 and apoapsis() < target_altitude*.95:
      status="80% of target_altitude {} passed".format(target_altitude*80)
      text1.content = 'TA 80%'
      text2.content = 'throttle 25%'
      throttle=dynamic_throttle_control(.25)
      vessel.control.throttle = throttle
      (lfb_active,sfb_active,sfb_past,lfb_past,vs_past,alt_past,lat_past,long_past,ut_past)=basic_telemetry()
      print_telemetry(solidfuel,liquidfuel,lfb_active,sfb_active,status)
    elif apoapsis() > target_altitude*0.95:
      status="95% of target_altitude {} passed throttle off".format(target_altitude*95)
      text1.content = 'nearing TA 95%'
      text2.content = 'throttle off'
      (lfb_active,sfb_active,sfb_past,lfb_past,vs_past,alt_past,lat_past,long_past,ut_past)=basic_telemetry()
      print_telemetry(solidfuel,liquidfuel,lfb_active,sfb_active,status)

      #coasting to target_altitude
      text1.content = 'Engine off'
      text2.content = 'coasting to AP'
      vessel.control.throttle = 0
      sleep(1)
      #############################
      #drop extra Fuel
      ############################
      if liquidfuel_stage1 < liquidfuel:
          vessel.control.activate_next_stage()
          if vessel.available_thrust == 0: #no thurst will be register if the booster is not active
             vessel.control.activate_next_stage() #try again
          sleep(1)
      #todo: need some logic to check if the current stage of booster is almost spent and dump it if it is
      break

loop_counter+=1
#end of ascent loop

######################################################################################################
#####Warning: This area is buggy if the LiquidFuel booster doesn't have enough fuel to an orbital circularization
##### It works fine if the we are on the last stage with enough fuel.
######################################################################################################

print_counter=0 #print counter to reduce the logging
# Wait until we're on 90% of the apoapsis.
while vessel.flight().mean_altitude < target_altitude*0.90:
   if print_counter % 30 == 0: #print every 15 seconds
     text2.content = 'wait {}'.format(print_counter)
     text3.content = '{}'.format(target_altitude-altitude())

     status="Coasting to AP with Engine off until {} loop counter is {}".format(target_altitude*0.90,loop_counter)
     (lfb_active,sfb_active,sfb_past,lfb_past,vs_past,alt_past,lat_past,long_past,ut_past)=basic_telemetry()
     print_telemetry(solidfuel,liquidfuel,lfb_active,sfb_active,status)
   sleep(.5)
   print_counter+=1
   loop_counter+=1

status='prograde turn and oribital circularization'

text1.content = 'Starting turn'
text2.content = 'prograde'
text3.content = 'turn'
text4.content = ''
(lfb_active,sfb_active,sfb_past,lfb_past,vs_past,alt_past,lat_past,long_past,ut_past)=basic_telemetry()
print_telemetry(solidfuel,liquidfuel,lfb_active,sfb_active,status)


# Plan circularization burn (using vis-viva equation)
text4.content=('Plan cir. burn')
mu = vessel.orbit.body.gravitational_parameter
print("debug mu: {}".format(mu))
r = vessel.orbit.apoapsis
print("debug r: {}".format(r))
a1 = vessel.orbit.semi_major_axis
print("debug a1: {}".format(a1))
a2 = r
v1 = math.sqrt(mu*((2./r)-(1./a1)))
print("debug v1: {}".format(v1))
v2 = math.sqrt(mu*((2./r)-(1./a2)))
print("debug v2: {}".format(v2))
delta_v = v2 - v1
print("debug delta_v: {}".format(delta_v))
node = vessel.control.add_node(
    ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

# Calculate burn time (using rocket equation)
F = vessel.available_thrust
print("debug F: {}".format(F))
Isp = vessel.specific_impulse * 9.82
print("debug Isp: {}".format(Isp))
m0 = vessel.mass
print("debug m0: {}".format(m0))
m1 = m0 / math.exp(delta_v/Isp)
print("debug m1: {}".format(m1))
flow_rate = F / Isp
print("debug flow_rate: {}".format(flow_rate))
burn_time = (m0 - m1) / flow_rate
print("debug burn_time: {}".format(burn_time))

# Orientate ship
status='Orienting ship for orbital burn'
(lfb_active,sfb_active,sfb_past,lfb_past,vs_past,alt_past,lat_past,long_past,ut_past)=basic_telemetry()
print_telemetry(solidfuel,liquidfuel,lfb_active,sfb_active,status)
text1.content=("Orienting ship.")
vessel.auto_pilot.reference_frame = node.reference_frame
vessel.auto_pilot.target_direction = (0, 1, 0)
status='Autopilot wait set'
print_telemetry(solidfuel,liquidfuel,lfb_active,sfb_active,status)
vessel.auto_pilot.wait()

# Wait until burn
status='Waiting until ready to exucute circularization burn'
(lfb_active,sfb_active,sfb_past,lfb_past,vs_past,alt_past,lat_past,long_past,ut_past)=basic_telemetry()
print_telemetry(solidfuel,liquidfuel,lfb_active,sfb_active,status)
burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
lead_time = 5 #added 5 seconds from default of 3
conn.space_center.warp_to(burn_ut - lead_time)

# Execute burn
status='Executing orbital circularization burn'
(lfb_active,sfb_active,sfb_past,lfb_past,vs_past,alt_past,lat_past,long_past,ut_past)=basic_telemetry()
print_telemetry(solidfuel,liquidfuel,lfb_active,sfb_active,status)
time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
while time_to_apoapsis() - (burn_time/2.) > 0:
    sleep(0.1)
vessel.control.throttle = 1.0
sleep(burn_time - 0.5)


vessel.control.throttle = 0.05
status='Fine tuning orbital circularization burn with throttle of 0.05'
(lfb_active,sfb_active,sfb_past,lfb_past,vs_past,alt_past,lat_past,long_past,ut_past)=basic_telemetry()
print_telemetry(solidfuel,liquidfuel,lfb_active,sfb_active,status)
remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)
while remaining_burn()[1] > 1:
    sleep(0.1)
vessel.control.throttle = 0.0
node.remove()

status="stable orbit sucessfully completed. Congratulations."
(lfb_active,sfb_active,sfb_past,lfb_past,vs_past,alt_past,lat_past,long_past,ut_past)=basic_telemetry()
print_telemetry(solidfuel,liquidfuel,lfb_active,sfb_active,status)

text1.content = 'Success'
text2.content = 'Orbital burn complete'

#
# text.content = 'Extend solar panels'
#  vessel = conn.space_center.active_vessel
#  for solar_panel in vessel.parts.solar_panels:
#      print (solar_panel.state)
#      solar_panel.deployed=True

text3.content = 'Welcome to orbit!'
text4.content = 'Done'
sleep(5)
print('Welcome to orbit!')
