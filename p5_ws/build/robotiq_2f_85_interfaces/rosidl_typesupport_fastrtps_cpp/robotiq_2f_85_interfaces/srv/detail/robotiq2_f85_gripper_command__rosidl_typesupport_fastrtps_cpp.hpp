// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from robotiq_2f_85_interfaces:srv/Robotiq2F85GripperCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_2F_85_INTERFACES__SRV__DETAIL__ROBOTIQ2_F85_GRIPPER_COMMAND__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define ROBOTIQ_2F_85_INTERFACES__SRV__DETAIL__ROBOTIQ2_F85_GRIPPER_COMMAND__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "robotiq_2f_85_interfaces/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "robotiq_2f_85_interfaces/srv/detail/robotiq2_f85_gripper_command__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace robotiq_2f_85_interfaces
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
cdr_serialize(
  const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
get_serialized_size(
  const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
max_serialized_size_Robotiq2F85GripperCommand_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace robotiq_2f_85_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, robotiq_2f_85_interfaces, srv, Robotiq2F85GripperCommand_Request)();

#ifdef __cplusplus
}
#endif

// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "robotiq_2f_85_interfaces/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
// already included above
// #include "robotiq_2f_85_interfaces/srv/detail/robotiq2_f85_gripper_command__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// already included above
// #include "fastcdr/Cdr.h"

namespace robotiq_2f_85_interfaces
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
cdr_serialize(
  const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
get_serialized_size(
  const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
max_serialized_size_Robotiq2F85GripperCommand_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace robotiq_2f_85_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, robotiq_2f_85_interfaces, srv, Robotiq2F85GripperCommand_Response)();

#ifdef __cplusplus
}
#endif

#include "rmw/types.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "robotiq_2f_85_interfaces/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
const rosidl_service_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, robotiq_2f_85_interfaces, srv, Robotiq2F85GripperCommand)();

#ifdef __cplusplus
}
#endif

#endif  // ROBOTIQ_2F_85_INTERFACES__SRV__DETAIL__ROBOTIQ2_F85_GRIPPER_COMMAND__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
