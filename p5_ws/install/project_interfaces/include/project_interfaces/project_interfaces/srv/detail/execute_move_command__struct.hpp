// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from project_interfaces:srv/ExecuteMoveCommand.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__EXECUTE_MOVE_COMMAND__STRUCT_HPP_
#define PROJECT_INTERFACES__SRV__DETAIL__EXECUTE_MOVE_COMMAND__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__project_interfaces__srv__ExecuteMoveCommand_Request __attribute__((deprecated))
#else
# define DEPRECATED__project_interfaces__srv__ExecuteMoveCommand_Request __declspec(deprecated)
#endif

namespace project_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ExecuteMoveCommand_Request_
{
  using Type = ExecuteMoveCommand_Request_<ContainerAllocator>;

  explicit ExecuteMoveCommand_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->arm = "";
      this->execute = false;
    }
  }

  explicit ExecuteMoveCommand_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : arm(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->arm = "";
      this->execute = false;
    }
  }

  // field types and members
  using _arm_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _arm_type arm;
  using _execute_type =
    bool;
  _execute_type execute;

  // setters for named parameter idiom
  Type & set__arm(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->arm = _arg;
    return *this;
  }
  Type & set__execute(
    const bool & _arg)
  {
    this->execute = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    project_interfaces::srv::ExecuteMoveCommand_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const project_interfaces::srv::ExecuteMoveCommand_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<project_interfaces::srv::ExecuteMoveCommand_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<project_interfaces::srv::ExecuteMoveCommand_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::ExecuteMoveCommand_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::ExecuteMoveCommand_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::ExecuteMoveCommand_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::ExecuteMoveCommand_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<project_interfaces::srv::ExecuteMoveCommand_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<project_interfaces::srv::ExecuteMoveCommand_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__project_interfaces__srv__ExecuteMoveCommand_Request
    std::shared_ptr<project_interfaces::srv::ExecuteMoveCommand_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__project_interfaces__srv__ExecuteMoveCommand_Request
    std::shared_ptr<project_interfaces::srv::ExecuteMoveCommand_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteMoveCommand_Request_ & other) const
  {
    if (this->arm != other.arm) {
      return false;
    }
    if (this->execute != other.execute) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteMoveCommand_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteMoveCommand_Request_

// alias to use template instance with default allocator
using ExecuteMoveCommand_Request =
  project_interfaces::srv::ExecuteMoveCommand_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace project_interfaces


#ifndef _WIN32
# define DEPRECATED__project_interfaces__srv__ExecuteMoveCommand_Response __attribute__((deprecated))
#else
# define DEPRECATED__project_interfaces__srv__ExecuteMoveCommand_Response __declspec(deprecated)
#endif

namespace project_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ExecuteMoveCommand_Response_
{
  using Type = ExecuteMoveCommand_Response_<ContainerAllocator>;

  explicit ExecuteMoveCommand_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->log = "";
    }
  }

  explicit ExecuteMoveCommand_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : log(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->log = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _log_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _log_type log;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__log(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->log = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    project_interfaces::srv::ExecuteMoveCommand_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const project_interfaces::srv::ExecuteMoveCommand_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<project_interfaces::srv::ExecuteMoveCommand_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<project_interfaces::srv::ExecuteMoveCommand_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::ExecuteMoveCommand_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::ExecuteMoveCommand_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::ExecuteMoveCommand_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::ExecuteMoveCommand_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<project_interfaces::srv::ExecuteMoveCommand_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<project_interfaces::srv::ExecuteMoveCommand_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__project_interfaces__srv__ExecuteMoveCommand_Response
    std::shared_ptr<project_interfaces::srv::ExecuteMoveCommand_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__project_interfaces__srv__ExecuteMoveCommand_Response
    std::shared_ptr<project_interfaces::srv::ExecuteMoveCommand_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteMoveCommand_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->log != other.log) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteMoveCommand_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteMoveCommand_Response_

// alias to use template instance with default allocator
using ExecuteMoveCommand_Response =
  project_interfaces::srv::ExecuteMoveCommand_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace project_interfaces

namespace project_interfaces
{

namespace srv
{

struct ExecuteMoveCommand
{
  using Request = project_interfaces::srv::ExecuteMoveCommand_Request;
  using Response = project_interfaces::srv::ExecuteMoveCommand_Response;
};

}  // namespace srv

}  // namespace project_interfaces

#endif  // PROJECT_INTERFACES__SRV__DETAIL__EXECUTE_MOVE_COMMAND__STRUCT_HPP_
