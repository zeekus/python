# jump assist logic

1. Base logic 
   if docked - do undock routine
   if in space - determine if we are near target gate or target docking point
     if near gate                - run jump routine 
     if not near target gate or destination station - run align and jump routine
     if near destination station - run docking routine. 
   if near station dock and exit program. 
 
# undock routine

  if sequence just started, and we are docked.
  click on the yellow undock button and wait. 

  When in space, wait a 30 seconds for the ship to clear the docking ring. 
  If we have a prop mod, use it.

# jump routine/ dock routine. 

  if we are near the gate or the docking station press the jump/dock button. 

# align and jump routine
  if we are not moving and far from the target gate or docking station, align and warp. 
  

   