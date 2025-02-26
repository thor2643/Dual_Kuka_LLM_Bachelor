// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from project_interfaces:srv/ExecuteMoveCommand.idl
// generated code does not contain a copyright notice
#include "project_interfaces/srv/detail/execute_move_command__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "project_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "project_interfaces/srv/detail/execute_move_command__struct.h"
#include "project_interfaces/srv/detail/execute_move_command__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // arm
#include "rosidl_runtime_c/string_functions.h"  // arm

// forward declare type support functions


using _ExecuteMoveCommand_Request__ros_msg_type = project_interfaces__srv__ExecuteMoveCommand_Request;

static bool _ExecuteMoveCommand_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ExecuteMoveCommand_Request__ros_msg_type * ros_message = static_cast<const _ExecuteMoveCommand_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: arm
  {
    const rosidl_runtime_c__String * str = &ros_message->arm;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: execute
  {
    cdr << (ros_message->execute ? true : false);
  }

  return true;
}

static bool _ExecuteMoveCommand_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ExecuteMoveCommand_Request__ros_msg_type * ros_message = static_cast<_ExecuteMoveCommand_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: arm
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->arm.data) {
      rosidl_runtime_c__String__init(&ros_message->arm);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->arm,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'arm'\n");
      return false;
    }
  }

  // Field name: execute
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->execute = tmp ? true : false;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_project_interfaces
size_t get_serialized_size_project_interfaces__srv__ExecuteMoveCommand_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ExecuteMoveCommand_Request__ros_msg_type * ros_message = static_cast<const _ExecuteMoveCommand_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name arm
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->arm.size + 1);
  // field.name execute
  {
    size_t item_size = sizeof(ros_message->execute);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _ExecuteMoveCommand_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_project_interfaces__srv__ExecuteMoveCommand_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_project_interfaces
size_t max_serialized_size_project_interfaces__srv__ExecuteMoveCommand_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: arm
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: execute
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = project_interfaces__srv__ExecuteMoveCommand_Request;
    is_plain =
      (
      offsetof(DataType, execute) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _ExecuteMoveCommand_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_project_interfaces__srv__ExecuteMoveCommand_Request(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_ExecuteMoveCommand_Request = {
  "project_interfaces::srv",
  "ExecuteMoveCommand_Request",
  _ExecuteMoveCommand_Request__cdr_serialize,
  _ExecuteMoveCommand_Request__cdr_deserialize,
  _ExecuteMoveCommand_Request__get_serialized_size,
  _ExecuteMoveCommand_Request__max_serialized_size
};

static rosidl_message_type_support_t _ExecuteMoveCommand_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ExecuteMoveCommand_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, project_interfaces, srv, ExecuteMoveCommand_Request)() {
  return &_ExecuteMoveCommand_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "project_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "project_interfaces/srv/detail/execute_move_command__struct.h"
// already included above
// #include "project_interfaces/srv/detail/execute_move_command__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

// already included above
// #include "rosidl_runtime_c/string.h"  // log
// already included above
// #include "rosidl_runtime_c/string_functions.h"  // log

// forward declare type support functions


using _ExecuteMoveCommand_Response__ros_msg_type = project_interfaces__srv__ExecuteMoveCommand_Response;

static bool _ExecuteMoveCommand_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ExecuteMoveCommand_Response__ros_msg_type * ros_message = static_cast<const _ExecuteMoveCommand_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: success
  {
    cdr << (ros_message->success ? true : false);
  }

  // Field name: log
  {
    const rosidl_runtime_c__String * str = &ros_message->log;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _ExecuteMoveCommand_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ExecuteMoveCommand_Response__ros_msg_type * ros_message = static_cast<_ExecuteMoveCommand_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: success
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->success = tmp ? true : false;
  }

  // Field name: log
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->log.data) {
      rosidl_runtime_c__String__init(&ros_message->log);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->log,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'log'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_project_interfaces
size_t get_serialized_size_project_interfaces__srv__ExecuteMoveCommand_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ExecuteMoveCommand_Response__ros_msg_type * ros_message = static_cast<const _ExecuteMoveCommand_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name success
  {
    size_t item_size = sizeof(ros_message->success);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name log
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->log.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _ExecuteMoveCommand_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_project_interfaces__srv__ExecuteMoveCommand_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_project_interfaces
size_t max_serialized_size_project_interfaces__srv__ExecuteMoveCommand_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: success
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: log
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = project_interfaces__srv__ExecuteMoveCommand_Response;
    is_plain =
      (
      offsetof(DataType, log) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _ExecuteMoveCommand_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_project_interfaces__srv__ExecuteMoveCommand_Response(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_ExecuteMoveCommand_Response = {
  "project_interfaces::srv",
  "ExecuteMoveCommand_Response",
  _ExecuteMoveCommand_Response__cdr_serialize,
  _ExecuteMoveCommand_Response__cdr_deserialize,
  _ExecuteMoveCommand_Response__get_serialized_size,
  _ExecuteMoveCommand_Response__max_serialized_size
};

static rosidl_message_type_support_t _ExecuteMoveCommand_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ExecuteMoveCommand_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, project_interfaces, srv, ExecuteMoveCommand_Response)() {
  return &_ExecuteMoveCommand_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "project_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "project_interfaces/srv/execute_move_command.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t ExecuteMoveCommand__callbacks = {
  "project_interfaces::srv",
  "ExecuteMoveCommand",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, project_interfaces, srv, ExecuteMoveCommand_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, project_interfaces, srv, ExecuteMoveCommand_Response)(),
};

static rosidl_service_type_support_t ExecuteMoveCommand__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &ExecuteMoveCommand__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, project_interfaces, srv, ExecuteMoveCommand)() {
  return &ExecuteMoveCommand__handle;
}

#if defined(__cplusplus)
}
#endif
