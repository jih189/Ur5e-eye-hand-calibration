project(tutorial-calibration)

cmake_minimum_required(VERSION 2.6)

find_package(VISP REQUIRED visp_robot visp_vision visp_io visp_gui)

set(tutorial_cpp
  get-chessboard-pose.cpp
  hand-eye-calibration.cpp
  convertAngle.cpp
)

file(GLOB tutorial_data "*.yaml")

foreach(cpp ${tutorial_cpp})
  visp_add_target(${cpp})
  if(COMMAND visp_add_dependency)
    visp_add_dependency(${cpp} "tutorials")
  endif()
endforeach()

# Copy the data files to the same location than the target
foreach(data ${tutorial_data})
  visp_copy_data(hand-eye-calibration.cpp ${data})
endforeach()
