// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from project_interfaces:srv/GetObjectInfo.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__GET_OBJECT_INFO__BUILDER_HPP_
#define PROJECT_INTERFACES__SRV__DETAIL__GET_OBJECT_INFO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "project_interfaces/srv/detail/get_object_info__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace project_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetObjectInfo_Request_object_name
{
public:
  Init_GetObjectInfo_Request_object_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::project_interfaces::srv::GetObjectInfo_Request object_name(::project_interfaces::srv::GetObjectInfo_Request::_object_name_type arg)
  {
    msg_.object_name = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project_interfaces::srv::GetObjectInfo_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::project_interfaces::srv::GetObjectInfo_Request>()
{
  return project_interfaces::srv::builder::Init_GetObjectInfo_Request_object_name();
}

}  // namespace project_interfaces


namespace project_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetObjectInfo_Response_grasp_widths
{
public:
  explicit Init_GetObjectInfo_Response_grasp_widths(::project_interfaces::srv::GetObjectInfo_Response & msg)
  : msg_(msg)
  {}
  ::project_interfaces::srv::GetObjectInfo_Response grasp_widths(::project_interfaces::srv::GetObjectInfo_Response::_grasp_widths_type arg)
  {
    msg_.grasp_widths = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project_interfaces::srv::GetObjectInfo_Response msg_;
};

class Init_GetObjectInfo_Response_orientations
{
public:
  explicit Init_GetObjectInfo_Response_orientations(::project_interfaces::srv::GetObjectInfo_Response & msg)
  : msg_(msg)
  {}
  Init_GetObjectInfo_Response_grasp_widths orientations(::project_interfaces::srv::GetObjectInfo_Response::_orientations_type arg)
  {
    msg_.orientations = std::move(arg);
    return Init_GetObjectInfo_Response_grasp_widths(msg_);
  }

private:
  ::project_interfaces::srv::GetObjectInfo_Response msg_;
};

class Init_GetObjectInfo_Response_centers
{
public:
  explicit Init_GetObjectInfo_Response_centers(::project_interfaces::srv::GetObjectInfo_Response & msg)
  : msg_(msg)
  {}
  Init_GetObjectInfo_Response_orientations centers(::project_interfaces::srv::GetObjectInfo_Response::_centers_type arg)
  {
    msg_.centers = std::move(arg);
    return Init_GetObjectInfo_Response_orientations(msg_);
  }

private:
  ::project_interfaces::srv::GetObjectInfo_Response msg_;
};

class Init_GetObjectInfo_Response_object_count
{
public:
  Init_GetObjectInfo_Response_object_count()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetObjectInfo_Response_centers object_count(::project_interfaces::srv::GetObjectInfo_Response::_object_count_type arg)
  {
    msg_.object_count = std::move(arg);
    return Init_GetObjectInfo_Response_centers(msg_);
  }

private:
  ::project_interfaces::srv::GetObjectInfo_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::project_interfaces::srv::GetObjectInfo_Response>()
{
  return project_interfaces::srv::builder::Init_GetObjectInfo_Response_object_count();
}

}  // namespace project_interfaces

#endif  // PROJECT_INTERFACES__SRV__DETAIL__GET_OBJECT_INFO__BUILDER_HPP_
