cmake_minimum_required(VERSION 2.8.3)
project(sr_description)
find_package(catkin REQUIRED COMPONENTS urdf xacro)
include_directories(${Boost_INCLUDE_DIR} ${catkin_INCLUDE_DIRS})
set(ROS_BUILD_TYPE Release)

#set the default path for built executables to the "bin" directory
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
#set the default path for built libraries to the "lib" directory
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

catkin_package(
    DEPENDS
    CATKIN_DEPENDS urdf xacro
    INCLUDE_DIRS
    LIBRARIES
)

catkin_add_gtest(test_sr_description_urdf test/test_sr_description_urdf.cpp)
target_link_libraries(test_sr_description_urdf ${Boost_LIBRARIES} ${GTEST_LIBRARIES} pthread)