execute_process(COMMAND "/home/elvis/catkin_ws/src/camera_calibration/build/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/elvis/catkin_ws/src/camera_calibration/build/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
