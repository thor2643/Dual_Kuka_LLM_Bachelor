// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from project_interfaces:srv/DefineObjectInfo.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__DEFINE_OBJECT_INFO__STRUCT_H_
#define PROJECT_INTERFACES__SRV__DETAIL__DEFINE_OBJECT_INFO__STRUCT_H_

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

/// Struct defined in srv/DefineObjectInfo in the package project_interfaces.
typedef struct project_interfaces__srv__DefineObjectInfo_Request
{
  /// Name of the object to adjust the value for
  rosidl_runtime_c__String object_name;
} project_interfaces__srv__DefineObjectInfo_Request;

// Struct for a sequence of project_interfaces__srv__DefineObjectInfo_Request.
typedef struct project_interfaces__srv__DefineObjectInfo_Request__Sequence
{
  project_interfaces__srv__DefineObjectInfo_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project_interfaces__srv__DefineObjectInfo_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/DefineObjectInfo in the package project_interfaces.
typedef struct project_interfaces__srv__DefineObjectInfo_Response
{
  bool success;
} project_interfaces__srv__DefineObjectInfo_Response;

// Struct for a sequence of project_interfaces__srv__DefineObjectInfo_Response.
typedef struct project_interfaces__srv__DefineObjectInfo_Response__Sequence
{
  project_interfaces__srv__DefineObjectInfo_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project_interfaces__srv__DefineObjectInfo_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PROJECT_INTERFACES__SRV__DETAIL__DEFINE_OBJECT_INFO__STRUCT_H_
