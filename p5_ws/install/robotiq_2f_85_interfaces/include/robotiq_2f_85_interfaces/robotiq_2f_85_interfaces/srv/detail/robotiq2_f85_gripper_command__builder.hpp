// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robotiq_2f_85_interfaces:srv/Robotiq2F85GripperCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_2F_85_INTERFACES__SRV__DETAIL__ROBOTIQ2_F85_GRIPPER_COMMAND__BUILDER_HPP_
#define ROBOTIQ_2F_85_INTERFACES__SRV__DETAIL__ROBOTIQ2_F85_GRIPPER_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robotiq_2f_85_interfaces/srv/detail/robotiq2_f85_gripper_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robotiq_2f_85_interfaces
{

namespace srv
{

namespace builder
{

class Init_Robotiq2F85GripperCommand_Request_force
{
public:
  explicit Init_Robotiq2F85GripperCommand_Request_force(::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request & msg)
  : msg_(msg)
  {}
  ::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request force(::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request::_force_type arg)
  {
    msg_.force = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request msg_;
};

class Init_Robotiq2F85GripperCommand_Request_speed
{
public:
  explicit Init_Robotiq2F85GripperCommand_Request_speed(::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request & msg)
  : msg_(msg)
  {}
  Init_Robotiq2F85GripperCommand_Request_force speed(::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request::_speed_type arg)
  {
    msg_.speed = std::move(arg);
    return Init_Robotiq2F85GripperCommand_Request_force(msg_);
  }

private:
  ::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request msg_;
};

class Init_Robotiq2F85GripperCommand_Request_width
{
public:
  Init_Robotiq2F85GripperCommand_Request_width()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Robotiq2F85GripperCommand_Request_speed width(::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request::_width_type arg)
  {
    msg_.width = std::move(arg);
    return Init_Robotiq2F85GripperCommand_Request_speed(msg_);
  }

private:
  ::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request>()
{
  return robotiq_2f_85_interfaces::srv::builder::Init_Robotiq2F85GripperCommand_Request_width();
}

}  // namespace robotiq_2f_85_interfaces


namespace robotiq_2f_85_interfaces
{

namespace srv
{

namespace builder
{

class Init_Robotiq2F85GripperCommand_Response_log
{
public:
  explicit Init_Robotiq2F85GripperCommand_Response_log(::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response & msg)
  : msg_(msg)
  {}
  ::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response log(::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response::_log_type arg)
  {
    msg_.log = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response msg_;
};

class Init_Robotiq2F85GripperCommand_Response_success
{
public:
  Init_Robotiq2F85GripperCommand_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Robotiq2F85GripperCommand_Response_log success(::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_Robotiq2F85GripperCommand_Response_log(msg_);
  }

private:
  ::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response>()
{
  return robotiq_2f_85_interfaces::srv::builder::Init_Robotiq2F85GripperCommand_Response_success();
}

}  // namespace robotiq_2f_85_interfaces

#endif  // ROBOTIQ_2F_85_INTERFACES__SRV__DETAIL__ROBOTIQ2_F85_GRIPPER_COMMAND__BUILDER_HPP_
