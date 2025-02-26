// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from project_interfaces:srv/GetObjectInfo.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__GET_OBJECT_INFO__STRUCT_HPP_
#define PROJECT_INTERFACES__SRV__DETAIL__GET_OBJECT_INFO__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__project_interfaces__srv__GetObjectInfo_Request __attribute__((deprecated))
#else
# define DEPRECATED__project_interfaces__srv__GetObjectInfo_Request __declspec(deprecated)
#endif

namespace project_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetObjectInfo_Request_
{
  using Type = GetObjectInfo_Request_<ContainerAllocator>;

  explicit GetObjectInfo_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->object_name = "";
    }
  }

  explicit GetObjectInfo_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    project_interfaces::srv::GetObjectInfo_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const project_interfaces::srv::GetObjectInfo_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<project_interfaces::srv::GetObjectInfo_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<project_interfaces::srv::GetObjectInfo_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::GetObjectInfo_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::GetObjectInfo_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::GetObjectInfo_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::GetObjectInfo_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<project_interfaces::srv::GetObjectInfo_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<project_interfaces::srv::GetObjectInfo_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__project_interfaces__srv__GetObjectInfo_Request
    std::shared_ptr<project_interfaces::srv::GetObjectInfo_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__project_interfaces__srv__GetObjectInfo_Request
    std::shared_ptr<project_interfaces::srv::GetObjectInfo_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetObjectInfo_Request_ & other) const
  {
    if (this->object_name != other.object_name) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetObjectInfo_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetObjectInfo_Request_

// alias to use template instance with default allocator
using GetObjectInfo_Request =
  project_interfaces::srv::GetObjectInfo_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace project_interfaces


// Include directives for member types
// Member 'centers'
#include "geometry_msgs/msg/detail/point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__project_interfaces__srv__GetObjectInfo_Response __attribute__((deprecated))
#else
# define DEPRECATED__project_interfaces__srv__GetObjectInfo_Response __declspec(deprecated)
#endif

namespace project_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetObjectInfo_Response_
{
  using Type = GetObjectInfo_Response_<ContainerAllocator>;

  explicit GetObjectInfo_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->object_count = 0l;
    }
  }

  explicit GetObjectInfo_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->object_count = 0l;
    }
  }

  // field types and members
  using _object_count_type =
    int32_t;
  _object_count_type object_count;
  using _centers_type =
    std::vector<geometry_msgs::msg::Point_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point_<ContainerAllocator>>>;
  _centers_type centers;
  using _orientations_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _orientations_type orientations;
  using _grasp_widths_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _grasp_widths_type grasp_widths;

  // setters for named parameter idiom
  Type & set__object_count(
    const int32_t & _arg)
  {
    this->object_count = _arg;
    return *this;
  }
  Type & set__centers(
    const std::vector<geometry_msgs::msg::Point_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point_<ContainerAllocator>>> & _arg)
  {
    this->centers = _arg;
    return *this;
  }
  Type & set__orientations(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->orientations = _arg;
    return *this;
  }
  Type & set__grasp_widths(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->grasp_widths = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    project_interfaces::srv::GetObjectInfo_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const project_interfaces::srv::GetObjectInfo_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<project_interfaces::srv::GetObjectInfo_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<project_interfaces::srv::GetObjectInfo_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::GetObjectInfo_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::GetObjectInfo_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      project_interfaces::srv::GetObjectInfo_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<project_interfaces::srv::GetObjectInfo_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<project_interfaces::srv::GetObjectInfo_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<project_interfaces::srv::GetObjectInfo_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__project_interfaces__srv__GetObjectInfo_Response
    std::shared_ptr<project_interfaces::srv::GetObjectInfo_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__project_interfaces__srv__GetObjectInfo_Response
    std::shared_ptr<project_interfaces::srv::GetObjectInfo_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetObjectInfo_Response_ & other) const
  {
    if (this->object_count != other.object_count) {
      return false;
    }
    if (this->centers != other.centers) {
      return false;
    }
    if (this->orientations != other.orientations) {
      return false;
    }
    if (this->grasp_widths != other.grasp_widths) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetObjectInfo_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetObjectInfo_Response_

// alias to use template instance with default allocator
using GetObjectInfo_Response =
  project_interfaces::srv::GetObjectInfo_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace project_interfaces

namespace project_interfaces
{

namespace srv
{

struct GetObjectInfo
{
  using Request = project_interfaces::srv::GetObjectInfo_Request;
  using Response = project_interfaces::srv::GetObjectInfo_Response;
};

}  // namespace srv

}  // namespace project_interfaces

#endif  // PROJECT_INTERFACES__SRV__DETAIL__GET_OBJECT_INFO__STRUCT_HPP_
