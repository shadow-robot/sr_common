#!/bin/bash
# Launch all the existing arm and hand models in RVIZ for visual inspection.

source ./test_models.sh

launch arm_and_hand_motor
launch arm_and_hand_motor_ellipsoid
launch arm_and_hand_motor_biotac
launch arm_and_hand_motor_three_finger
launch arm_and_sr_one_finger_motor
launch arm_and_hand_muscle
launch arm_and_hand_muscle_biotac
