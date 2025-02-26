// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from robotiq_3f_gripper_ros2_interfaces:msg/Robotiq3FGripperOutputRegisters.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "robotiq_3f_gripper_ros2_interfaces/msg/detail/robotiq3_f_gripper_output_registers__struct.h"
#include "robotiq_3f_gripper_ros2_interfaces/msg/detail/robotiq3_f_gripper_output_registers__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool robotiq_3f_gripper_ros2_interfaces__msg__robotiq3_f_gripper_output_registers__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[108];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("robotiq_3f_gripper_ros2_interfaces.msg._robotiq3_f_gripper_output_registers.Robotiq3FGripperOutputRegisters", full_classname_dest, 107) == 0);
  }
  robotiq_3f_gripper_ros2_interfaces__msg__Robotiq3FGripperOutputRegisters * ros_message = _ros_message;
  {  // r_act
    PyObject * field = PyObject_GetAttrString(_pymsg, "r_act");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->r_act = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // r_mod
    PyObject * field = PyObject_GetAttrString(_pymsg, "r_mod");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->r_mod = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // r_gto
    PyObject * field = PyObject_GetAttrString(_pymsg, "r_gto");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->r_gto = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // r_atr
    PyObject * field = PyObject_GetAttrString(_pymsg, "r_atr");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->r_atr = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // r_pra
    PyObject * field = PyObject_GetAttrString(_pymsg, "r_pra");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->r_pra = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // r_spa
    PyObject * field = PyObject_GetAttrString(_pymsg, "r_spa");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->r_spa = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // r_fra
    PyObject * field = PyObject_GetAttrString(_pymsg, "r_fra");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->r_fra = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * robotiq_3f_gripper_ros2_interfaces__msg__robotiq3_f_gripper_output_registers__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of Robotiq3FGripperOutputRegisters */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("robotiq_3f_gripper_ros2_interfaces.msg._robotiq3_f_gripper_output_registers");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "Robotiq3FGripperOutputRegisters");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  robotiq_3f_gripper_ros2_interfaces__msg__Robotiq3FGripperOutputRegisters * ros_message = (robotiq_3f_gripper_ros2_interfaces__msg__Robotiq3FGripperOutputRegisters *)raw_ros_message;
  {  // r_act
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->r_act);
    {
      int rc = PyObject_SetAttrString(_pymessage, "r_act", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // r_mod
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->r_mod);
    {
      int rc = PyObject_SetAttrString(_pymessage, "r_mod", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // r_gto
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->r_gto);
    {
      int rc = PyObject_SetAttrString(_pymessage, "r_gto", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // r_atr
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->r_atr);
    {
      int rc = PyObject_SetAttrString(_pymessage, "r_atr", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // r_pra
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->r_pra);
    {
      int rc = PyObject_SetAttrString(_pymessage, "r_pra", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // r_spa
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->r_spa);
    {
      int rc = PyObject_SetAttrString(_pymessage, "r_spa", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // r_fra
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->r_fra);
    {
      int rc = PyObject_SetAttrString(_pymessage, "r_fra", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
