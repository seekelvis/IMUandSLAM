开始执行过程

```
终端1:
roscore
终端2:
catkin_make
source devel/setup.bash
终端3:(发布者)
roslaunch usb_cam-test.launch  或者 rosrun usb_cam usb_cam_node
终端4:(接收者)
rosrun ORB_SLAM2 Mono ~/catkin_ws/src/ORB_SLAM2/Vocabulary/ORBvoc.txt ~/catkin_ws/src/Asus_myUsbCam.yaml  (自带则~/catkin_ws/src/ORB_SLAM2/Examples/ROS/ORB_SLAM2/Asus.yaml) 

多台连接：
export ROS_MASTER_URI=http://sen7u-laptop:11311

查看话题：
rqt_graph 

控制：
rosrun usb_cam talker2.py

保存图片序列：
运行usb_cam_node时，新建文件夹，在此打开终端
rosrun image_view image_saver image:=/usb_cam/image_raw


```

标定相机内参

```
宽9高6 每格0.0238 米(pc) 注意9*6是内部点的数量 而不是格子数
$ rosrun camera_calibration cameracalibrator.py --size 9x6 --square 0.0238 image:=/usb_cam/image_raw camera:=/usb_cam
宽9高6 每格0.0145 米(ipad)
$ rosrun camera_calibration cameracalibrator.py --size 9x6 --square 0.0145  image:=/usb_cam/image_raw camera:=/usb_cam



error:
出现Failed to load module "canberra-gtk-module"错误的解决方案:
$ sudo apt-get install libcanberra-gtk-module
```







# 配置摄像头出现的问题

## 1

```
ERROR: cannot launch node of type [usb_cam/usb_cam_node]: usb_cam
ROS path [0]=/opt/ros/melodic/share/ros
ROS path [1]=/opt/ros/melodic/share
```

是因为缺少依赖库：

``` 
sudo apt-get install ros-melodic-usb-cam
```

## 2

查看摄像头信息,用于查看想象头编号

```
v4l2-ctl -d /dev/video0 --list-formats-ext
```

## 3

编译ROS的example时出现下面问题

```
cd ~/catkin_ws/src/ORB_SLAM2/Example/ROS/ORB_SLAM2
mkdir build
cd build
cmake ..
make 
```

cmake 时的问题

```
[rosbuild] Building package ORB_SLAM-master
[rosbuild] Error from directory check: /opt/ros/indigo/share/ros/core/rosbuild/bin/check_same_directories.py/home/wf/LearnVIORB-master/Examples/ROS/ORB_VIO
1
Traceback (most recent call last):
File "/opt/ros/indigo/share/ros/core/rosbuild/bin/check_same_directories.py", line 46, in
raise Exception
Exception
CMake Error at /opt/ros/indigo/share/ros/core/rosbuild/private.cmake:102 (message):
[rosbuild] rospack found package "ORB_VIO" at "", but the current
directory is "/home/wf/LearnVIORB-master/Examples/ROS/ORB_VIO". You should
double-check your ROS_PACKAGE_PATH to ensure that packages are found in the
correct precedence order.
Call Stack (most recent call first):
/opt/ros/indigo/share/ros/core/rosbuild/public.cmake:177 (_rosbuild_check_package_location)
CMakeLists.txt:4 (rosbuild_init)

-- Configuring incomplete, errors occurred!
See also "/home/wf/LearnVIORB-master/Examples/ROS/ORB_VIO/build/CMakeFiles/CMakeOutput.log".

在/.bashrc 末尾添加：export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/home/wf/LearnVIORB-master/Examples/ROS/ORB_VIO
添加后要重启电脑
```

make时出现问题

```
[ 22%] Linking CXX executable ../RGBD
/usr/bin/ld: CMakeFiles/RGBD.dir/src/ros_rgbd.cc.o: undefined reference to symbol '_ZN5boost6system15system_categoryEv'
/usr/lib/x86_64-linux-gnu/libboost_system.so: 无法添加符号: DSO missing from command line
collect2: error: ld returned 1 exit status
CMakeFiles/RGBD.dir/build.make:217: recipe for target '../RGBD' failed
make[2]: *** [../RGBD] Error 1
CMakeFiles/Makefile2:67: recipe for target 'CMakeFiles/RGBD.dir/all' failed
make[1]: *** [CMakeFiles/RGBD.dir/all] Error 2
Makefile:129: recipe for target 'all' failed
make: *** [all] Error 2
```

出错原因：libboost_system.so 与libboost_filesystem.so找不到链接目录

解决方案：

```
elvis@elvis-ThinkPad:~/catkin_ws/src/ORB_SLAM2/Examples/ROS/ORB_SLAM2/build$ locate  boost_system
/snap/gnome-3-26-1604/74/usr/lib/x86_64-linux-gnu/libboost_system.so.1.58.0
/snap/gnome-3-26-1604/82/usr/lib/x86_64-linux-gnu/libboost_system.so.1.58.0
/usr/lib/x86_64-linux-gnu/libboost_system.a
/usr/lib/x86_64-linux-gnu/libboost_system.so
/usr/lib/x86_64-linux-gnu/libboost_system.so.1.65.1

elvis@elvis-ThinkPad:~/catkin_ws/src/ORB_SLAM2/Examples/ROS/ORB_SLAM2/build$ locate boost_filesystem
/snap/gnome-3-26-1604/74/usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.58.0
/snap/gnome-3-26-1604/82/usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.58.0
/usr/lib/x86_64-linux-gnu/libboost_filesystem.a
/usr/lib/x86_64-linux-gnu/libboost_filesystem.so
/usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.65.1

```

将libboost_system.so与libboost_filesystem.so复制到ORB_SLAM2/lib下，并且将ORBSLAM2/Examples/ROS/ORBSLAM2下的Cmakelists.txt中加入库目录，具体为 

```
在set(LIBS
${OpenCV_LIBS}
${EIGEN3_LIBS}
${Pangolin_LIBRARIES}
${PROJECT_SOURCE_DIR}/../../../Thirdparty/DBoW2/lib/libDBoW2.so
${PROJECT_SOURCE_DIR}/../../../Thirdparty/g2o/lib/libg2o.so
${PROJECT_SOURCE_DIR}/../../../lib/libORB_SLAM2.so
之后加入${PROJECT_SOURCE_DIR}/../../../lib/libboost_filesystem.so
${PROJECT_SOURCE_DIR}/../../../lib/libboost_system.so
```

### 5

修改接收者话题

##  修改话题

usb_cam默认话题 为usb_cam/image_raw

ros订阅的图像默认为 image/image_raw

进到catkin_ws/src/ORB_SLAM2/Examples/ROS/ORB_SLAM2/src 打开ros_mono.cc 
将subscribe的话题改为/usb_cam/image_raw,将话题接上

重新编译ROS的example

```
 cd ~/catkin_ws/src/ORB_SLAM2
    chmod +x build_ros.sh
    ./build_ros.sh
```

 重新编译工作空间

```
`cd ~/catkin_ws<br>``catkin_make`
```