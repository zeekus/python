#!/usr/bin/jruby
#filename: json_setup_screen_points.rb
#description: gets screen points and puts them in json file for later. The values and keys are used in auto_jump_loop.rb
require 'java'
require 'json'

java_import 'java.awt.Robot'            #robot class
java_import 'java.awt.event.InputEvent' #moves mouse and typing
java_import 'java.awt.MouseInfo'        #get location of mouse
java_import 'java.awt.Color'            #get color of pixel at location on screen
java_import 'java.awt.event.KeyEvent'   #presing keys

def speak(robot,message,counter)
  if counter == 1
    system("echo #{message} | espeak > /dev/null 2> /dev/null") #supress messages
    robot.delay(2000) #2 second delay
  else 
    system("echo #{message} | espeak > /dev/null 2> /dev/null") #supress messages
    robot.delay(1000) #1 second delay
  end
end

def get_color_of_pixel(robot,x,y)
  mycolors=robot.getPixelColor(x,y)
  r = mycolors.red
  g = mycolors.green
  b = mycolors.blue
  print "get_color_of_pixel: at [#{x},#{y}] color is r=#{r},g=#{g},b=#{b}\n"
  return "#{r},#{b},#{g}"
end

def write_file_for_configuration(filename,a)
  file = File.new(filename,"w")                                                      
  a.each do |x|
	  file.puts x
  end
  file.close
end

def get_mouse_loc(robot)
  x=MouseInfo.getPointerInfo().getLocation().x
  y=MouseInfo.getPointerInfo().getLocation().y
  puts "[#{x},#{y}]"
  return x,y
end

def countdown(robot,counter)
  if counter > 3
     speak(robot,"hold",counter)
     robot.delay(500)
  else
    speak(robot,"1",counter)
    speak(robot,"hold",counter)
  end
end

def request_data(robot,label,build_list,counter)
  puts "getting location for #{label}"
  speak(robot,label,counter)
  countdown(robot,counter)
  x,y=get_mouse_loc(robot)
  if label =~ /yellow/ or label =~ /center/ or label =~ /cloak/ or label =~ /micro/
    #a.push([ "label1",[1,2] ] ) #working format
    build_list.push([ "#{label}", [x,y] ])
    #build_list.push(["#{label}[#{x},#{y}]"])
  else 
    build_list.push([ "#{label}_top", [x,y] ])
    #build_list.push("#{label}_top", [x,y] )
    x=x+5
    y=y+5
    build_list.push([ "#{label}_bottom", [x,y] ])
    #build_list.push("#{label}_bottom", [x,y])
    #build_list.push(["#{label}_bottom,[#{x},#{y}]"])
  end
  return build_list
end

robot = Robot.new
my_menu_item_points=[]

counter=0
speak(robot,"defining setup",counter)

map_of_stored_data={
  "screen_center"             => "move the mouse to the center of the screen",
  "cloaking_module"           => "move to the location of the cloaking module",
  "microwarp_module"          => "move to the location of the microwarp  module",
  "yellow_icon_left_top"      => "Yellow icon top Where do you wnat the scan for icon to start",
  "yellow_icon_right_bottom"  => "Yellow icon bottom where do you wnat the scan for icon to end",
  "align_to"                  => "move to the align to button.",
  "warp_to"                   => "move to the warp to button",
  "jump_button"               => "move to the jump button",
  "white_i_icon"              => "move to the white icon button",
  "blue_speed"                => "move to the jump button",
}


#loop through the map_of_questions and build data array
for key,values in map_of_stored_data
  counter=counter+1
  my_menu_item_points=request_data(robot,label=key,build_list=my_menu_item_points,counter)
  puts "size of my_menu_item_points is " + my_menu_item_points.length.to_s
end

puts "size of my_menu_item_points is " + my_menu_item_points.length.to_s

#convert array to hash json formatted uses this
hash_my_menu_item_pts={}
hash_my_menu_item_pts= my_menu_item_points.to_h #convert array to hash 

#create json file holding data
json_location="/var/tmp/locations.json"
File.open(json_location,'w') do |f|
  f.write(hash_my_menu_item_pts.to_json)
end

#legacy: create a standard file
write_file_for_configuration("/var/tmp/locations.txt",my_menu_item_points)

speak(robot,"finished thanks",counter)