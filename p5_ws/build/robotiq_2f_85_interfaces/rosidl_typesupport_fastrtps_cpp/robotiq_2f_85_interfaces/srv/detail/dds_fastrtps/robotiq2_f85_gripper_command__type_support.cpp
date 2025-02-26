// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from robotiq_2f_85_interfaces:srv/Robotiq2F85GripperCommand.idl
// generated code does not contain a copyright notice
#include "robotiq_2f_85_interfaces/srv/detail/robotiq2_f85_gripper_command__rosidl_typesupport_fastrtps_cpp.hpp"
#include "robotiq_2f_85_interfaces/srv/detail/robotiq2_f85_gripper_command__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace robotiq_2f_85_interfaces
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
cdr_serialize(
  const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: width
  cdr << ros_message.width;
  // Member: speed
  cdr << ros_message.speed;
  // Member: force
  cdr << ros_message.force;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request & ros_message)
{
  // Member: width
  cdr >> ros_message.width;

  // Member: speed
  cdr >> ros_message.speed;

  // Member: force
  cdr >> ros_message.force;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
get_serialized_size(
  const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: width
  {
    size_t item_size = sizeof(ros_message.width);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: speed
  {
    size_t item_size = sizeof(ros_message.speed);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: force
  {
    size_t item_size = sizeof(ros_message.force);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
max_serialized_size_Robotiq2F85GripperCommand_Request(
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


  // Member: width
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: speed
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: force
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request;
    is_plain =
      (
      offsetof(DataType, force) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _Robotiq2F85GripperCommand_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _Robotiq2F85GripperCommand_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _Robotiq2F85GripperCommand_Request__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _Robotiq2F85GripperCommand_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_Robotiq2F85GripperCommand_Request(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _Robotiq2F85GripperCommand_Request__callbacks = {
  "robotiq_2f_85_interfaces::srv",
  "Robotiq2F85GripperCommand_Request",
  _Robotiq2F85GripperCommand_Request__cdr_serialize,
  _Robotiq2F85GripperCommand_Request__cdr_deserialize,
  _Robotiq2F85GripperCommand_Request__get_serialized_size,
  _Robotiq2F85GripperCommand_Request__max_serialized_size
};

static rosidl_message_type_support_t _Robotiq2F85GripperCommand_Request__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Robotiq2F85GripperCommand_Request__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace robotiq_2f_85_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_robotiq_2f_85_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Request>()
{
  return &robotiq_2f_85_interfaces::srv::typesupport_fastrtps_cpp::_Robotiq2F85GripperCommand_Request__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, robotiq_2f_85_interfaces, srv, Robotiq2F85GripperCommand_Request)() {
  return &robotiq_2f_85_interfaces::srv::typesupport_fastrtps_cpp::_Robotiq2F85GripperCommand_Request__handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include <limits>
// already included above
// #include <stdexcept>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
// already included above
// #include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace robotiq_2f_85_interfaces
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
cdr_serialize(
  const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: success
  cdr << (ros_message.success ? true : false);
  // Member: log
  cdr << ros_message.log;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response & ros_message)
{
  // Member: success
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.success = tmp ? true : false;
  }

  // Member: log
  cdr >> ros_message.log;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
get_serialized_size(
  const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: success
  {
    size_t item_size = sizeof(ros_message.success);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: log
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.log.size() + 1);

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_2f_85_interfaces
max_serialized_size_Robotiq2F85GripperCommand_Response(
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


  // Member: success
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: log
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
    using DataType = robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response;
    is_plain =
      (
      offsetof(DataType, log) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _Robotiq2F85GripperCommand_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _Robotiq2F85GripperCommand_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _Robotiq2F85GripperCommand_Response__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _Robotiq2F85GripperCommand_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_Robotiq2F85GripperCommand_Response(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _Robotiq2F85GripperCommand_Response__callbacks = {
  "robotiq_2f_85_interfaces::srv",
  "Robotiq2F85GripperCommand_Response",
  _Robotiq2F85GripperCommand_Response__cdr_serialize,
  _Robotiq2F85GripperCommand_Response__cdr_deserialize,
  _Robotiq2F85GripperCommand_Response__get_serialized_size,
  _Robotiq2F85GripperCommand_Response__max_serialized_size
};

static rosidl_message_type_support_t _Robotiq2F85GripperCommand_Response__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Robotiq2F85GripperCommand_Response__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace robotiq_2f_85_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_robotiq_2f_85_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand_Response>()
{
  return &robotiq_2f_85_interfaces::srv::typesupport_fastrtps_cpp::_Robotiq2F85GripperCommand_Response__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, robotiq_2f_85_interfaces, srv, Robotiq2F85GripperCommand_Response)() {
  return &robotiq_2f_85_interfaces::srv::typesupport_fastrtps_cpp::_Robotiq2F85GripperCommand_Response__handle;
}

#ifdef __cplusplus
}
#endif

#include "rmw/error_handling.h"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/service_type_support_decl.hpp"

namespace robotiq_2f_85_interfaces
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

static service_type_support_callbacks_t _Robotiq2F85GripperCommand__callbacks = {
  "robotiq_2f_85_interfaces::srv",
  "Robotiq2F85GripperCommand",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, robotiq_2f_85_interfaces, srv, Robotiq2F85GripperCommand_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, robotiq_2f_85_interfaces, srv, Robotiq2F85GripperCommand_Response)(),
};

static rosidl_service_type_support_t _Robotiq2F85GripperCommand__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Robotiq2F85GripperCommand__callbacks,
  get_service_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace robotiq_2f_85_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_robotiq_2f_85_interfaces
const rosidl_service_type_support_t *
get_service_type_support_handle<robotiq_2f_85_interfaces::srv::Robotiq2F85GripperCommand>()
{
  return &robotiq_2f_85_interfaces::srv::typesupport_fastrtps_cpp::_Robotiq2F85GripperCommand__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, robotiq_2f_85_interfaces, srv, Robotiq2F85GripperCommand)() {
  return &robotiq_2f_85_interfaces::srv::typesupport_fastrtps_cpp::_Robotiq2F85GripperCommand__handle;
}

#ifdef __cplusplus
}
#endif
