cmake_minimum_required(VERSION 3.0.2)
project(uwrov_cams)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  sensor_msgs
  std_msgs
)

catkin_package(DEPENDS
    rospy
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

# catkin_python_setup()

catkin_install_python(PROGRAMS
  scripts/pi_cam.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

catkin_install_python(PROGRAMS
  scripts/usb_cam.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
