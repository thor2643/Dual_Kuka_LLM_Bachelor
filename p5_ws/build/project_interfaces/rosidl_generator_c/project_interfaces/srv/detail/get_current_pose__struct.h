// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from project_interfaces:srv/GetCurrentPose.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__GET_CURRENT_POSE__STRUCT_H_
#define PROJECT_INTERFACES__SRV__DETAIL__GET_CURRENT_POSE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'arm'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/GetCurrentPose in the package project_interfaces.
typedef struct project_interfaces__srv__GetCurrentPose_Request
{
  rosidl_runtime_c__String arm;
} project_interfaces__srv__GetCurrentPose_Request;

// Struct for a sequence of project_interfaces__srv__GetCurrentPose_Request.
typedef struct project_interfaces__srv__GetCurrentPose_Request__Sequence
{
  project_interfaces__srv__GetCurrentPose_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project_interfaces__srv__GetCurrentPose_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'log'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/GetCurrentPose in the package project_interfaces.
typedef struct project_interfaces__srv__GetCurrentPose_Response
{
  geometry_msgs__msg__Pose pose;
  bool success;
  rosidl_runtime_c__String log;
} project_interfaces__srv__GetCurrentPose_Response;

// Struct for a sequence of project_interfaces__srv__GetCurrentPose_Response.
typedef struct project_interfaces__srv__GetCurrentPose_Response__Sequence
{
  project_interfaces__srv__GetCurrentPose_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project_interfaces__srv__GetCurrentPose_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PROJECT_INTERFACES__SRV__DETAIL__GET_CURRENT_POSE__STRUCT_H_
