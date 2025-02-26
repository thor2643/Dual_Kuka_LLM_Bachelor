// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from project_interfaces:srv/PlanMoveCommand.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__PLAN_MOVE_COMMAND__BUILDER_HPP_
#define PROJECT_INTERFACES__SRV__DETAIL__PLAN_MOVE_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "project_interfaces/srv/detail/plan_move_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace project_interfaces
{

namespace srv
{

namespace builder
{

class Init_PlanMoveCommand_Request_orientation
{
public:
  explicit Init_PlanMoveCommand_Request_orientation(::project_interfaces::srv::PlanMoveCommand_Request & msg)
  : msg_(msg)
  {}
  ::project_interfaces::srv::PlanMoveCommand_Request orientation(::project_interfaces::srv::PlanMoveCommand_Request::_orientation_type arg)
  {
    msg_.orientation = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project_interfaces::srv::PlanMoveCommand_Request msg_;
};

class Init_PlanMoveCommand_Request_position
{
public:
  explicit Init_PlanMoveCommand_Request_position(::project_interfaces::srv::PlanMoveCommand_Request & msg)
  : msg_(msg)
  {}
  Init_PlanMoveCommand_Request_orientation position(::project_interfaces::srv::PlanMoveCommand_Request::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_PlanMoveCommand_Request_orientation(msg_);
  }

private:
  ::project_interfaces::srv::PlanMoveCommand_Request msg_;
};

class Init_PlanMoveCommand_Request_arm
{
public:
  Init_PlanMoveCommand_Request_arm()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanMoveCommand_Request_position arm(::project_interfaces::srv::PlanMoveCommand_Request::_arm_type arg)
  {
    msg_.arm = std::move(arg);
    return Init_PlanMoveCommand_Request_position(msg_);
  }

private:
  ::project_interfaces::srv::PlanMoveCommand_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::project_interfaces::srv::PlanMoveCommand_Request>()
{
  return project_interfaces::srv::builder::Init_PlanMoveCommand_Request_arm();
}

}  // namespace project_interfaces


namespace project_interfaces
{

namespace srv
{

namespace builder
{

class Init_PlanMoveCommand_Response_log
{
public:
  explicit Init_PlanMoveCommand_Response_log(::project_interfaces::srv::PlanMoveCommand_Response & msg)
  : msg_(msg)
  {}
  ::project_interfaces::srv::PlanMoveCommand_Response log(::project_interfaces::srv::PlanMoveCommand_Response::_log_type arg)
  {
    msg_.log = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project_interfaces::srv::PlanMoveCommand_Response msg_;
};

class Init_PlanMoveCommand_Response_success
{
public:
  Init_PlanMoveCommand_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanMoveCommand_Response_log success(::project_interfaces::srv::PlanMoveCommand_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_PlanMoveCommand_Response_log(msg_);
  }

private:
  ::project_interfaces::srv::PlanMoveCommand_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::project_interfaces::srv::PlanMoveCommand_Response>()
{
  return project_interfaces::srv::builder::Init_PlanMoveCommand_Response_success();
}

}  // namespace project_interfaces

#endif  // PROJECT_INTERFACES__SRV__DETAIL__PLAN_MOVE_COMMAND__BUILDER_HPP_
