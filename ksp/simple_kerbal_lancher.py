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
Python program to bring my Handsfree 1 rocket in orbit in Kerbal Space Program.

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

conn = krpc.connect(name='Simple Kerbel Launcher')
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
turn_start_altitude = 5000
turn_end_altitude = 40000
target_altitude=80000 #target_apoapsis
target_periapsis=75000
gravity_turn_limit=35 # don't go greater than 35 degrees

# Now we're actually starting
vessel = conn.space_center.active_vessel
srf_frame = vessel.orbit.body.reference_frame

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

def print_telemetry(solidfuel,liquidfuel,lfb_active,slb_active):
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
   remaining_fuel(lfb_active,slb_active,mytime, initial_solidfuel=solidfuel,initial_liquidfuel=liquidfuel)
   #print('universal time to warp is %s' % ut() )

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
     #get basic telmetry from one second ago and pass it back to main
     #1sp = 1 second in past
     sfb_1sp = solid_fuel_level()
     lfb_1sp = liq_fuel_level()
     vertical_speed_1sp = vs()
     altitude_1sp = altitude()
     latitude_1sp=latitude()
     longitude_1sp=longitude()
     ut_1sp=ut()
     sleep(1)
     if sfb_1sp == solid_fuel_level():
       sfb_active=False
     else:
       sfb_active=True
     if lfb_1sp == liq_fuel_level():
       lfb_active=False
     else:
       lfb_active=True

     return (lfb_active,sfb_active,sfb_1sp,lfb_1sp,vertical_speed_1sp,altitude_1sp,latitude_1sp,longitude_1sp,ut_1sp)


def dynamic_throttle_control(override):
  if dynamic_pressure()/19000 >1 and vs() > 5000:
      #too fast wasting fuel during ascent
      x = 0.5
  elif dynamic_pressure()/4000 < 0.8 or altitude() < 15000:
      #low resistance or too altitude run at full power
      #gravity sucks
      x = 1
  elif dynamic_pressure()/10000 > 1:
     #moderate atmospheric resistance
     x = .8
  elif override>0:
     x = override
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


#solid booster check
if solid_fuel_level() > 0.1:
  solid_booster_attached=True # we assume one is not attached
  solid_booster_seperated=False
  text3.content = 'SolidFuel on'
else:
  solid_booster_attached=False
  solid_booster_seperated=True
  text3.content = 'LiquidFuel on'

#ativate first stage
vessel.control.throttle = 1
vessel.control.activate_next_stage()
mystage=mystage+1
text4.content = 'Stage {}'.format(mystage)
turn_angle=90 #no turn on start

#ascent loop start
while True:

    (lfb_active,sfb_active,sfb_1sp,lfb_1sp,vs_1sp,alt_1sp,lat_1sp,long_1sp,ut_1sp)=basic_telemetry()

    ####
    ##booster type detection and burn
    ####
    #solid booster attached and with fuel
    if solid_fuel_level() > 0.1 and sfb_active is True:
      text3.content = 'SolidFuel burning' #launches solid fuel
      text4.content = 'SB Stage {}'.format(mystage)
      print('Status            : solid booster active')
      throttle=dynamic_throttle_control(0)
      vessel.control.throttle = throttle
      sleep(1)
    #solid booster attached but fuel is spent
    elif solid_fuel_level() < 0.1 and solid_booster_attached is True:
      text3.content = 'SolidFuel spent' #launches solid fuel
      vessel.control.activate_next_stage()
      sleep(1)
      text3.content = 'SolidFuel dropped' #launches solid fuel
      sleep(1)
      mystage=mystage+1
      text4.content = 'LB Stage {}'.format(mystage)
      solid_booster_attached=False
      print('Status            :solid booster spend ')


    #solid booster absent and liquid fuel is greater than zero
    elif solid_booster_attached is False and liq_fuel_level() > 0.1 and altitude() < turn_end_altitude:
      (lfb_active,sfb_active,sfb_1sp,lfb_1sp,vs_1sp,alt_1sp,lat_1sp,long_1sp,ut_1sp)=basic_telemetry()
      #monitor fuel
      text3.content = 'LiquidFuel burn'
      print('Status            : Liquid Burn Activated')
      throttle=dynamic_throttle_control(0)
      vessel.control.throttle = throttle

      if liq_fuel_level() == lfb_1sp :
         text3.content = 'Out of Fuel'
         vessel.control.activate_next_stage() #out of fuel change stage
         sleep(1)
         mystage=mystage+1
         print('Status            : Out of Fuel')
         text4.content = 'LB Stage {}'.format(mystage)
         #no fuel
    #at heights above turn_end_altitude the gravity turn logic controls the speed
    elif solid_booster_attached is False and liq_fuel_level() > 0.1 and altitude() > turn_end_altitude:
        #get basic telemetry
        (lfb_active,sfb_active,sfb_1sp,lfb_1sp,vs_1sp,alt_1sp,lat_1sp,long_1sp,ut_1sp)=basic_telemetry()
        # print telemetry
        print_telemetry(solidfuel,liquidfuel,lfb_active,sfb_active)

    else:
      text1.content = 'problem detected.'
      text2.content = 'exiting.'
      text3.content = 'out of fuel'
      text4.content = 'Stage {}'.format(mystage)
      sleep(5)
      print('Status            : out of fuel ')
      exit("out of fuel")


    # Gravity turn
    if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
      frac = ((altitude() - turn_start_altitude) /
                (turn_end_altitude - turn_start_altitude))
      new_turn_angle = frac * 90
      if abs(new_turn_angle - turn_angle) > 1:
        turn_angle = round(new_turn_angle)

        if (90-turn_angle) > gravity_turn_limit:
          vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, 90)
          print('Status            : gravity turn angle is {0}'.format(turn_angle))
          text1.content = "Gravity Turn deeper"
          text2.content = "turn is {}".format(90-turn_angle)
        else:
          print('Status            : gravity turn angle limit reached.')
          text2.content = "turn limit reached"


    # Decrease throttle when approaching target apoapsis
    if apoapsis() > target_altitude*0.80 and apoapsis() < target_altitude*.95:
      text1.content = 'nearing TA 80%'
      text2.content = 'throttle 25%'
      throttle=dynamic_throttle_control(.25)
      vessel.control.throttle = throttle
      sleep(1)
      print('Approaching target apoapsis.')
    elif apoapsis() > target_altitude*0.98:
      text1.content = 'nearing TA 95%'
      text2.content = 'throttle off'
      break

#end of ascent loop

#coasting to target_altitude
text1.content = 'Engine off'
text2.content = 'coasting to AP'
vessel.control.throttle = 0
sleep(1)


# Wait until we're on 90% of the apoapsis.
while vessel.flight().mean_altitude < target_altitude*0.90:
   sleep(.2)
   text3.content = 'waiting {}'.format(target_altitude-altitude())

text1.content = 'Starting turn'
text2.content = 'Turning to PG'
print('Turn to prograde and plan circularization burn')

# Plan circularization burn (using vis-viva equation)
text3.content=('Plan cir. burn')
mu = vessel.orbit.body.gravitational_parameter
r = vessel.orbit.apoapsis
a1 = vessel.orbit.semi_major_axis
a2 = r
v1 = math.sqrt(mu*((2./r)-(1./a1)))
v2 = math.sqrt(mu*((2./r)-(1./a2)))
delta_v = v2 - v1
node = vessel.control.add_node(
    ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

# Calculate burn time (using rocket equation)
F = vessel.available_thrust
Isp = vessel.specific_impulse * 9.82
m0 = vessel.mass
m1 = m0 / math.exp(delta_v/Isp)
flow_rate = F / Isp
burn_time = (m0 - m1) / flow_rate

# Orientate ship
text4.content=("Orienting ship.")
print('Orientating ship for circularization burn')
vessel.auto_pilot.reference_frame = node.reference_frame
vessel.auto_pilot.target_direction = (0, 1, 0)
vessel.auto_pilot.wait()

# Wait until burn
print('Waiting until circularization burn')
burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
lead_time = 3
conn.space_center.warp_to(burn_ut - lead_time)

# Execute burn
print('Ready to execute burn')
time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
while time_to_apoapsis() - (burn_time/2.) > 0:
    sleep(0.1)
print('Executing burn')
vessel.control.throttle = 1.0
sleep(burn_time - 0.5)
print('Fine tuning')
vessel.control.throttle = 0.05
remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)
while remaining_burn()[1] > 1:
    sleep(0.1)
vessel.control.throttle = 0.0
node.remove()

text1.content = 'Success'
text2.content = 'Orbital burn complete'

#get basic telemetry
(lfb_active,sfb_active,sfb_1sp,lfb_1sp,vs_1sp,alt_1sp,lat_1sp,long_1sp,ut_1sp)=basic_telemetry()

# print telemetry
print_telemetry(solidfuel,liquidfuel,lfb_active,sfb_active)


#
# text.content = 'Extend solar panels'
#  vessel = conn.space_center.active_vessel
#  for solar_panel in vessel.parts.solar_panels:
#      print (solar_panel.state)
#      solar_panel.deployed=True

text3.content = 'Welcome to orbit!'
text4.content = 'Done'
print('Welcome to orbit!')
