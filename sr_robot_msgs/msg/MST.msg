# Stamp when sent
time timestamp
# Fields gathering both the magnetic and temperature data
geometry_msgs/Point[] magnetic_data
float32[] temperature_data
# Fields gathering status information
# -1 --> the sensor does not provide this information
# 0 --> all good
# > 0 values --> error codes (please refer to documentation)
int8 status