// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from project_interfaces:srv/PlanMoveCommand.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__PLAN_MOVE_COMMAND__STRUCT_H_
#define PROJECT_INTERFACES__SRV__DETAIL__PLAN_MOVE_COMMAND__STRUCT_H_

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
// Member 'position'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'orientation'
#include "geometry_msgs/msg/detail/quaternion__struct.h"

/// Struct defined in srv/PlanMoveCommand in the package project_interfaces.
typedef struct project_interfaces__srv__PlanMoveCommand_Request
{
  /// Define which arm to use
  rosidl_runtime_c__String arm;
  /// The center coordinates (X, Y, Z) of each object found
  geometry_msgs__msg__Point position;
  /// Name of the object to search for
  geometry_msgs__msg__Quaternion orientation;
} project_interfaces__srv__PlanMoveCommand_Request;

// Struct for a sequence of project_interfaces__srv__PlanMoveCommand_Request.
typedef struct project_interfaces__srv__PlanMoveCommand_Request__Sequence
{
  project_interfaces__srv__PlanMoveCommand_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project_interfaces__srv__PlanMoveCommand_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'log'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/PlanMoveCommand in the package project_interfaces.
typedef struct project_interfaces__srv__PlanMoveCommand_Response
{
  /// The number of objects found
  bool success;
  rosidl_runtime_c__String log;
} project_interfaces__srv__PlanMoveCommand_Response;

// Struct for a sequence of project_interfaces__srv__PlanMoveCommand_Response.
typedef struct project_interfaces__srv__PlanMoveCommand_Response__Sequence
{
  project_interfaces__srv__PlanMoveCommand_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project_interfaces__srv__PlanMoveCommand_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PROJECT_INTERFACES__SRV__DETAIL__PLAN_MOVE_COMMAND__STRUCT_H_
