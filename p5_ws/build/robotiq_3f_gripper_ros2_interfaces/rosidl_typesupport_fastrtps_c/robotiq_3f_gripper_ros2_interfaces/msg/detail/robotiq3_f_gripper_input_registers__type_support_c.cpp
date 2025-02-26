// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from robotiq_3f_gripper_ros2_interfaces:msg/Robotiq3FGripperInputRegisters.idl
// generated code does not contain a copyright notice
#include "robotiq_3f_gripper_ros2_interfaces/msg/detail/robotiq3_f_gripper_input_registers__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "robotiq_3f_gripper_ros2_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "robotiq_3f_gripper_ros2_interfaces/msg/detail/robotiq3_f_gripper_input_registers__struct.h"
#include "robotiq_3f_gripper_ros2_interfaces/msg/detail/robotiq3_f_gripper_input_registers__functions.h"
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


// forward declare type support functions


using _Robotiq3FGripperInputRegisters__ros_msg_type = robotiq_3f_gripper_ros2_interfaces__msg__Robotiq3FGripperInputRegisters;

static bool _Robotiq3FGripperInputRegisters__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _Robotiq3FGripperInputRegisters__ros_msg_type * ros_message = static_cast<const _Robotiq3FGripperInputRegisters__ros_msg_type *>(untyped_ros_message);
  // Field name: g_act
  {
    cdr << ros_message->g_act;
  }

  // Field name: g_mod
  {
    cdr << ros_message->g_mod;
  }

  // Field name: g_gto
  {
    cdr << ros_message->g_gto;
  }

  // Field name: g_imc
  {
    cdr << ros_message->g_imc;
  }

  // Field name: g_sta
  {
    cdr << ros_message->g_sta;
  }

  // Field name: g_flt
  {
    cdr << ros_message->g_flt;
  }

  // Field name: g_pra
  {
    cdr << ros_message->g_pra;
  }

  return true;
}

static bool _Robotiq3FGripperInputRegisters__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _Robotiq3FGripperInputRegisters__ros_msg_type * ros_message = static_cast<_Robotiq3FGripperInputRegisters__ros_msg_type *>(untyped_ros_message);
  // Field name: g_act
  {
    cdr >> ros_message->g_act;
  }

  // Field name: g_mod
  {
    cdr >> ros_message->g_mod;
  }

  // Field name: g_gto
  {
    cdr >> ros_message->g_gto;
  }

  // Field name: g_imc
  {
    cdr >> ros_message->g_imc;
  }

  // Field name: g_sta
  {
    cdr >> ros_message->g_sta;
  }

  // Field name: g_flt
  {
    cdr >> ros_message->g_flt;
  }

  // Field name: g_pra
  {
    cdr >> ros_message->g_pra;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_robotiq_3f_gripper_ros2_interfaces
size_t get_serialized_size_robotiq_3f_gripper_ros2_interfaces__msg__Robotiq3FGripperInputRegisters(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _Robotiq3FGripperInputRegisters__ros_msg_type * ros_message = static_cast<const _Robotiq3FGripperInputRegisters__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name g_act
  {
    size_t item_size = sizeof(ros_message->g_act);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name g_mod
  {
    size_t item_size = sizeof(ros_message->g_mod);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name g_gto
  {
    size_t item_size = sizeof(ros_message->g_gto);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name g_imc
  {
    size_t item_size = sizeof(ros_message->g_imc);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name g_sta
  {
    size_t item_size = sizeof(ros_message->g_sta);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name g_flt
  {
    size_t item_size = sizeof(ros_message->g_flt);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name g_pra
  {
    size_t item_size = sizeof(ros_message->g_pra);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _Robotiq3FGripperInputRegisters__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_robotiq_3f_gripper_ros2_interfaces__msg__Robotiq3FGripperInputRegisters(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_robotiq_3f_gripper_ros2_interfaces
size_t max_serialized_size_robotiq_3f_gripper_ros2_interfaces__msg__Robotiq3FGripperInputRegisters(
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

  // member: g_act
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: g_mod
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: g_gto
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: g_imc
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: g_sta
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: g_flt
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: g_pra
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
    using DataType = robotiq_3f_gripper_ros2_interfaces__msg__Robotiq3FGripperInputRegisters;
    is_plain =
      (
      offsetof(DataType, g_pra) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _Robotiq3FGripperInputRegisters__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_robotiq_3f_gripper_ros2_interfaces__msg__Robotiq3FGripperInputRegisters(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_Robotiq3FGripperInputRegisters = {
  "robotiq_3f_gripper_ros2_interfaces::msg",
  "Robotiq3FGripperInputRegisters",
  _Robotiq3FGripperInputRegisters__cdr_serialize,
  _Robotiq3FGripperInputRegisters__cdr_deserialize,
  _Robotiq3FGripperInputRegisters__get_serialized_size,
  _Robotiq3FGripperInputRegisters__max_serialized_size
};

static rosidl_message_type_support_t _Robotiq3FGripperInputRegisters__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_Robotiq3FGripperInputRegisters,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, robotiq_3f_gripper_ros2_interfaces, msg, Robotiq3FGripperInputRegisters)() {
  return &_Robotiq3FGripperInputRegisters__type_support;
}

#if defined(__cplusplus)
}
#endif
