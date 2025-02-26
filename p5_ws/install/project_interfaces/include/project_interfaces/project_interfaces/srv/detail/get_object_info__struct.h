// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from project_interfaces:srv/GetObjectInfo.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__GET_OBJECT_INFO__STRUCT_H_
#define PROJECT_INTERFACES__SRV__DETAIL__GET_OBJECT_INFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'object_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/GetObjectInfo in the package project_interfaces.
typedef struct project_interfaces__srv__GetObjectInfo_Request
{
  /// Name of the object to search for
  rosidl_runtime_c__String object_name;
} project_interfaces__srv__GetObjectInfo_Request;

// Struct for a sequence of project_interfaces__srv__GetObjectInfo_Request.
typedef struct project_interfaces__srv__GetObjectInfo_Request__Sequence
{
  project_interfaces__srv__GetObjectInfo_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project_interfaces__srv__GetObjectInfo_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'centers'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'orientations'
// Member 'grasp_widths'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in srv/GetObjectInfo in the package project_interfaces.
typedef struct project_interfaces__srv__GetObjectInfo_Response
{
  /// The number of objects found
  int32_t object_count;
  /// The center coordinates (X, Y, Z) of each object found
  geometry_msgs__msg__Point__Sequence centers;
  /// The orientation of each object (in angle)
  rosidl_runtime_c__float__Sequence orientations;
  /// The grasping width of each object found
  rosidl_runtime_c__float__Sequence grasp_widths;
} project_interfaces__srv__GetObjectInfo_Response;

// Struct for a sequence of project_interfaces__srv__GetObjectInfo_Response.
typedef struct project_interfaces__srv__GetObjectInfo_Response__Sequence
{
  project_interfaces__srv__GetObjectInfo_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project_interfaces__srv__GetObjectInfo_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PROJECT_INTERFACES__SRV__DETAIL__GET_OBJECT_INFO__STRUCT_H_
