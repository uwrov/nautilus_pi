# syntax=docker/dockerfile:1
FROM arm32v7/ros:noetic-ros-base

ENV ROS_DISTRO noetic

# Installing Dependencies
RUN apt-get update && apt-get install -y \
    git curl pkg-config \
    build-essential cmake \
    python3-pip python3-dev python3-numpy \
    netbase net-tools usbutils \
    libjpeg-dev libpng-dev \
    libavcodec-dev libavformat-dev \
    libswscale-dev libdc1394-22-dev \
    libv4l-dev v4l-utils \
    libtbb2 libtbb-dev

RUN git clone --depth=1 https://github.com/opencv/opencv.git
RUN mkdir /opencv/build
WORKDIR /opencv/build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_ZLIB=ON \
    -D BUILD_OPENMP=ON \
    -D BUILD_TIFF=OFF \
    -D BUILD_OPENJPEG=OFF \
    -D BUILD_JASPER=OFF \
    -D BUILD_OPENEXR=OFF \
    -D BUILD_WEBP=OFF \
    -D BUILD_TBB=ON \
    -D BUILD_IPP_IW=OFF \
    -D BUILD_ITT=OFF \
    -D WITH_OPENMP=ON \
    -D WITH_OPENCL=OFF \
    -D WITH_AVFOUNDATION=OFF \
    -D WITH_CAP_IOS=OFF \
    -D WITH_CAROTENE=OFF \
    -D WITH_CPUFEATURES=OFF \
    -D WITH_EIGEN=OFF \
    -D WITH_GSTREAMER=ON \
    -D WITH_GTK=OFF \
    -D WITH_IPP=OFF \
    -D WITH_HALIDE=OFF \
    -D WITH_VULKAN=OFF \
    -D WITH_INF_ENGINE=OFF \
    -D WITH_NGRAPH=OFF \
    -D WITH_JASPER=OFF \
    -D WITH_OPENJPEG=OFF \
    -D WITH_WEBP=OFF \
    -D WITH_OPENEXR=OFF \
    -D WITH_TIFF=OFF \
    -D WITH_OPENVX=OFF \
    -D WITH_GDCM=OFF \
    -D WITH_TBB=ON \
    -D WITH_HPX=OFF \
    -D WITH_EIGEN=OFF \
    -D WITH_V4L=ON \
    -D WITH_LIBV4L=ON \
    -D WITH_VTK=OFF \
    -D WITH_QT=OFF \
    -D BUILD_opencv_python3=ON \
    -D BUILD_opencv_java=OFF \
    -D BUILD_opencv_gapi=OFF \
    -D BUILD_opencv_objc=OFF \
    -D BUILD_opencv_js=OFF \
    -D BUILD_opencv_ts=OFF \
    -D BUILD_opencv_dnn=OFF \
    -D BUILD_opencv_calib3d=OFF \
    -D BUILD_opencv_objdetect=OFF \
    -D BUILD_opencv_stitching=OFF \
    -D BUILD_opencv_ml=OFF \
    -D BUILD_opencv_world=OFF \
    -D BUILD_EXAMPLES=OFF \
    -D OPENCV_ENABLE_NONFREE=OFF \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF ..

# Install pi camera
RUN pip3 install git+https://github.com/waveform80/picamera

# Create a catkin workspace
# RUN mkdir -p /root/catkin_ws/src

# # Set up ROS workspace
# WORKDIR /root

# # Create a copy of our ROS packages and build
# COPY src/uwrov_auto /root/catkin_ws/src/uwrov_auto
# COPY src/uwrov_cams /root/catkin_ws/src/uwrov_cams
# RUN . ~/.bashrc && . /opt/ros/${ROS_DISTRO}/setup.sh \
#     && cd catkin_ws \
#     && catkin_make

# RUN echo "source /root/catkin_ws/devel/setup.bash" >> ~/.bashrc

# ENV ROS_LOG_DIR /root/logs
