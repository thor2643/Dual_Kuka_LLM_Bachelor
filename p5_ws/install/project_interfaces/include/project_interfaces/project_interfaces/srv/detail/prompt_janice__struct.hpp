// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from project_interfaces:srv/PromptJanice.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__PROMPT_JANICE__STRUCT_HPP_
#define PROJECT_INTERFACES__SRV__DETAIL__PROMPT_JANICE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__project_interfaces__srv__PromptJanice_Request __attribute__((deprecated))
#else
# define DEPRECATED__project_interfaces__srv__PromptJanice_Request __declspec(deprecated)
#endif

namespace project_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct PromptJanice_Request_
{
  using Type = PromptJanice_Request_<ContainerAllocator>;

  explicit PromptJanice_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->prompt = "";
    }
  }

  explicit PromptJanice_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : prompt(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->prompt = "";
    }
  }

  // field types and members
  using _prompt_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _prompt_type prompt;

  // setters for named parameter idiom
  Type & set__prompt(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->prompt = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    project_interfaces::srv::PromptJanice_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const project_interfaces::srv::PromptJanice_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<project_interfaces::srv::PromptJanice_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<project_interfaces::srv::PromptJanice_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::PromptJanice_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::PromptJanice_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::PromptJanice_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::PromptJanice_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<project_interfaces::srv::PromptJanice_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<project_interfaces::srv::PromptJanice_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__project_interfaces__srv__PromptJanice_Request
    std::shared_ptr<project_interfaces::srv::PromptJanice_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__project_interfaces__srv__PromptJanice_Request
    std::shared_ptr<project_interfaces::srv::PromptJanice_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PromptJanice_Request_ & other) const
  {
    if (this->prompt != other.prompt) {
      return false;
    }
    return true;
  }
  bool operator!=(const PromptJanice_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PromptJanice_Request_

// alias to use template instance with default allocator
using PromptJanice_Request =
  project_interfaces::srv::PromptJanice_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace project_interfaces


#ifndef _WIN32
# define DEPRECATED__project_interfaces__srv__PromptJanice_Response __attribute__((deprecated))
#else
# define DEPRECATED__project_interfaces__srv__PromptJanice_Response __declspec(deprecated)
#endif

namespace project_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct PromptJanice_Response_
{
  using Type = PromptJanice_Response_<ContainerAllocator>;

  explicit PromptJanice_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->message = "";
    }
  }

  explicit PromptJanice_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->message = "";
    }
  }

  // field types and members
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    project_interfaces::srv::PromptJanice_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const project_interfaces::srv::PromptJanice_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<project_interfaces::srv::PromptJanice_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<project_interfaces::srv::PromptJanice_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::PromptJanice_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::PromptJanice_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::PromptJanice_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::PromptJanice_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<project_interfaces::srv::PromptJanice_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<project_interfaces::srv::PromptJanice_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__project_interfaces__srv__PromptJanice_Response
    std::shared_ptr<project_interfaces::srv::PromptJanice_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__project_interfaces__srv__PromptJanice_Response
    std::shared_ptr<project_interfaces::srv::PromptJanice_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PromptJanice_Response_ & other) const
  {
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const PromptJanice_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PromptJanice_Response_

// alias to use template instance with default allocator
using PromptJanice_Response =
  project_interfaces::srv::PromptJanice_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace project_interfaces

namespace project_interfaces
{

namespace srv
{

struct PromptJanice
{
  using Request = project_interfaces::srv::PromptJanice_Request;
  using Response = project_interfaces::srv::PromptJanice_Response;
};

}  // namespace srv

}  // namespace project_interfaces

#endif  // PROJECT_INTERFACES__SRV__DETAIL__PROMPT_JANICE__STRUCT_HPP_
