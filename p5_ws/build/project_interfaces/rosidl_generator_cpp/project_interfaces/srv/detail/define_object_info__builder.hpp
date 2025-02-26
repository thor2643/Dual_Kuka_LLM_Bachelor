// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from project_interfaces:srv/DefineObjectInfo.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__DEFINE_OBJECT_INFO__BUILDER_HPP_
#define PROJECT_INTERFACES__SRV__DETAIL__DEFINE_OBJECT_INFO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "project_interfaces/srv/detail/define_object_info__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace project_interfaces
{

namespace srv
{

namespace builder
{

class Init_DefineObjectInfo_Request_object_name
{
public:
  Init_DefineObjectInfo_Request_object_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::project_interfaces::srv::DefineObjectInfo_Request object_name(::project_interfaces::srv::DefineObjectInfo_Request::_object_name_type arg)
  {
    msg_.object_name = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project_interfaces::srv::DefineObjectInfo_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::project_interfaces::srv::DefineObjectInfo_Request>()
{
  return project_interfaces::srv::builder::Init_DefineObjectInfo_Request_object_name();
}

}  // namespace project_interfaces


namespace project_interfaces
{

namespace srv
{

namespace builder
{

class Init_DefineObjectInfo_Response_success
{
public:
  Init_DefineObjectInfo_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::project_interfaces::srv::DefineObjectInfo_Response success(::project_interfaces::srv::DefineObjectInfo_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project_interfaces::srv::DefineObjectInfo_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::project_interfaces::srv::DefineObjectInfo_Response>()
{
  return project_interfaces::srv::builder::Init_DefineObjectInfo_Response_success();
}

}  // namespace project_interfaces

#endif  // PROJECT_INTERFACES__SRV__DETAIL__DEFINE_OBJECT_INFO__BUILDER_HPP_
