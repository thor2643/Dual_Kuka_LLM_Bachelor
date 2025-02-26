// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from robotiq_3f_gripper_ros2_interfaces:msg/Robotiq3FGripperInputRegisters.idl
// generated code does not contain a copyright notice
#include "robotiq_3f_gripper_ros2_interfaces/msg/detail/robotiq3_f_gripper_input_registers__rosidl_typesupport_fastrtps_cpp.hpp"
#include "robotiq_3f_gripper_ros2_interfaces/msg/detail/robotiq3_f_gripper_input_registers__struct.hpp"

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

namespace robotiq_3f_gripper_ros2_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_3f_gripper_ros2_interfaces
cdr_serialize(
  const robotiq_3f_gripper_ros2_interfaces::msg::Robotiq3FGripperInputRegisters & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: g_act
  cdr << ros_message.g_act;
  // Member: g_mod
  cdr << ros_message.g_mod;
  // Member: g_gto
  cdr << ros_message.g_gto;
  // Member: g_imc
  cdr << ros_message.g_imc;
  // Member: g_sta
  cdr << ros_message.g_sta;
  // Member: g_flt
  cdr << ros_message.g_flt;
  // Member: g_pra
  cdr << ros_message.g_pra;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_3f_gripper_ros2_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  robotiq_3f_gripper_ros2_interfaces::msg::Robotiq3FGripperInputRegisters & ros_message)
{
  // Member: g_act
  cdr >> ros_message.g_act;

  // Member: g_mod
  cdr >> ros_message.g_mod;

  // Member: g_gto
  cdr >> ros_message.g_gto;

  // Member: g_imc
  cdr >> ros_message.g_imc;

  // Member: g_sta
  cdr >> ros_message.g_sta;

  // Member: g_flt
  cdr >> ros_message.g_flt;

  // Member: g_pra
  cdr >> ros_message.g_pra;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_3f_gripper_ros2_interfaces
get_serialized_size(
  const robotiq_3f_gripper_ros2_interfaces::msg::Robotiq3FGripperInputRegisters & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: g_act
  {
    size_t item_size = sizeof(ros_message.g_act);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: g_mod
  {
    size_t item_size = sizeof(ros_message.g_mod);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: g_gto
  {
    size_t item_size = sizeof(ros_message.g_gto);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: g_imc
  {
    size_t item_size = sizeof(ros_message.g_imc);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: g_sta
  {
    size_t item_size = sizeof(ros_message.g_sta);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: g_flt
  {
    size_t item_size = sizeof(ros_message.g_flt);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: g_pra
  {
    size_t item_size = sizeof(ros_message.g_pra);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_3f_gripper_ros2_interfaces
max_serialized_size_Robotiq3FGripperInputRegisters(
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


  // Member: g_act
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: g_mod
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: g_gto
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: g_imc
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: g_sta
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: g_flt
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: g_pra
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
    using DataType = robotiq_3f_gripper_ros2_interfaces::msg::Robotiq3FGripperInputRegisters;
    is_plain =
      (
      offsetof(DataType, g_pra) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _Robotiq3FGripperInputRegisters__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const robotiq_3f_gripper_ros2_interfaces::msg::Robotiq3FGripperInputRegisters *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _Robotiq3FGripperInputRegisters__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<robotiq_3f_gripper_ros2_interfaces::msg::Robotiq3FGripperInputRegisters *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _Robotiq3FGripperInputRegisters__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const robotiq_3f_gripper_ros2_interfaces::msg::Robotiq3FGripperInputRegisters *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _Robotiq3FGripperInputRegisters__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_Robotiq3FGripperInputRegisters(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _Robotiq3FGripperInputRegisters__callbacks = {
  "robotiq_3f_gripper_ros2_interfaces::msg",
  "Robotiq3FGripperInputRegisters",
  _Robotiq3FGripperInputRegisters__cdr_serialize,
  _Robotiq3FGripperInputRegisters__cdr_deserialize,
  _Robotiq3FGripperInputRegisters__get_serialized_size,
  _Robotiq3FGripperInputRegisters__max_serialized_size
};

static rosidl_message_type_support_t _Robotiq3FGripperInputRegisters__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Robotiq3FGripperInputRegisters__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace robotiq_3f_gripper_ros2_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_robotiq_3f_gripper_ros2_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<robotiq_3f_gripper_ros2_interfaces::msg::Robotiq3FGripperInputRegisters>()
{
  return &robotiq_3f_gripper_ros2_interfaces::msg::typesupport_fastrtps_cpp::_Robotiq3FGripperInputRegisters__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, robotiq_3f_gripper_ros2_interfaces, msg, Robotiq3FGripperInputRegisters)() {
  return &robotiq_3f_gripper_ros2_interfaces::msg::typesupport_fastrtps_cpp::_Robotiq3FGripperInputRegisters__handle;
}

#ifdef __cplusplus
}
#endif
