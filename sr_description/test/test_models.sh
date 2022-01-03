function stop_rostopic {
	kill $ROSTOPIC_PID
	unset ROSTOPIC_PID
	trap - EXIT  # Uninstall cleanup handler
}

function start_rostopic {
	# Publish text marker
	rostopic pub /text_marker visualization_msgs/Marker \
"header:
  frame_id: 'world'
type: 9
pose:
  position: {x: 0.0, y: 0.0, z: -0.1}
  orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
scale: {x: 0.0, y: 0.0, z: 0.1}
color: {r: 0.0, g: 0.0, b: 0.0, a: 1.0}
text: '$1 $2 $3 $4 $5 $6'" &

	ROSTOPIC_PID=$!          # Get PID from background process
	trap stop_rostopic EXIT  # Ensure rostopic is killed on exit
}

function launch {
	
	robot_description=$(xacro ../robots/sr_hand.urdf.xacro $2 $3 $4 $5 $6)
	echo $robot_description > "robot_description"

	echo "***********************************************"
	echo "Testing $1.urdf.xacro "
	for ((i=2; i<=$#; i++))
	do
		echo "--- ${!i}"
	done
	echo "***********************************************"

	start_rostopic $1 $2 $3 $4 $5 $6
	roslaunch sr_description test_models.launch robot:="$(rospack find sr_description)/test/robot_description" rviz_config:=$RVIZ_CONFIG
	rm "robot_description"
	stop_rostopic

	sleep 0.2  # Some time to Ctrl-C before next launch
}

RVIZ_CONFIG="$(basename $0)"
RVIZ_CONFIG="${RVIZ_CONFIG%%.*}.rviz"

if ! rostopic list > /dev/null ; then
	echo "We suggest to run your own roscore. Then the processed filename will be displayed as a text marker in rviz."
	echo
fi
echo "We will iterate through some URDF files now. Ctrl-C or close rviz to forward to the next one."
echo "Hold Ctrl-C for a while to ultimately stop."
read -p "Press [Enter] to start."
