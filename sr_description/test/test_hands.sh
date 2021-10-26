#!/bin/bash
# Launch all the existing hand models in RVIZ for visual inspection.

source ./test_models.sh

launch sr_hand hand_type:="hand_ex" hand_version:="E3M5" side:="right" fingers:="th,ff,lf" tip_sensors:="pst"