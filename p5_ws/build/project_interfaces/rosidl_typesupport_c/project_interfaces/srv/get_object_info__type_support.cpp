// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from project_interfaces:srv/GetObjectInfo.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "project_interfaces/srv/detail/get_object_info__struct.h"
#include "project_interfaces/srv/detail/get_object_info__type_support.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace project_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _GetObjectInfo_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetObjectInfo_Request_type_support_ids_t;

static const _GetObjectInfo_Request_type_support_ids_t _GetObjectInfo_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _GetObjectInfo_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetObjectInfo_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetObjectInfo_Request_type_support_symbol_names_t _GetObjectInfo_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, project_interfaces, srv, GetObjectInfo_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, project_interfaces, srv, GetObjectInfo_Request)),
  }
};

typedef struct _GetObjectInfo_Request_type_support_data_t
{
  void * data[2];
} _GetObjectInfo_Request_type_support_data_t;

static _GetObjectInfo_Request_type_support_data_t _GetObjectInfo_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetObjectInfo_Request_message_typesupport_map = {
  2,
  "project_interfaces",
  &_GetObjectInfo_Request_message_typesupport_ids.typesupport_identifier[0],
  &_GetObjectInfo_Request_message_typesupport_symbol_names.symbol_name[0],
  &_GetObjectInfo_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GetObjectInfo_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetObjectInfo_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace project_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, project_interfaces, srv, GetObjectInfo_Request)() {
  return &::project_interfaces::srv::rosidl_typesupport_c::GetObjectInfo_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "project_interfaces/srv/detail/get_object_info__struct.h"
// already included above
// #include "project_interfaces/srv/detail/get_object_info__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace project_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _GetObjectInfo_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetObjectInfo_Response_type_support_ids_t;

static const _GetObjectInfo_Response_type_support_ids_t _GetObjectInfo_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _GetObjectInfo_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetObjectInfo_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetObjectInfo_Response_type_support_symbol_names_t _GetObjectInfo_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, project_interfaces, srv, GetObjectInfo_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, project_interfaces, srv, GetObjectInfo_Response)),
  }
};

typedef struct _GetObjectInfo_Response_type_support_data_t
{
  void * data[2];
} _GetObjectInfo_Response_type_support_data_t;

static _GetObjectInfo_Response_type_support_data_t _GetObjectInfo_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetObjectInfo_Response_message_typesupport_map = {
  2,
  "project_interfaces",
  &_GetObjectInfo_Response_message_typesupport_ids.typesupport_identifier[0],
  &_GetObjectInfo_Response_message_typesupport_symbol_names.symbol_name[0],
  &_GetObjectInfo_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GetObjectInfo_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetObjectInfo_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace project_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, project_interfaces, srv, GetObjectInfo_Response)() {
  return &::project_interfaces::srv::rosidl_typesupport_c::GetObjectInfo_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "project_interfaces/srv/detail/get_object_info__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace project_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _GetObjectInfo_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetObjectInfo_type_support_ids_t;

static const _GetObjectInfo_type_support_ids_t _GetObjectInfo_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _GetObjectInfo_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetObjectInfo_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetObjectInfo_type_support_symbol_names_t _GetObjectInfo_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, project_interfaces, srv, GetObjectInfo)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, project_interfaces, srv, GetObjectInfo)),
  }
};

typedef struct _GetObjectInfo_type_support_data_t
{
  void * data[2];
} _GetObjectInfo_type_support_data_t;

static _GetObjectInfo_type_support_data_t _GetObjectInfo_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetObjectInfo_service_typesupport_map = {
  2,
  "project_interfaces",
  &_GetObjectInfo_service_typesupport_ids.typesupport_identifier[0],
  &_GetObjectInfo_service_typesupport_symbol_names.symbol_name[0],
  &_GetObjectInfo_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t GetObjectInfo_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetObjectInfo_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace project_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, project_interfaces, srv, GetObjectInfo)() {
  return &::project_interfaces::srv::rosidl_typesupport_c::GetObjectInfo_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif
