#!/bin/bash
# Launch all the existing hand models in RVIZ for visual inspection.

source ./test_models.sh

# Testing default hand - hand_type:="hand_e" hand_version:="E3M5" side:="right" fingers:="all" tip_sensors:="pst"
launch sr_hand

# Testing left side
launch sr_hand side:="left"

# Testing 'bt_sp' tip sensors
launch sr_hand tip_sensors:="bt_sp"

# Testing 'bt_2p' tip sensors
launch sr_hand tip_sensors:="bt_2p"

# Testing custom finger set
launch sr_hand fingers:="th,ff,mf,rf"
launch sr_hand fingers:="th,ff,mf"

# Testing hand lite
launch sr_hand hand_type:="hand_g" hand_version:="G1M5"

# Testing muscle hand
launch sr_hand hand_type:="hand_c" hand_version:="C6M2"
