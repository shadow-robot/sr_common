#!/bin/bash
# Launch all the existing hand models in RVIZ for visual inspection.

source ./test_models.sh

launch sr_hand hand_type:="hand_e" hand_version:="E3M5" side:="right" fingers:="th,ff,lf" tip_sensors:="pst"
launch sr_hand hand_type:="hand_e" hand_version:="E3M5" side:="left" fingers:="th,ff,lf" tip_sensors:="pst"
launch sr_hand hand_type:="hand_e" hand_version:="E3M5" side:="right" fingers:="th,ff,lf" tip_sensors:="th=bt_2p,ff=bt_sp,mf=pst,rf=pst,lf=pst"
launch sr_hand
