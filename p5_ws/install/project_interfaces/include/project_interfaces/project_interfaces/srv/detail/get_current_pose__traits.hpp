// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from project_interfaces:srv/GetCurrentPose.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__GET_CURRENT_POSE__TRAITS_HPP_
#define PROJECT_INTERFACES__SRV__DETAIL__GET_CURRENT_POSE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "project_interfaces/srv/detail/get_current_pose__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace project_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetCurrentPose_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: arm
  {
    out << "arm: ";
    rosidl_generator_traits::value_to_yaml(msg.arm, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetCurrentPose_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: arm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "arm: ";
    rosidl_generator_traits::value_to_yaml(msg.arm, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetCurrentPose_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace project_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use project_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const project_interfaces::srv::GetCurrentPose_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  project_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use project_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const project_interfaces::srv::GetCurrentPose_Request & msg)
{
  return project_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<project_interfaces::srv::GetCurrentPose_Request>()
{
  return "project_interfaces::srv::GetCurrentPose_Request";
}

template<>
inline const char * name<project_interfaces::srv::GetCurrentPose_Request>()
{
  return "project_interfaces/srv/GetCurrentPose_Request";
}

template<>
struct has_fixed_size<project_interfaces::srv::GetCurrentPose_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<project_interfaces::srv::GetCurrentPose_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<project_interfaces::srv::GetCurrentPose_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"

namespace project_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetCurrentPose_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: pose
  {
    out << "pose: ";
    to_flow_style_yaml(msg.pose, out);
    out << ", ";
  }

  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: log
  {
    out << "log: ";
    rosidl_generator_traits::value_to_yaml(msg.log, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetCurrentPose_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pose:\n";
    to_block_style_yaml(msg.pose, out, indentation + 2);
  }

  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: log
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "log: ";
    rosidl_generator_traits::value_to_yaml(msg.log, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetCurrentPose_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace project_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use project_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const project_interfaces::srv::GetCurrentPose_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  project_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use project_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const project_interfaces::srv::GetCurrentPose_Response & msg)
{
  return project_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<project_interfaces::srv::GetCurrentPose_Response>()
{
  return "project_interfaces::srv::GetCurrentPose_Response";
}

template<>
inline const char * name<project_interfaces::srv::GetCurrentPose_Response>()
{
  return "project_interfaces/srv/GetCurrentPose_Response";
}

template<>
struct has_fixed_size<project_interfaces::srv::GetCurrentPose_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<project_interfaces::srv::GetCurrentPose_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<project_interfaces::srv::GetCurrentPose_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<project_interfaces::srv::GetCurrentPose>()
{
  return "project_interfaces::srv::GetCurrentPose";
}

template<>
inline const char * name<project_interfaces::srv::GetCurrentPose>()
{
  return "project_interfaces/srv/GetCurrentPose";
}

template<>
struct has_fixed_size<project_interfaces::srv::GetCurrentPose>
  : std::integral_constant<
    bool,
    has_fixed_size<project_interfaces::srv::GetCurrentPose_Request>::value &&
    has_fixed_size<project_interfaces::srv::GetCurrentPose_Response>::value
  >
{
};

template<>
struct has_bounded_size<project_interfaces::srv::GetCurrentPose>
  : std::integral_constant<
    bool,
    has_bounded_size<project_interfaces::srv::GetCurrentPose_Request>::value &&
    has_bounded_size<project_interfaces::srv::GetCurrentPose_Response>::value
  >
{
};

template<>
struct is_service<project_interfaces::srv::GetCurrentPose>
  : std::true_type
{
};

template<>
struct is_service_request<project_interfaces::srv::GetCurrentPose_Request>
  : std::true_type
{
};

template<>
struct is_service_response<project_interfaces::srv::GetCurrentPose_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // PROJECT_INTERFACES__SRV__DETAIL__GET_CURRENT_POSE__TRAITS_HPP_
