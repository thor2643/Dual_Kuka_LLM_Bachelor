cmake_minimum_required(VERSION 3.10)
project(project_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(sensor_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/GetSimCameraData.srv"
  "srv/SendDepthData.srv"
  "srv/SendRGBData.srv"
  "srv/SpawnCube.srv"
  DEPENDENCIES builtin_interfaces sensor_msgs std_msgs
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
