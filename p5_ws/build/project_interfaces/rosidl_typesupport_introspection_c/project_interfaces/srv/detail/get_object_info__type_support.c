// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from project_interfaces:srv/GetObjectInfo.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "project_interfaces/srv/detail/get_object_info__rosidl_typesupport_introspection_c.h"
#include "project_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "project_interfaces/srv/detail/get_object_info__functions.h"
#include "project_interfaces/srv/detail/get_object_info__struct.h"


// Include directives for member types
// Member `object_name`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void project_interfaces__srv__GetObjectInfo_Request__rosidl_typesupport_introspection_c__GetObjectInfo_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  project_interfaces__srv__GetObjectInfo_Request__init(message_memory);
}

void project_interfaces__srv__GetObjectInfo_Request__rosidl_typesupport_introspection_c__GetObjectInfo_Request_fini_function(void * message_memory)
{
  project_interfaces__srv__GetObjectInfo_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember project_interfaces__srv__GetObjectInfo_Request__rosidl_typesupport_introspection_c__GetObjectInfo_Request_message_member_array[1] = {
  {
    "object_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(project_interfaces__srv__GetObjectInfo_Request, object_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers project_interfaces__srv__GetObjectInfo_Request__rosidl_typesupport_introspection_c__GetObjectInfo_Request_message_members = {
  "project_interfaces__srv",  // message namespace
  "GetObjectInfo_Request",  // message name
  1,  // number of fields
  sizeof(project_interfaces__srv__GetObjectInfo_Request),
  project_interfaces__srv__GetObjectInfo_Request__rosidl_typesupport_introspection_c__GetObjectInfo_Request_message_member_array,  // message members
  project_interfaces__srv__GetObjectInfo_Request__rosidl_typesupport_introspection_c__GetObjectInfo_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  project_interfaces__srv__GetObjectInfo_Request__rosidl_typesupport_introspection_c__GetObjectInfo_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t project_interfaces__srv__GetObjectInfo_Request__rosidl_typesupport_introspection_c__GetObjectInfo_Request_message_type_support_handle = {
  0,
  &project_interfaces__srv__GetObjectInfo_Request__rosidl_typesupport_introspection_c__GetObjectInfo_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_project_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, project_interfaces, srv, GetObjectInfo_Request)() {
  if (!project_interfaces__srv__GetObjectInfo_Request__rosidl_typesupport_introspection_c__GetObjectInfo_Request_message_type_support_handle.typesupport_identifier) {
    project_interfaces__srv__GetObjectInfo_Request__rosidl_typesupport_introspection_c__GetObjectInfo_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &project_interfaces__srv__GetObjectInfo_Request__rosidl_typesupport_introspection_c__GetObjectInfo_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "project_interfaces/srv/detail/get_object_info__rosidl_typesupport_introspection_c.h"
// already included above
// #include "project_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "project_interfaces/srv/detail/get_object_info__functions.h"
// already included above
// #include "project_interfaces/srv/detail/get_object_info__struct.h"


// Include directives for member types
// Member `centers`
#include "geometry_msgs/msg/point.h"
// Member `centers`
#include "geometry_msgs/msg/detail/point__rosidl_typesupport_introspection_c.h"
// Member `orientations`
// Member `grasp_widths`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__GetObjectInfo_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  project_interfaces__srv__GetObjectInfo_Response__init(message_memory);
}

void project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__GetObjectInfo_Response_fini_function(void * message_memory)
{
  project_interfaces__srv__GetObjectInfo_Response__fini(message_memory);
}

size_t project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__size_function__GetObjectInfo_Response__centers(
  const void * untyped_member)
{
  const geometry_msgs__msg__Point__Sequence * member =
    (const geometry_msgs__msg__Point__Sequence *)(untyped_member);
  return member->size;
}

const void * project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetObjectInfo_Response__centers(
  const void * untyped_member, size_t index)
{
  const geometry_msgs__msg__Point__Sequence * member =
    (const geometry_msgs__msg__Point__Sequence *)(untyped_member);
  return &member->data[index];
}

void * project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_function__GetObjectInfo_Response__centers(
  void * untyped_member, size_t index)
{
  geometry_msgs__msg__Point__Sequence * member =
    (geometry_msgs__msg__Point__Sequence *)(untyped_member);
  return &member->data[index];
}

void project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetObjectInfo_Response__centers(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const geometry_msgs__msg__Point * item =
    ((const geometry_msgs__msg__Point *)
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetObjectInfo_Response__centers(untyped_member, index));
  geometry_msgs__msg__Point * value =
    (geometry_msgs__msg__Point *)(untyped_value);
  *value = *item;
}

void project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetObjectInfo_Response__centers(
  void * untyped_member, size_t index, const void * untyped_value)
{
  geometry_msgs__msg__Point * item =
    ((geometry_msgs__msg__Point *)
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_function__GetObjectInfo_Response__centers(untyped_member, index));
  const geometry_msgs__msg__Point * value =
    (const geometry_msgs__msg__Point *)(untyped_value);
  *item = *value;
}

bool project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__resize_function__GetObjectInfo_Response__centers(
  void * untyped_member, size_t size)
{
  geometry_msgs__msg__Point__Sequence * member =
    (geometry_msgs__msg__Point__Sequence *)(untyped_member);
  geometry_msgs__msg__Point__Sequence__fini(member);
  return geometry_msgs__msg__Point__Sequence__init(member, size);
}

size_t project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__size_function__GetObjectInfo_Response__orientations(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetObjectInfo_Response__orientations(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_function__GetObjectInfo_Response__orientations(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetObjectInfo_Response__orientations(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetObjectInfo_Response__orientations(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetObjectInfo_Response__orientations(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_function__GetObjectInfo_Response__orientations(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__resize_function__GetObjectInfo_Response__orientations(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

size_t project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__size_function__GetObjectInfo_Response__grasp_widths(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetObjectInfo_Response__grasp_widths(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_function__GetObjectInfo_Response__grasp_widths(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetObjectInfo_Response__grasp_widths(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetObjectInfo_Response__grasp_widths(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetObjectInfo_Response__grasp_widths(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_function__GetObjectInfo_Response__grasp_widths(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__resize_function__GetObjectInfo_Response__grasp_widths(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__GetObjectInfo_Response_message_member_array[4] = {
  {
    "object_count",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(project_interfaces__srv__GetObjectInfo_Response, object_count),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "centers",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(project_interfaces__srv__GetObjectInfo_Response, centers),  // bytes offset in struct
    NULL,  // default value
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__size_function__GetObjectInfo_Response__centers,  // size() function pointer
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetObjectInfo_Response__centers,  // get_const(index) function pointer
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_function__GetObjectInfo_Response__centers,  // get(index) function pointer
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetObjectInfo_Response__centers,  // fetch(index, &value) function pointer
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetObjectInfo_Response__centers,  // assign(index, value) function pointer
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__resize_function__GetObjectInfo_Response__centers  // resize(index) function pointer
  },
  {
    "orientations",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(project_interfaces__srv__GetObjectInfo_Response, orientations),  // bytes offset in struct
    NULL,  // default value
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__size_function__GetObjectInfo_Response__orientations,  // size() function pointer
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetObjectInfo_Response__orientations,  // get_const(index) function pointer
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_function__GetObjectInfo_Response__orientations,  // get(index) function pointer
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetObjectInfo_Response__orientations,  // fetch(index, &value) function pointer
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetObjectInfo_Response__orientations,  // assign(index, value) function pointer
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__resize_function__GetObjectInfo_Response__orientations  // resize(index) function pointer
  },
  {
    "grasp_widths",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(project_interfaces__srv__GetObjectInfo_Response, grasp_widths),  // bytes offset in struct
    NULL,  // default value
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__size_function__GetObjectInfo_Response__grasp_widths,  // size() function pointer
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetObjectInfo_Response__grasp_widths,  // get_const(index) function pointer
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__get_function__GetObjectInfo_Response__grasp_widths,  // get(index) function pointer
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetObjectInfo_Response__grasp_widths,  // fetch(index, &value) function pointer
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetObjectInfo_Response__grasp_widths,  // assign(index, value) function pointer
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__resize_function__GetObjectInfo_Response__grasp_widths  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__GetObjectInfo_Response_message_members = {
  "project_interfaces__srv",  // message namespace
  "GetObjectInfo_Response",  // message name
  4,  // number of fields
  sizeof(project_interfaces__srv__GetObjectInfo_Response),
  project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__GetObjectInfo_Response_message_member_array,  // message members
  project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__GetObjectInfo_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__GetObjectInfo_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__GetObjectInfo_Response_message_type_support_handle = {
  0,
  &project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__GetObjectInfo_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_project_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, project_interfaces, srv, GetObjectInfo_Response)() {
  project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__GetObjectInfo_Response_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Point)();
  if (!project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__GetObjectInfo_Response_message_type_support_handle.typesupport_identifier) {
    project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__GetObjectInfo_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &project_interfaces__srv__GetObjectInfo_Response__rosidl_typesupport_introspection_c__GetObjectInfo_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "project_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "project_interfaces/srv/detail/get_object_info__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers project_interfaces__srv__detail__get_object_info__rosidl_typesupport_introspection_c__GetObjectInfo_service_members = {
  "project_interfaces__srv",  // service namespace
  "GetObjectInfo",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // project_interfaces__srv__detail__get_object_info__rosidl_typesupport_introspection_c__GetObjectInfo_Request_message_type_support_handle,
  NULL  // response message
  // project_interfaces__srv__detail__get_object_info__rosidl_typesupport_introspection_c__GetObjectInfo_Response_message_type_support_handle
};

static rosidl_service_type_support_t project_interfaces__srv__detail__get_object_info__rosidl_typesupport_introspection_c__GetObjectInfo_service_type_support_handle = {
  0,
  &project_interfaces__srv__detail__get_object_info__rosidl_typesupport_introspection_c__GetObjectInfo_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, project_interfaces, srv, GetObjectInfo_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, project_interfaces, srv, GetObjectInfo_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_project_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, project_interfaces, srv, GetObjectInfo)() {
  if (!project_interfaces__srv__detail__get_object_info__rosidl_typesupport_introspection_c__GetObjectInfo_service_type_support_handle.typesupport_identifier) {
    project_interfaces__srv__detail__get_object_info__rosidl_typesupport_introspection_c__GetObjectInfo_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)project_interfaces__srv__detail__get_object_info__rosidl_typesupport_introspection_c__GetObjectInfo_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, project_interfaces, srv, GetObjectInfo_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, project_interfaces, srv, GetObjectInfo_Response)()->data;
  }

  return &project_interfaces__srv__detail__get_object_info__rosidl_typesupport_introspection_c__GetObjectInfo_service_type_support_handle;
}
