// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robotiq_2f_85_interfaces:srv/Robotiq2F85GripperCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_2F_85_INTERFACES__SRV__DETAIL__ROBOTIQ2_F85_GRIPPER_COMMAND__TRAITS_HPP_
#define ROBOTIQ_2F_85_INTERFACES__SRV__DETAIL__ROBOTIQ2_F85_GRIPPER_COMMAND__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robotiq_2f_85_interfaces/srv/detail/robotiq2_f85_gripper_command__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace robotiq_2f_85_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const Robotiq2F85GripperCommand_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: width
  {
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << ", ";
  }

  // member: speed
  {
    out << "speed: ";
    rosidl_generator_traits::value_to_yaml(msg.speed, out);
    out << ", ";
  }

  // member: force
  {
    out << "force: ";
    rosidl_generator_traits::value_to_yaml(msg.force, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Robotiq2F85GripperCommand_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: width
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << "\n";
  }

  // member: speed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "speed: ";
    rosidl_generator_traits::value_to_yaml(msg.speed, out);
    out << "\n";
  }

  // member: force
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "force: ";
    rosidl_generator_traits::value_to_yaml(msg.force, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Robotiq2F85GripperCommand_Request & msg, bool use_flow_style = false)
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

}  // namespace robotiq_2f_85_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use robotiq_2f_85_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  robotiq_2f_85_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robotiq_2f_85_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request & msg)
{
  return robotiq_2f_85_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request>()
{
  return "robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request";
}

template<>
inline const char * name<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request>()
{
  return "robotiq_2f_85_interfaces/srv/Robotiq2F85GripperCommand_Request";
}

template<>
struct has_fixed_size<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace robotiq_2f_85_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const Robotiq2F85GripperCommand_Response & msg,
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
  const Robotiq2F85GripperCommand_Response & msg,
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

inline std::string to_yaml(const Robotiq2F85GripperCommand_Response & msg, bool use_flow_style = false)
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

}  // namespace robotiq_2f_85_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use robotiq_2f_85_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  robotiq_2f_85_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robotiq_2f_85_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response & msg)
{
  return robotiq_2f_85_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response>()
{
  return "robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response";
}

template<>
inline const char * name<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response>()
{
  return "robotiq_2f_85_interfaces/srv/Robotiq2F85GripperCommand_Response";
}

template<>
struct has_fixed_size<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand>()
{
  return "robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand";
}

template<>
inline const char * name<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand>()
{
  return "robotiq_2f_85_interfaces/srv/Robotiq2F85GripperCommand";
}

template<>
struct has_fixed_size<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand>
  : std::integral_constant<
    bool,
    has_fixed_size<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request>::value &&
    has_fixed_size<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response>::value
  >
{
};

template<>
struct has_bounded_size<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand>
  : std::integral_constant<
    bool,
    has_bounded_size<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request>::value &&
    has_bounded_size<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response>::value
  >
{
};

template<>
struct is_service<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand>
  : std::true_type
{
};

template<>
struct is_service_request<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request>
  : std::true_type
{
};

template<>
struct is_service_response<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // ROBOTIQ_2F_85_INTERFACES__SRV__DETAIL__ROBOTIQ2_F85_GRIPPER_COMMAND__TRAITS_HPP_
