// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from project_interfaces:srv/ExecuteMoveCommand.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__EXECUTE_MOVE_COMMAND__BUILDER_HPP_
#define PROJECT_INTERFACES__SRV__DETAIL__EXECUTE_MOVE_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "project_interfaces/srv/detail/execute_move_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace project_interfaces
{

namespace srv
{

namespace builder
{

class Init_ExecuteMoveCommand_Request_execute
{
public:
  explicit Init_ExecuteMoveCommand_Request_execute(::project_interfaces::srv::ExecuteMoveCommand_Request & msg)
  : msg_(msg)
  {}
  ::project_interfaces::srv::ExecuteMoveCommand_Request execute(::project_interfaces::srv::ExecuteMoveCommand_Request::_execute_type arg)
  {
    msg_.execute = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project_interfaces::srv::ExecuteMoveCommand_Request msg_;
};

class Init_ExecuteMoveCommand_Request_arm
{
public:
  Init_ExecuteMoveCommand_Request_arm()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteMoveCommand_Request_execute arm(::project_interfaces::srv::ExecuteMoveCommand_Request::_arm_type arg)
  {
    msg_.arm = std::move(arg);
    return Init_ExecuteMoveCommand_Request_execute(msg_);
  }

private:
  ::project_interfaces::srv::ExecuteMoveCommand_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::project_interfaces::srv::ExecuteMoveCommand_Request>()
{
  return project_interfaces::srv::builder::Init_ExecuteMoveCommand_Request_arm();
}

}  // namespace project_interfaces


namespace project_interfaces
{

namespace srv
{

namespace builder
{

class Init_ExecuteMoveCommand_Response_log
{
public:
  explicit Init_ExecuteMoveCommand_Response_log(::project_interfaces::srv::ExecuteMoveCommand_Response & msg)
  : msg_(msg)
  {}
  ::project_interfaces::srv::ExecuteMoveCommand_Response log(::project_interfaces::srv::ExecuteMoveCommand_Response::_log_type arg)
  {
    msg_.log = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project_interfaces::srv::ExecuteMoveCommand_Response msg_;
};

class Init_ExecuteMoveCommand_Response_success
{
public:
  Init_ExecuteMoveCommand_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteMoveCommand_Response_log success(::project_interfaces::srv::ExecuteMoveCommand_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ExecuteMoveCommand_Response_log(msg_);
  }

private:
  ::project_interfaces::srv::ExecuteMoveCommand_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::project_interfaces::srv::ExecuteMoveCommand_Response>()
{
  return project_interfaces::srv::builder::Init_ExecuteMoveCommand_Response_success();
}

}  // namespace project_interfaces

#endif  // PROJECT_INTERFACES__SRV__DETAIL__EXECUTE_MOVE_COMMAND__BUILDER_HPP_
