cmake_minimum_required(VERSION 3.8)
project(gpd_ros2)

# Find ROS2 dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(pcl_conversions REQUIRED)   # For pcl::fromROSMsg
find_package(PCL 1.9 REQUIRED COMPONENTS common io)  # Find PCL
find_package(Eigen3 REQUIRED)
find_package(OpenCV REQUIRED)
find_package(std_srvs REQUIRED)
find_package(visualization_msgs REQUIRED)



# GPD does not provide an ament package, so find it manually
find_library(GPD_LIB NAMES gpd PATHS /usr/local/lib NO_DEFAULT_PATH)
if(NOT GPD_LIB)
  message(FATAL_ERROR "libgpd.so not found. Did you install GPD to /usr/local?") 
endif()
# GPD headers are in /usr/local/include/gpd
include_directories(/usr/local/include)   # include parent of gpd directory
include_directories(${PCL_INCLUDE_DIRS} ${OpenCV_INCLUDE_DIRS} ${EIGEN3_INCLUDE_DIR})

add_executable(gpd_node src/gpd_node.cpp)
target_compile_definitions(gpd_node PRIVATE DISABLE_PLOTTING)
ament_target_dependencies(gpd_node 
  rclcpp 
  std_msgs 
  sensor_msgs 
  geometry_msgs 
  pcl_conversions
  std_srvs
  visualization_msgs 
)
# Link against GPD, PCL, OpenMP, OpenCV
target_link_libraries(gpd_node ${GPD_LIB} ${PCL_LIBRARIES} ${OpenCV_LIBS} gomp)  # gomp for OpenMP
target_compile_options(gpd_node PRIVATE -O3 -march=native -pthread)

install(TARGETS gpd_node DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
