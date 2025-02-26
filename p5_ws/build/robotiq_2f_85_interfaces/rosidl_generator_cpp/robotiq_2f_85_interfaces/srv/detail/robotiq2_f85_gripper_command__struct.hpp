// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robotiq_2f_85_interfaces:srv/Robotiq2F85GripperCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_2F_85_INTERFACES__SRV__DETAIL__ROBOTIQ2_F85_GRIPPER_COMMAND__STRUCT_HPP_
#define ROBOTIQ_2F_85_INTERFACES__SRV__DETAIL__ROBOTIQ2_F85_GRIPPER_COMMAND__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Request __attribute__((deprecated))
#else
# define DEPRECATED__robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Request __declspec(deprecated)
#endif

namespace robotiq_2f_85_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Robotiq2F85GripperCommand_Request_
{
  using Type = Robotiq2F85GripperCommand_Request_<ContainerAllocator>;

  explicit Robotiq2F85GripperCommand_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->width = 0.0f;
      this->speed = 0.0f;
      this->force = 0.0f;
    }
  }

  explicit Robotiq2F85GripperCommand_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->width = 0.0f;
      this->speed = 0.0f;
      this->force = 0.0f;
    }
  }

  // field types and members
  using _width_type =
    float;
  _width_type width;
  using _speed_type =
    float;
  _speed_type speed;
  using _force_type =
    float;
  _force_type force;

  // setters for named parameter idiom
  Type & set__width(
    const float & _arg)
  {
    this->width = _arg;
    return *this;
  }
  Type & set__speed(
    const float & _arg)
  {
    this->speed = _arg;
    return *this;
  }
  Type & set__force(
    const float & _arg)
  {
    this->force = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Request
    std::shared_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Request
    std::shared_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Robotiq2F85GripperCommand_Request_ & other) const
  {
    if (this->width != other.width) {
      return false;
    }
    if (this->speed != other.speed) {
      return false;
    }
    if (this->force != other.force) {
      return false;
    }
    return true;
  }
  bool operator!=(const Robotiq2F85GripperCommand_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Robotiq2F85GripperCommand_Request_

// alias to use template instance with default allocator
using Robotiq2F85GripperCommand_Request =
  robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace robotiq_2f_85_interfaces


#ifndef _WIN32
# define DEPRECATED__robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Response __attribute__((deprecated))
#else
# define DEPRECATED__robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Response __declspec(deprecated)
#endif

namespace robotiq_2f_85_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Robotiq2F85GripperCommand_Response_
{
  using Type = Robotiq2F85GripperCommand_Response_<ContainerAllocator>;

  explicit Robotiq2F85GripperCommand_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->log = "";
    }
  }

  explicit Robotiq2F85GripperCommand_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Response
    std::shared_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Response
    std::shared_ptr<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Robotiq2F85GripperCommand_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->log != other.log) {
      return false;
    }
    return true;
  }
  bool operator!=(const Robotiq2F85GripperCommand_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Robotiq2F85GripperCommand_Response_

// alias to use template instance with default allocator
using Robotiq2F85GripperCommand_Response =
  robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace robotiq_2f_85_interfaces

namespace robotiq_2f_85_interfaces
{

namespace srv
{

struct Robotiq2F85GripperCommand
{
  using Request = robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request;
  using Response = robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response;
};

}  // namespace srv

}  // namespace robotiq_2f_85_interfaces

#endif  // ROBOTIQ_2F_85_INTERFACES__SRV__DETAIL__ROBOTIQ2_F85_GRIPPER_COMMAND__STRUCT_HPP_
