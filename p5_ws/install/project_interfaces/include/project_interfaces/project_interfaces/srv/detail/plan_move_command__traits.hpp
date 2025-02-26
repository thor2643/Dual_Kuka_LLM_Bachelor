// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from project_interfaces:srv/PlanMoveCommand.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__PLAN_MOVE_COMMAND__TRAITS_HPP_
#define PROJECT_INTERFACES__SRV__DETAIL__PLAN_MOVE_COMMAND__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "project_interfaces/srv/detail/plan_move_command__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'position'
#include "geometry_msgs/msg/detail/point__traits.hpp"
// Member 'orientation'
#include "geometry_msgs/msg/detail/quaternion__traits.hpp"

namespace project_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const PlanMoveCommand_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: arm
  {
    out << "arm: ";
    rosidl_generator_traits::value_to_yaml(msg.arm, out);
    out << ", ";
  }

  // member: position
  {
    out << "position: ";
    to_flow_style_yaml(msg.position, out);
    out << ", ";
  }

  // member: orientation
  {
    out << "orientation: ";
    to_flow_style_yaml(msg.orientation, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PlanMoveCommand_Request & msg,
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

  // member: position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "position:\n";
    to_block_style_yaml(msg.position, out, indentation + 2);
  }

  // member: orientation
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "orientation:\n";
    to_block_style_yaml(msg.orientation, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PlanMoveCommand_Request & msg, bool use_flow_style = false)
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
  const project_interfaces::srv::PlanMoveCommand_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  project_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use project_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const project_interfaces::srv::PlanMoveCommand_Request & msg)
{
  return project_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<project_interfaces::srv::PlanMoveCommand_Request>()
{
  return "project_interfaces::srv::PlanMoveCommand_Request";
}

template<>
inline const char * name<project_interfaces::srv::PlanMoveCommand_Request>()
{
  return "project_interfaces/srv/PlanMoveCommand_Request";
}

template<>
struct has_fixed_size<project_interfaces::srv::PlanMoveCommand_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<project_interfaces::srv::PlanMoveCommand_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<project_interfaces::srv::PlanMoveCommand_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace project_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const PlanMoveCommand_Response & msg,
  std::ostream & out)
{
  out << "{";
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
  const PlanMoveCommand_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
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

inline std::string to_yaml(const PlanMoveCommand_Response & msg, bool use_flow_style = false)
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
  const project_interfaces::srv::PlanMoveCommand_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  project_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use project_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const project_interfaces::srv::PlanMoveCommand_Response & msg)
{
  return project_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<project_interfaces::srv::PlanMoveCommand_Response>()
{
  return "project_interfaces::srv::PlanMoveCommand_Response";
}

template<>
inline const char * name<project_interfaces::srv::PlanMoveCommand_Response>()
{
  return "project_interfaces/srv/PlanMoveCommand_Response";
}

template<>
struct has_fixed_size<project_interfaces::srv::PlanMoveCommand_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<project_interfaces::srv::PlanMoveCommand_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<project_interfaces::srv::PlanMoveCommand_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<project_interfaces::srv::PlanMoveCommand>()
{
  return "project_interfaces::srv::PlanMoveCommand";
}

template<>
inline const char * name<project_interfaces::srv::PlanMoveCommand>()
{
  return "project_interfaces/srv/PlanMoveCommand";
}

template<>
struct has_fixed_size<project_interfaces::srv::PlanMoveCommand>
  : std::integral_constant<
    bool,
    has_fixed_size<project_interfaces::srv::PlanMoveCommand_Request>::value &&
    has_fixed_size<project_interfaces::srv::PlanMoveCommand_Response>::value
  >
{
};

template<>
struct has_bounded_size<project_interfaces::srv::PlanMoveCommand>
  : std::integral_constant<
    bool,
    has_bounded_size<project_interfaces::srv::PlanMoveCommand_Request>::value &&
    has_bounded_size<project_interfaces::srv::PlanMoveCommand_Response>::value
  >
{
};

template<>
struct is_service<project_interfaces::srv::PlanMoveCommand>
  : std::true_type
{
};

template<>
struct is_service_request<project_interfaces::srv::PlanMoveCommand_Request>
  : std::true_type
{
};

template<>
struct is_service_response<project_interfaces::srv::PlanMoveCommand_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // PROJECT_INTERFACES__SRV__DETAIL__PLAN_MOVE_COMMAND__TRAITS_HPP_
