// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from project_interfaces:srv/GetCurrentPose.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__GET_CURRENT_POSE__BUILDER_HPP_
#define PROJECT_INTERFACES__SRV__DETAIL__GET_CURRENT_POSE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "project_interfaces/srv/detail/get_current_pose__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace project_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetCurrentPose_Request_arm
{
public:
  Init_GetCurrentPose_Request_arm()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::project_interfaces::srv::GetCurrentPose_Request arm(::project_interfaces::srv::GetCurrentPose_Request::_arm_type arg)
  {
    msg_.arm = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project_interfaces::srv::GetCurrentPose_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::project_interfaces::srv::GetCurrentPose_Request>()
{
  return project_interfaces::srv::builder::Init_GetCurrentPose_Request_arm();
}

}  // namespace project_interfaces


namespace project_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetCurrentPose_Response_log
{
public:
  explicit Init_GetCurrentPose_Response_log(::project_interfaces::srv::GetCurrentPose_Response & msg)
  : msg_(msg)
  {}
  ::project_interfaces::srv::GetCurrentPose_Response log(::project_interfaces::srv::GetCurrentPose_Response::_log_type arg)
  {
    msg_.log = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project_interfaces::srv::GetCurrentPose_Response msg_;
};

class Init_GetCurrentPose_Response_success
{
public:
  explicit Init_GetCurrentPose_Response_success(::project_interfaces::srv::GetCurrentPose_Response & msg)
  : msg_(msg)
  {}
  Init_GetCurrentPose_Response_log success(::project_interfaces::srv::GetCurrentPose_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_GetCurrentPose_Response_log(msg_);
  }

private:
  ::project_interfaces::srv::GetCurrentPose_Response msg_;
};

class Init_GetCurrentPose_Response_pose
{
public:
  Init_GetCurrentPose_Response_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetCurrentPose_Response_success pose(::project_interfaces::srv::GetCurrentPose_Response::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return Init_GetCurrentPose_Response_success(msg_);
  }

private:
  ::project_interfaces::srv::GetCurrentPose_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::project_interfaces::srv::GetCurrentPose_Response>()
{
  return project_interfaces::srv::builder::Init_GetCurrentPose_Response_pose();
}

}  // namespace project_interfaces

#endif  // PROJECT_INTERFACES__SRV__DETAIL__GET_CURRENT_POSE__BUILDER_HPP_
