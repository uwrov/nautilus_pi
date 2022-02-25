# syntax=docker/dockerfile:1
FROM uwrov/pi_base:latest

ENV ROS_DISTRO noetic

# Create a catkin workspace
RUN mkdir -p /root/catkin_ws/src

# Set up ROS workspace
WORKDIR /root

# Create a copy of our ROS packages and build
COPY src/uwrov_auto /root/catkin_ws/src/uwrov_auto
COPY src/uwrov_cams /root/catkin_ws/src/uwrov_cams
RUN bash ~/.bashrc && . /opt/ros/${ROS_DISTRO}/setup.sh \
    && cd catkin_ws \
    && catkin_make

RUN apt-get update && apt-get install -y wget unzip
RUN unzip -f master.zip && cd pigpio-master && make && sudo make install 
RUN echo "source /root/catkin_ws/devel/setup.bash" >> ~/.bashrc
