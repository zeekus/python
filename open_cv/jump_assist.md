# jump assist logic 

* rewrite version 3. 

todo: 
    *implement multithreading* -> #import threading #multiple checks at the same time rather than linear checks.
    *implement image processsing with numpy* 
    *logic improvments* - implement a loop that figures out how far we need to go.

# Goals: 
     * make a new version that uses opencv,numpy, and multithreading 
     * reduce errors and hangups to 0 - older version have difficulty with background images. Maybe we can remove them with numpy or something else.
     * precondition the refernce images and the live target images to reduce errors. 
     * create situation awareness in the script. - We want the current state at all times.  
     * create calibration checks that map out regions of screen so no input is needed. 
      - identify and record location of the button window
      - identify and reord the location of the icons displaying the yellow targe location 
      - in the calibration - automatically determine what modules are in place and run the script per the modules we find. 


   references: 
      removing background image using a tensor flow - https://www.youtube.com/watch?v=KkhPN7Z4Fy8
      - https://stackoverflow.com/questions/63001988/how-to-remove-background-of-images-in-pytho
      - sklearn https://flothesof.github.io/removing-background-scikit-image.html
      - https://livecodestream.dev/post/remove-the-background-from-images-using-ai-and-python/
      - https://betterprogramming.pub/automating-white-or-any-other-color-background-removal-with-python-and-opencv-4be4addb6c99

# calibration checks
  - open ship fitting window and dermine what modules we have on our ship and the ship class.  
  - determine if we have a mwd and map the location
  - determine if we have a cloaking device and map location
  - determine and map location of the golden wheel 
  - determine and map location of the session change button 
  - determine and map location of the undock buttion 

# basic situational awareness
    - if we see the warping message go to sleep for 2 sec.
    - if we see object not found image, determine if we are in a session change or hung up. 
      -   if we are sitting still for longer than 10 seconds, we are probably hung up. 


# Basic logic 
   if docked - do undock routine
   if in space - determine if we are near target gate or target docking point
     if near gate - run jump routine
        [ todo: insert image here. ] 
     if not near target gate or destination station - run align and jump routine
        [ todo: insert image here.]
     if near destination station - run docking routine.
        [ todo: insert image here. ] 
     if near station dock and exit program.
        [todo: incert image here. ] 
 
# undock routine
  if sequence just started, and we are docked.
  click on the yellow undock button and wait. 

  When in space, wait a 30 seconds for the ship to clear the docking ring. 
  If we have a prop mod, use it.

# jump routine/ dock routine. 
  if we are near the gate or the docking station press the jump/dock button. 

# align and jump routine
  if we are not moving and far from the target gate or docking station, align and warp. 

                                                  