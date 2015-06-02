#!/bin/bash
# launch all the existing hand models in RVIZ for visual test. use CTRL-C to kill current test and enter to launch next one
echo press enter after you tested and killed the launch file

read -p "Press [Enter] key "
SIMULATED=0  MUSCLE=0  BIOTAC_HAND=0 BTSP_HAND=1  ELLIPSOID=0  ONE_FINGER=0  THREE_FINGER=0  LEFT_HAND=0   roslaunch sr_description test_hand_models.launch   #shadowhand_motor_btsp.urdf
