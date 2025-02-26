// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from project_interfaces:srv/PromptJanice.idl
// generated code does not contain a copyright notice

#ifndef PROJECT_INTERFACES__SRV__DETAIL__PROMPT_JANICE__STRUCT_H_
#define PROJECT_INTERFACES__SRV__DETAIL__PROMPT_JANICE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'prompt'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/PromptJanice in the package project_interfaces.
typedef struct project_interfaces__srv__PromptJanice_Request
{
  rosidl_runtime_c__String prompt;
} project_interfaces__srv__PromptJanice_Request;

// Struct for a sequence of project_interfaces__srv__PromptJanice_Request.
typedef struct project_interfaces__srv__PromptJanice_Request__Sequence
{
  project_interfaces__srv__PromptJanice_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project_interfaces__srv__PromptJanice_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/PromptJanice in the package project_interfaces.
typedef struct project_interfaces__srv__PromptJanice_Response
{
  rosidl_runtime_c__String message;
} project_interfaces__srv__PromptJanice_Response;

// Struct for a sequence of project_interfaces__srv__PromptJanice_Response.
typedef struct project_interfaces__srv__PromptJanice_Response__Sequence
{
  project_interfaces__srv__PromptJanice_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} project_interfaces__srv__PromptJanice_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PROJECT_INTERFACES__SRV__DETAIL__PROMPT_JANICE__STRUCT_H_
