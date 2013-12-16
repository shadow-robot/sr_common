cmake_minimum_required(VERSION 2.8.3)
project(sr_robot_msgs)
find_package(catkin REQUIRED COMPONENTS roslib message_generation std_msgs sensor_msgs)

#set the default path for built executables to the "bin" directory
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
#set the default path for built libraries to the "lib" directory
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

add_message_files(
  FILES
  AuxSpiData.msg
  BiotacAll.msg
  Biotac.msg
  cartesian_data.msg
  cartesian_position.msg
  command.msg
  config.msg
  contrlr.msg
  ControlType.msg
  EthercatDebug.msg
  FromMotorDataType.msg
  JointControllerState.msg
  joint.msg
  JointMusclePositionControllerState.msg
  JointMuscleValveControllerCommand.msg
  JointMuscleValveControllerState.msg
  joints_data.msg
  MidProxDataAll.msg
  MidProxData.msg
  MotorSystemControls.msg
  reverseKinematics.msg
  sendupdate.msg
  ShadowPST.msg
  TactileArray.msg
  Tactile.msg
  UBI0All.msg
  UBI0.msg
)

add_service_files(
  FILES
  ChangeControlType.srv
  ChangeMotorSystemControls.srv
  ForceController.srv
  GetSegmentedLine.srv
  is_hand_occupied.srv
  ManualSelfTest.srv
  NullifyDemand.srv
  SetDebugData.srv
  SetEffortControllerGains.srv
  SetMixedPositionVelocityPidGains.srv
  SetPidGains.srv
  SimpleMotorFlasher.srv
  which_fingers_are_touching.srv
)

generate_messages(DEPENDENCIES std_msgs sensor_msgs)

catkin_package(
  DEPENDS
  CATKIN_DEPENDS roslib message_runtime std_msgs sensor_msgs
  INCLUDE_DIRS
  LIBRARIES
)