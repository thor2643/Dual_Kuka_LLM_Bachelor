// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from project_interfaces:srv/DefineObjectInfo.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__DEFINE_OBJECT_INFO__STRUCT_HPP_
#define PROJECT_INTERFACES__SRV__DETAIL__DEFINE_OBJECT_INFO__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__project_interfaces__srv__DefineObjectInfo_Request __attribute__((deprecated))
#else
# define DEPRECATED__project_interfaces__srv__DefineObjectInfo_Request __declspec(deprecated)
#endif

namespace project_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct DefineObjectInfo_Request_
{
  using Type = DefineObjectInfo_Request_<ContainerAllocator>;

  explicit DefineObjectInfo_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->object_name = "";
    }
  }

  explicit DefineObjectInfo_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : object_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->object_name = "";
    }
  }

  // field types and members
  using _object_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _object_name_type object_name;

  // setters for named parameter idiom
  Type & set__object_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->object_name = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    project_interfaces::srv::DefineObjectInfo_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const project_interfaces::srv::DefineObjectInfo_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<project_interfaces::srv::DefineObjectInfo_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<project_interfaces::srv::DefineObjectInfo_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::DefineObjectInfo_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::DefineObjectInfo_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::DefineObjectInfo_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::DefineObjectInfo_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<project_interfaces::srv::DefineObjectInfo_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<project_interfaces::srv::DefineObjectInfo_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__project_interfaces__srv__DefineObjectInfo_Request
    std::shared_ptr<project_interfaces::srv::DefineObjectInfo_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__project_interfaces__srv__DefineObjectInfo_Request
    std::shared_ptr<project_interfaces::srv::DefineObjectInfo_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DefineObjectInfo_Request_ & other) const
  {
    if (this->object_name != other.object_name) {
      return false;
    }
    return true;
  }
  bool operator!=(const DefineObjectInfo_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DefineObjectInfo_Request_

// alias to use template instance with default allocator
using DefineObjectInfo_Request =
  project_interfaces::srv::DefineObjectInfo_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace project_interfaces


#ifndef _WIN32
# define DEPRECATED__project_interfaces__srv__DefineObjectInfo_Response __attribute__((deprecated))
#else
# define DEPRECATED__project_interfaces__srv__DefineObjectInfo_Response __declspec(deprecated)
#endif

namespace project_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct DefineObjectInfo_Response_
{
  using Type = DefineObjectInfo_Response_<ContainerAllocator>;

  explicit DefineObjectInfo_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  explicit DefineObjectInfo_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    project_interfaces::srv::DefineObjectInfo_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const project_interfaces::srv::DefineObjectInfo_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<project_interfaces::srv::DefineObjectInfo_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<project_interfaces::srv::DefineObjectInfo_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::DefineObjectInfo_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::DefineObjectInfo_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::DefineObjectInfo_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::DefineObjectInfo_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<project_interfaces::srv::DefineObjectInfo_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<project_interfaces::srv::DefineObjectInfo_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__project_interfaces__srv__DefineObjectInfo_Response
    std::shared_ptr<project_interfaces::srv::DefineObjectInfo_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__project_interfaces__srv__DefineObjectInfo_Response
    std::shared_ptr<project_interfaces::srv::DefineObjectInfo_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DefineObjectInfo_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    return true;
  }
  bool operator!=(const DefineObjectInfo_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DefineObjectInfo_Response_

// alias to use template instance with default allocator
using DefineObjectInfo_Response =
  project_interfaces::srv::DefineObjectInfo_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace project_interfaces

namespace project_interfaces
{

namespace srv
{

struct DefineObjectInfo
{
  using Request = project_interfaces::srv::DefineObjectInfo_Request;
  using Response = project_interfaces::srv::DefineObjectInfo_Response;
};

}  // namespace srv

}  // namespace project_interfaces

#endif  // PROJECT_INTERFACES__SRV__DETAIL__DEFINE_OBJECT_INFO__STRUCT_HPP_
