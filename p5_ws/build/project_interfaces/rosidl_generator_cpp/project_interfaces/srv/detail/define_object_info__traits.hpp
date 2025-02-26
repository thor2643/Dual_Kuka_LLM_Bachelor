// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from project_interfaces:srv/DefineObjectInfo.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__DEFINE_OBJECT_INFO__TRAITS_HPP_
#define PROJECT_INTERFACES__SRV__DETAIL__DEFINE_OBJECT_INFO__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "project_interfaces/srv/detail/define_object_info__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace project_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const DefineObjectInfo_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: object_name
  {
    out << "object_name: ";
    rosidl_generator_traits::value_to_yaml(msg.object_name, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const DefineObjectInfo_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: object_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "object_name: ";
    rosidl_generator_traits::value_to_yaml(msg.object_name, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const DefineObjectInfo_Request & msg, bool use_flow_style = false)
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
  const project_interfaces::srv::DefineObjectInfo_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  project_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use project_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const project_interfaces::srv::DefineObjectInfo_Request & msg)
{
  return project_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<project_interfaces::srv::DefineObjectInfo_Request>()
{
  return "project_interfaces::srv::DefineObjectInfo_Request";
}

template<>
inline const char * name<project_interfaces::srv::DefineObjectInfo_Request>()
{
  return "project_interfaces/srv/DefineObjectInfo_Request";
}

template<>
struct has_fixed_size<project_interfaces::srv::DefineObjectInfo_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<project_interfaces::srv::DefineObjectInfo_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<project_interfaces::srv::DefineObjectInfo_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace project_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const DefineObjectInfo_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const DefineObjectInfo_Response & msg,
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
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const DefineObjectInfo_Response & msg, bool use_flow_style = false)
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
  const project_interfaces::srv::DefineObjectInfo_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  project_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use project_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const project_interfaces::srv::DefineObjectInfo_Response & msg)
{
  return project_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<project_interfaces::srv::DefineObjectInfo_Response>()
{
  return "project_interfaces::srv::DefineObjectInfo_Response";
}

template<>
inline const char * name<project_interfaces::srv::DefineObjectInfo_Response>()
{
  return "project_interfaces/srv/DefineObjectInfo_Response";
}

template<>
struct has_fixed_size<project_interfaces::srv::DefineObjectInfo_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<project_interfaces::srv::DefineObjectInfo_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<project_interfaces::srv::DefineObjectInfo_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<project_interfaces::srv::DefineObjectInfo>()
{
  return "project_interfaces::srv::DefineObjectInfo";
}

template<>
inline const char * name<project_interfaces::srv::DefineObjectInfo>()
{
  return "project_interfaces/srv/DefineObjectInfo";
}

template<>
struct has_fixed_size<project_interfaces::srv::DefineObjectInfo>
  : std::integral_constant<
    bool,
    has_fixed_size<project_interfaces::srv::DefineObjectInfo_Request>::value &&
    has_fixed_size<project_interfaces::srv::DefineObjectInfo_Response>::value
  >
{
};

template<>
struct has_bounded_size<project_interfaces::srv::DefineObjectInfo>
  : std::integral_constant<
    bool,
    has_bounded_size<project_interfaces::srv::DefineObjectInfo_Request>::value &&
    has_bounded_size<project_interfaces::srv::DefineObjectInfo_Response>::value
  >
{
};

template<>
struct is_service<project_interfaces::srv::DefineObjectInfo>
  : std::true_type
{
};

template<>
struct is_service_request<project_interfaces::srv::DefineObjectInfo_Request>
  : std::true_type
{
};

template<>
struct is_service_response<project_interfaces::srv::DefineObjectInfo_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // PROJECT_INTERFACES__SRV__DETAIL__DEFINE_OBJECT_INFO__TRAITS_HPP_
