// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robotiq_2f_85_interfaces:srv/Robotiq2F85GripperCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_2F_85_INTERFACES__SRV__DETAIL__ROBOTIQ2_F85_GRIPPER_COMMAND__STRUCT_H_
#define ROBOTIQ_2F_85_INTERFACES__SRV__DETAIL__ROBOTIQ2_F85_GRIPPER_COMMAND__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/Robotiq2F85GripperCommand in the package robotiq_2f_85_interfaces.
typedef struct robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Request
{
  float width;
  float speed;
  float force;
} robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Request;

// Struct for a sequence of robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Request.
typedef struct robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Request__Sequence
{
  robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'log'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/Robotiq2F85GripperCommand in the package robotiq_2f_85_interfaces.
typedef struct robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Response
{
  bool success;
  rosidl_runtime_c__String log;
} robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Response;

// Struct for a sequence of robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Response.
typedef struct robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Response__Sequence
{
  robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robotiq_2f_85_interfaces__srv__Robotiq2F85GripperCommand_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOTIQ_2F_85_INTERFACES__SRV__DETAIL__ROBOTIQ2_F85_GRIPPER_COMMAND__STRUCT_H_
