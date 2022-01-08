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
RUN . ~/.bashrc && . /opt/ros/${ROS_DISTRO}/setup.sh \
    && cd catkin_ws \
    && catkin_make

RUN echo "source /root/catkin_ws/devel/setup.bash" >> ~/.bashrc
RUN alias con="sudo docker exec -it pi_container /bin/bash"