// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from robotiq_3f_gripper_ros2_interfaces:msg/Robotiq3FGripperInputRegisters.idl
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
#include "robotiq_3f_gripper_ros2_interfaces/msg/detail/robotiq3_f_gripper_input_registers__struct.h"
#include "robotiq_3f_gripper_ros2_interfaces/msg/detail/robotiq3_f_gripper_input_registers__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool robotiq_3f_gripper_ros2_interfaces__msg__robotiq3_f_gripper_input_registers__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[106];
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
    assert(strncmp("robotiq_3f_gripper_ros2_interfaces.msg._robotiq3_f_gripper_input_registers.Robotiq3FGripperInputRegisters", full_classname_dest, 105) == 0);
  }
  robotiq_3f_gripper_ros2_interfaces__msg__Robotiq3FGripperInputRegisters * ros_message = _ros_message;
  {  // g_act
    PyObject * field = PyObject_GetAttrString(_pymsg, "g_act");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->g_act = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // g_mod
    PyObject * field = PyObject_GetAttrString(_pymsg, "g_mod");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->g_mod = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // g_gto
    PyObject * field = PyObject_GetAttrString(_pymsg, "g_gto");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->g_gto = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // g_imc
    PyObject * field = PyObject_GetAttrString(_pymsg, "g_imc");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->g_imc = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // g_sta
    PyObject * field = PyObject_GetAttrString(_pymsg, "g_sta");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->g_sta = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // g_flt
    PyObject * field = PyObject_GetAttrString(_pymsg, "g_flt");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->g_flt = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // g_pra
    PyObject * field = PyObject_GetAttrString(_pymsg, "g_pra");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->g_pra = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * robotiq_3f_gripper_ros2_interfaces__msg__robotiq3_f_gripper_input_registers__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of Robotiq3FGripperInputRegisters */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("robotiq_3f_gripper_ros2_interfaces.msg._robotiq3_f_gripper_input_registers");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "Robotiq3FGripperInputRegisters");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  robotiq_3f_gripper_ros2_interfaces__msg__Robotiq3FGripperInputRegisters * ros_message = (robotiq_3f_gripper_ros2_interfaces__msg__Robotiq3FGripperInputRegisters *)raw_ros_message;
  {  // g_act
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->g_act);
    {
      int rc = PyObject_SetAttrString(_pymessage, "g_act", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // g_mod
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->g_mod);
    {
      int rc = PyObject_SetAttrString(_pymessage, "g_mod", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // g_gto
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->g_gto);
    {
      int rc = PyObject_SetAttrString(_pymessage, "g_gto", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // g_imc
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->g_imc);
    {
      int rc = PyObject_SetAttrString(_pymessage, "g_imc", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // g_sta
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->g_sta);
    {
      int rc = PyObject_SetAttrString(_pymessage, "g_sta", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // g_flt
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->g_flt);
    {
      int rc = PyObject_SetAttrString(_pymessage, "g_flt", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // g_pra
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->g_pra);
    {
      int rc = PyObject_SetAttrString(_pymessage, "g_pra", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
