# syntax=docker/dockerfile:1
FROM arm32v7/ros:noetic-ros-base

ENV ROS_DISTRO noetic

# Installing Dependencies
RUN apt-get update && apt-get install -y \
    git curl \
    build-essential \
    python3-pip \
    netbase \
    net-tools \
    cmake gfortran libjpeg-dev libtiff-dev libgif-dev \
    libavcodec-dev libavformat-dev libswscale-dev libgtk2.0-dev libcanberra-gtk* \
    libxvidcore-dev libx264-dev libgtk-3-dev libtbb2 libtbb-dev libdc1394-22-dev \
    libv4l-dev libopenblas-dev libatlas-base-dev libblas-dev libjasper-dev \
    liblapack-dev libhdf5-dev gcc-arm* protobuf-compiler libgstreamer1.0-dev \
    libilmbase-dev libopenexr-dev

# Install python packages
COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

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

ENV ROS_LOG_DIR /root/logs

EXPOSE 3000
