// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from project_interfaces:srv/GetCurrentPose.idl
// generated code does not contain a copyright notice
#include "project_interfaces/srv/detail/get_current_pose__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `arm`
#include "rosidl_runtime_c/string_functions.h"

bool
project_interfaces__srv__GetCurrentPose_Request__init(project_interfaces__srv__GetCurrentPose_Request * msg)
{
  if (!msg) {
    return false;
  }
  // arm
  if (!rosidl_runtime_c__String__init(&msg->arm)) {
    project_interfaces__srv__GetCurrentPose_Request__fini(msg);
    return false;
  }
  return true;
}

void
project_interfaces__srv__GetCurrentPose_Request__fini(project_interfaces__srv__GetCurrentPose_Request * msg)
{
  if (!msg) {
    return;
  }
  // arm
  rosidl_runtime_c__String__fini(&msg->arm);
}

bool
project_interfaces__srv__GetCurrentPose_Request__are_equal(const project_interfaces__srv__GetCurrentPose_Request * lhs, const project_interfaces__srv__GetCurrentPose_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // arm
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->arm), &(rhs->arm)))
  {
    return false;
  }
  return true;
}

bool
project_interfaces__srv__GetCurrentPose_Request__copy(
  const project_interfaces__srv__GetCurrentPose_Request * input,
  project_interfaces__srv__GetCurrentPose_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // arm
  if (!rosidl_runtime_c__String__copy(
      &(input->arm), &(output->arm)))
  {
    return false;
  }
  return true;
}

project_interfaces__srv__GetCurrentPose_Request *
project_interfaces__srv__GetCurrentPose_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project_interfaces__srv__GetCurrentPose_Request * msg = (project_interfaces__srv__GetCurrentPose_Request *)allocator.allocate(sizeof(project_interfaces__srv__GetCurrentPose_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(project_interfaces__srv__GetCurrentPose_Request));
  bool success = project_interfaces__srv__GetCurrentPose_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
project_interfaces__srv__GetCurrentPose_Request__destroy(project_interfaces__srv__GetCurrentPose_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    project_interfaces__srv__GetCurrentPose_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
project_interfaces__srv__GetCurrentPose_Request__Sequence__init(project_interfaces__srv__GetCurrentPose_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project_interfaces__srv__GetCurrentPose_Request * data = NULL;

  if (size) {
    data = (project_interfaces__srv__GetCurrentPose_Request *)allocator.zero_allocate(size, sizeof(project_interfaces__srv__GetCurrentPose_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = project_interfaces__srv__GetCurrentPose_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        project_interfaces__srv__GetCurrentPose_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
project_interfaces__srv__GetCurrentPose_Request__Sequence__fini(project_interfaces__srv__GetCurrentPose_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      project_interfaces__srv__GetCurrentPose_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

project_interfaces__srv__GetCurrentPose_Request__Sequence *
project_interfaces__srv__GetCurrentPose_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project_interfaces__srv__GetCurrentPose_Request__Sequence * array = (project_interfaces__srv__GetCurrentPose_Request__Sequence *)allocator.allocate(sizeof(project_interfaces__srv__GetCurrentPose_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = project_interfaces__srv__GetCurrentPose_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
project_interfaces__srv__GetCurrentPose_Request__Sequence__destroy(project_interfaces__srv__GetCurrentPose_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    project_interfaces__srv__GetCurrentPose_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
project_interfaces__srv__GetCurrentPose_Request__Sequence__are_equal(const project_interfaces__srv__GetCurrentPose_Request__Sequence * lhs, const project_interfaces__srv__GetCurrentPose_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!project_interfaces__srv__GetCurrentPose_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
project_interfaces__srv__GetCurrentPose_Request__Sequence__copy(
  const project_interfaces__srv__GetCurrentPose_Request__Sequence * input,
  project_interfaces__srv__GetCurrentPose_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(project_interfaces__srv__GetCurrentPose_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    project_interfaces__srv__GetCurrentPose_Request * data =
      (project_interfaces__srv__GetCurrentPose_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!project_interfaces__srv__GetCurrentPose_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          project_interfaces__srv__GetCurrentPose_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!project_interfaces__srv__GetCurrentPose_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `pose`
#include "geometry_msgs/msg/detail/pose__functions.h"
// Member `log`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
project_interfaces__srv__GetCurrentPose_Response__init(project_interfaces__srv__GetCurrentPose_Response * msg)
{
  if (!msg) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__init(&msg->pose)) {
    project_interfaces__srv__GetCurrentPose_Response__fini(msg);
    return false;
  }
  // success
  // log
  if (!rosidl_runtime_c__String__init(&msg->log)) {
    project_interfaces__srv__GetCurrentPose_Response__fini(msg);
    return false;
  }
  return true;
}

void
project_interfaces__srv__GetCurrentPose_Response__fini(project_interfaces__srv__GetCurrentPose_Response * msg)
{
  if (!msg) {
    return;
  }
  // pose
  geometry_msgs__msg__Pose__fini(&msg->pose);
  // success
  // log
  rosidl_runtime_c__String__fini(&msg->log);
}

bool
project_interfaces__srv__GetCurrentPose_Response__are_equal(const project_interfaces__srv__GetCurrentPose_Response * lhs, const project_interfaces__srv__GetCurrentPose_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->pose), &(rhs->pose)))
  {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // log
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->log), &(rhs->log)))
  {
    return false;
  }
  return true;
}

bool
project_interfaces__srv__GetCurrentPose_Response__copy(
  const project_interfaces__srv__GetCurrentPose_Response * input,
  project_interfaces__srv__GetCurrentPose_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->pose), &(output->pose)))
  {
    return false;
  }
  // success
  output->success = input->success;
  // log
  if (!rosidl_runtime_c__String__copy(
      &(input->log), &(output->log)))
  {
    return false;
  }
  return true;
}

project_interfaces__srv__GetCurrentPose_Response *
project_interfaces__srv__GetCurrentPose_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project_interfaces__srv__GetCurrentPose_Response * msg = (project_interfaces__srv__GetCurrentPose_Response *)allocator.allocate(sizeof(project_interfaces__srv__GetCurrentPose_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(project_interfaces__srv__GetCurrentPose_Response));
  bool success = project_interfaces__srv__GetCurrentPose_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
project_interfaces__srv__GetCurrentPose_Response__destroy(project_interfaces__srv__GetCurrentPose_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    project_interfaces__srv__GetCurrentPose_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
project_interfaces__srv__GetCurrentPose_Response__Sequence__init(project_interfaces__srv__GetCurrentPose_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project_interfaces__srv__GetCurrentPose_Response * data = NULL;

  if (size) {
    data = (project_interfaces__srv__GetCurrentPose_Response *)allocator.zero_allocate(size, sizeof(project_interfaces__srv__GetCurrentPose_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = project_interfaces__srv__GetCurrentPose_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        project_interfaces__srv__GetCurrentPose_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
project_interfaces__srv__GetCurrentPose_Response__Sequence__fini(project_interfaces__srv__GetCurrentPose_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      project_interfaces__srv__GetCurrentPose_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

project_interfaces__srv__GetCurrentPose_Response__Sequence *
project_interfaces__srv__GetCurrentPose_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  project_interfaces__srv__GetCurrentPose_Response__Sequence * array = (project_interfaces__srv__GetCurrentPose_Response__Sequence *)allocator.allocate(sizeof(project_interfaces__srv__GetCurrentPose_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = project_interfaces__srv__GetCurrentPose_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
project_interfaces__srv__GetCurrentPose_Response__Sequence__destroy(project_interfaces__srv__GetCurrentPose_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    project_interfaces__srv__GetCurrentPose_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
project_interfaces__srv__GetCurrentPose_Response__Sequence__are_equal(const project_interfaces__srv__GetCurrentPose_Response__Sequence * lhs, const project_interfaces__srv__GetCurrentPose_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!project_interfaces__srv__GetCurrentPose_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
project_interfaces__srv__GetCurrentPose_Response__Sequence__copy(
  const project_interfaces__srv__GetCurrentPose_Response__Sequence * input,
  project_interfaces__srv__GetCurrentPose_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(project_interfaces__srv__GetCurrentPose_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    project_interfaces__srv__GetCurrentPose_Response * data =
      (project_interfaces__srv__GetCurrentPose_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!project_interfaces__srv__GetCurrentPose_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          project_interfaces__srv__GetCurrentPose_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!project_interfaces__srv__GetCurrentPose_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
