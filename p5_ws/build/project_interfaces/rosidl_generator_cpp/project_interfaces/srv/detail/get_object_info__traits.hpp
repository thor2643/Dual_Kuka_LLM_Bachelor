// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from project_interfaces:srv/GetObjectInfo.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__GET_OBJECT_INFO__TRAITS_HPP_
#define PROJECT_INTERFACES__SRV__DETAIL__GET_OBJECT_INFO__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "project_interfaces/srv/detail/get_object_info__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace project_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetObjectInfo_Request & msg,
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
  const GetObjectInfo_Request & msg,
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

inline std::string to_yaml(const GetObjectInfo_Request & msg, bool use_flow_style = false)
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
  const project_interfaces::srv::GetObjectInfo_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  project_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use project_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const project_interfaces::srv::GetObjectInfo_Request & msg)
{
  return project_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<project_interfaces::srv::GetObjectInfo_Request>()
{
  return "project_interfaces::srv::GetObjectInfo_Request";
}

template<>
inline const char * name<project_interfaces::srv::GetObjectInfo_Request>()
{
  return "project_interfaces/srv/GetObjectInfo_Request";
}

template<>
struct has_fixed_size<project_interfaces::srv::GetObjectInfo_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<project_interfaces::srv::GetObjectInfo_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<project_interfaces::srv::GetObjectInfo_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'centers'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace project_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetObjectInfo_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: object_count
  {
    out << "object_count: ";
    rosidl_generator_traits::value_to_yaml(msg.object_count, out);
    out << ", ";
  }

  // member: centers
  {
    if (msg.centers.size() == 0) {
      out << "centers: []";
    } else {
      out << "centers: [";
      size_t pending_items = msg.centers.size();
      for (auto item : msg.centers) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: orientations
  {
    if (msg.orientations.size() == 0) {
      out << "orientations: []";
    } else {
      out << "orientations: [";
      size_t pending_items = msg.orientations.size();
      for (auto item : msg.orientations) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: grasp_widths
  {
    if (msg.grasp_widths.size() == 0) {
      out << "grasp_widths: []";
    } else {
      out << "grasp_widths: [";
      size_t pending_items = msg.grasp_widths.size();
      for (auto item : msg.grasp_widths) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetObjectInfo_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: object_count
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "object_count: ";
    rosidl_generator_traits::value_to_yaml(msg.object_count, out);
    out << "\n";
  }

  // member: centers
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.centers.size() == 0) {
      out << "centers: []\n";
    } else {
      out << "centers:\n";
      for (auto item : msg.centers) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: orientations
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.orientations.size() == 0) {
      out << "orientations: []\n";
    } else {
      out << "orientations:\n";
      for (auto item : msg.orientations) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: grasp_widths
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.grasp_widths.size() == 0) {
      out << "grasp_widths: []\n";
    } else {
      out << "grasp_widths:\n";
      for (auto item : msg.grasp_widths) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetObjectInfo_Response & msg, bool use_flow_style = false)
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
  const project_interfaces::srv::GetObjectInfo_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  project_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use project_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const project_interfaces::srv::GetObjectInfo_Response & msg)
{
  return project_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<project_interfaces::srv::GetObjectInfo_Response>()
{
  return "project_interfaces::srv::GetObjectInfo_Response";
}

template<>
inline const char * name<project_interfaces::srv::GetObjectInfo_Response>()
{
  return "project_interfaces/srv/GetObjectInfo_Response";
}

template<>
struct has_fixed_size<project_interfaces::srv::GetObjectInfo_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<project_interfaces::srv::GetObjectInfo_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<project_interfaces::srv::GetObjectInfo_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<project_interfaces::srv::GetObjectInfo>()
{
  return "project_interfaces::srv::GetObjectInfo";
}

template<>
inline const char * name<project_interfaces::srv::GetObjectInfo>()
{
  return "project_interfaces/srv/GetObjectInfo";
}

template<>
struct has_fixed_size<project_interfaces::srv::GetObjectInfo>
  : std::integral_constant<
    bool,
    has_fixed_size<project_interfaces::srv::GetObjectInfo_Request>::value &&
    has_fixed_size<project_interfaces::srv::GetObjectInfo_Response>::value
  >
{
};

template<>
struct has_bounded_size<project_interfaces::srv::GetObjectInfo>
  : std::integral_constant<
    bool,
    has_bounded_size<project_interfaces::srv::GetObjectInfo_Request>::value &&
    has_bounded_size<project_interfaces::srv::GetObjectInfo_Response>::value
  >
{
};

template<>
struct is_service<project_interfaces::srv::GetObjectInfo>
  : std::true_type
{
};

template<>
struct is_service_request<project_interfaces::srv::GetObjectInfo_Request>
  : std::true_type
{
};

template<>
struct is_service_response<project_interfaces::srv::GetObjectInfo_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // PROJECT_INTERFACES__SRV__DETAIL__GET_OBJECT_INFO__TRAITS_HPP_
