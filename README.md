# OpenVSLAM_Dev

This repository has the process to setup OpenVSLAM and how to use it.

## System:

The below code is tested on:

 - Ubuntu 18.05 LTS
 - NVIDIA GTX 950M
 
## Initial Installation

Do initial installation as per [this](https://openvslam.readthedocs.io/en/master/installation.html#subsection-common-linux-macos).

For Linux, the commands are all laid out here:

    # Clone the official VSLAM repo
    git clone https://github.com/xdspacelab/openvslam

    # grant yourself root permissions. 
    sudo -s

    apt update -y
    apt upgrade -y --no-install-recommends
  
    # basic dependencies
    apt install -y build-essential pkg-config cmake git wget curl unzip
    
    # g2o dependencies
    apt install -y libatlas-base-dev libsuitesparse-dev
    
    # OpenCV dependencies
    apt install -y libgtk-3-dev
    apt install -y ffmpeg
    apt install -y libavcodec-dev libavformat-dev libavutil-dev libswscale-dev libavresample-dev
    
    # eigen dependencies
    apt install -y gfortran
    
    # other dependencies
    apt install -y libyaml-cpp-dev libgoogle-glog-dev libgflags-dev
    
    # Download and install Eigen from source.
    cd ~/openvslam/
    wget -q https://gitlab.com/libeigen/eigen/-/archive/3.3.7/eigen-3.3.7.tar.bz2
    tar xf eigen-3.3.7.tar.bz2
    rm -rf eigen-3.3.7.tar.bz2
    cd eigen-3.3.7
    mkdir -p build && cd build
    cmake \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        ..
    make -j4
    make install
    
    # Download, build and install OpenCV from source.
    
    cd ~/openvslam/
    wget -q https://github.com/opencv/opencv/archive/3.4.0.zip
    unzip -q 3.4.0.zip
    rm -rf 3.4.0.zip
    cd opencv-3.4.0
    mkdir -p build && cd build
    cmake \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        -DENABLE_CXX11=ON \
        -DBUILD_DOCS=OFF \
        -DBUILD_EXAMPLES=OFF \
        -DBUILD_JASPER=OFF \
        -DBUILD_OPENEXR=OFF \
        -DBUILD_PERF_TESTS=OFF \
        -DBUILD_TESTS=OFF \
        -DWITH_EIGEN=ON \
        -DWITH_FFMPEG=ON \
        -DWITH_OPENMP=ON \
        ..
    make -j4
    make install

    
    # Common Installation Instructions
    # Download, build and install the custom DBoW2 from source.
    
    cd ~/openvslam/
    git clone https://github.com/shinsumicco/DBoW2.git
    cd DBoW2
    mkdir build && cd build
    cmake \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        ..
    make -j4
    make install

    # Download, build and install g2o.

    cd ~/openvslam/
    git clone https://github.com/RainerKuemmerle/g2o.git
    cd g2o
    git checkout 9b41a4ea5ade8e1250b9c1b279f3a9c098811b5a
    mkdir build && cd build
    cmake \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        -DCMAKE_CXX_FLAGS=-std=c++11 \
        -DBUILD_SHARED_LIBS=ON \
        -DBUILD_UNITTESTS=OFF \
        -DBUILD_WITH_MARCH_NATIVE=ON \
        -DG2O_USE_CHOLMOD=OFF \
        -DG2O_USE_CSPARSE=ON \
        -DG2O_USE_OPENGL=OFF \
        -DG2O_USE_OPENMP=ON \
        ..
    make -j4
    make install

    # (if you plan on using PangolinViewer)
    # Download, build and install Pangolin from source.

    cd ~/openvslam/
    git clone https://github.com/stevenlovegrove/Pangolin.git
    cd Pangolin
    git checkout ad8b5f83222291c51b4800d5a5873b0e90a0cf81
    mkdir build && cd build
    cmake \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        ..
    make -j4
    make install

    # (if you plan on using SocketViewer)
    # Download, build and install socket.io-client-cpp from source.

    cd ~/openvslam/
    git clone https://github.com/shinsumicco/socket.io-client-cpp.git
    cd socket.io-client-cpp
    git submodule init
    git submodule update
    mkdir build && cd build
    cmake \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        -DBUILD_UNIT_TESTS=OFF \
        ..
    make -j4
    make install

    # (if you plan on using SocketViewer)
    # Install Protobuf.

    # for Ubuntu 18.04 (or later)
    apt install -y libprotobuf-dev protobuf-compiler

## Build Instructions

 When building with support for PangolinViewer, please specify the following cmake options: 
 **-DUSE_PANGOLIN_VIEWER=ON** and **-DUSE_SOCKET_PUBLISHER=OFF**.

    cd ~/openvslam/
    mkdir build && cd build
    cmake \
        -DBUILD_WITH_MARCH_NATIVE=ON \
        -DUSE_PANGOLIN_VIEWER=ON \
        -DUSE_SOCKET_PUBLISHER=OFF \
        -DUSE_STACK_TRACE_LOGGER=ON \
        -DBOW_FRAMEWORK=DBoW2 \
        -DBUILD_TESTS=ON \
        ..
    make -j4

 When building with support for SocketViewer, please specify the following cmake options: 
 **-DUSE_PANGOLIN_VIEWER=OFF** and **-DUSE_SOCKET_PUBLISHER=ON**.

    cd ~/openvslam/
    mkdir build && cd build
    cmake \
        -DBUILD_WITH_MARCH_NATIVE=ON \
        -DUSE_PANGOLIN_VIEWER=OFF \
        -DUSE_SOCKET_PUBLISHER=ON \
        -DUSE_STACK_TRACE_LOGGER=ON \
        -DBOW_FRAMEWORK=DBoW2 \
        -DBUILD_TESTS=ON \
        ..
    make -j4

After building, check to see if it was successfully built by executing 

    ./run_kitti_slam -h

The output should be like this:

    Allowed options:
    -h, --help             produce help message
    -v, --vocab arg        vocabulary file path
    -d, --data-dir arg     directory path which contains dataset
    -c, --config arg       config file path
    --frame-skip arg (=1)  interval of frame skip
    --no-sleep             not wait for next frame in real time
    --auto-term            automatically terminate the viewer
    --debug                debug mode
    --eval-log             store trajectory and tracking times for evaluation
    -p, --map-db arg       store a map database at this path after SLAM

Here onwards scroll down and check the [official documentation](https://openvslam.readthedocs.io/en/master/installation.html#subsection-common-linux-macos) to run in SocketViewer.

## Launching socketviewer

    $ cd ~/openvslam/viewer
    $ node app.js

The output should be as follows: 

    WebSocket: listening on *:3000
    HTTP server: listening on *:3001

Open a new browser tab and type in :

    http://localhost:3001/
    
You should now be able to see the Socket Viewer. Continue with **Simple Tutorials** [here](https://openvslam.readthedocs.io/en/master/simple_tutorial.html).

## Running on any dataset:

There are many sample datasets as seen [here](https://openvslam.readthedocs.io/en/master/simple_tutorial.html).
To extract any one specific folder in openvslam/build, do the following

 - Right click on the scenario and copy link
 - Copy the FILE_ID part of the link.
 
 For example, while trying to extract for aist_factory_A.zip, the link is 
 
    https://drive.google.com/file/d/10JZjmZYntdpiDvIxe8sxLlF4xZ0exyw0/view?usp=sharing
    
 Here the FILE_ID is 

    10JZjmZYntdpiDvIxe8sxLlF4xZ0exyw0
    
Now, to download and unzip anything from this directory, execute the following commands:

    $ FILE_ID="10JZjmZYntdpiDvIxe8sxLlF4xZ0exyw0"

    $ curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=${FILE_ID}" > /dev/null

    $ CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"

    $ curl -sLb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=${FILE_ID}" -o aist_factory_A.zip

    $ unzip aist_factory_A.zip 

You can see the extracted folder in the build directory now.

## Running on a standard dataset

### Kitti Dataset

The dataset can be downloaded from [here](http://www.cvlibs.net/datasets/kitti/eval_odometry.php). Download the greyscale one. 

Paste the folders in the right directory. I pasted the kitti dataset in the **openvslam/example/kitti/** directory. You can see the sequences of images in them. To launch, start the socket viewer as shown previously. Then, enter the following commands:

    $ cd ~/openvslam/build
   
Open a new terminal

    $ sudo -s

    $ ./run_kitti_slam -v ../build/orb_vocab/orb_vocab.dbow2 -d ../example/kitti/dataset/sequences/00/ -c ../example/kitti/KITTI_mono_00-02.yaml


## Running on ROS

## Launching socketviewer

All commands are followed as per [this](https://openvslam.readthedocs.io/en/master/ros_package.html)

    $ cd ~/openvslam/viewer
    $ node app.js

The output should be as follows: 

    WebSocket: listening on *:3000
    HTTP server: listening on *:3001

Open a new browser tab and type in :

    http://localhost:3001/
    
Open a new terminal, and Start roscore

    $ roscore
    
Open a new terminal
    
    $ source ~/openvslam/ros/devel/setup.bash
    $ rosrun publisher video -m /path/to/video.mp4

Open a new terminal, Republish the ROS topic to **/camera/image_raw**

    $ source ~/openvslam/ros/devel/setup.bash
    $ rosrun image_transport republish raw in:=/video/image_raw raw out:=/camera/image_raw
   
Open a new terminal
    
    $ source ~/openvslam/ros/devel/setup.bash
    $ rosrun openvslam run_slam -v build/orb_vocab/orb_vocab.dbow2 -c /path/to/config.yaml
    
Open a new terminal
    
    $ source ~/openvslam/ros/devel/setup.bash
    $ rosrun openvslam run_localization -v build/orb_vocab/orb_vocab.dbow2 -c /path/to/config.yaml --map-db build/map.msg

## Visualization and using point cloud data

#### Visualizing using open3d and .msg file

Run from the ~/openvslam/example folder

    $ python3 visualize_openvslam_map.py ~/openvslam/build/map.msg

#### Converting from .msg file to .csv

Run from the ~/openvslam/example folder

    $ python3 msg2csv.py ~/openvslam/build/map.msg output_file.csv

#### Converting from .msg file to .pcd 

Run from the ~/openvslam/example folder

    $ python3 msg2pcd.py ~/openvslam/build/map.msg output_file.pcd
    
#### Converting from .csv file to .ply file

Run from the ~/openvslam/example folder

    $ python3 csv2ply.py
