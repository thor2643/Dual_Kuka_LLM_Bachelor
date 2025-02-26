// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from project_interfaces:srv/PromptJanice.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__PROMPT_JANICE__BUILDER_HPP_
#define PROJECT_INTERFACES__SRV__DETAIL__PROMPT_JANICE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "project_interfaces/srv/detail/prompt_janice__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace project_interfaces
{

namespace srv
{

namespace builder
{

class Init_PromptJanice_Request_prompt
{
public:
  Init_PromptJanice_Request_prompt()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::project_interfaces::srv::PromptJanice_Request prompt(::project_interfaces::srv::PromptJanice_Request::_prompt_type arg)
  {
    msg_.prompt = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project_interfaces::srv::PromptJanice_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::project_interfaces::srv::PromptJanice_Request>()
{
  return project_interfaces::srv::builder::Init_PromptJanice_Request_prompt();
}

}  // namespace project_interfaces


namespace project_interfaces
{

namespace srv
{

namespace builder
{

class Init_PromptJanice_Response_message
{
public:
  Init_PromptJanice_Response_message()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::project_interfaces::srv::PromptJanice_Response message(::project_interfaces::srv::PromptJanice_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::project_interfaces::srv::PromptJanice_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::project_interfaces::srv::PromptJanice_Response>()
{
  return project_interfaces::srv::builder::Init_PromptJanice_Response_message();
}

}  // namespace project_interfaces

#endif  // PROJECT_INTERFACES__SRV__DETAIL__PROMPT_JANICE__BUILDER_HPP_
