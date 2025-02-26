# generated from rosidl_generator_py/resource/_idl.py.em
# with input from robotiq_3f_gripper_ros2_interfaces:srv/Robotiq3FGripperOutputService.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Robotiq3FGripperOutputService_Request(type):
    """Metaclass of message 'Robotiq3FGripperOutputService_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('robotiq_3f_gripper_ros2_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'robotiq_3f_gripper_ros2_interfaces.srv.Robotiq3FGripperOutputService_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__robotiq3_f_gripper_output_service__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__robotiq3_f_gripper_output_service__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__robotiq3_f_gripper_output_service__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__robotiq3_f_gripper_output_service__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__robotiq3_f_gripper_output_service__request

            from robotiq_3f_gripper_ros2_interfaces.msg import Robotiq3FGripperOutputRegisters
            if Robotiq3FGripperOutputRegisters.__class__._TYPE_SUPPORT is None:
                Robotiq3FGripperOutputRegisters.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Robotiq3FGripperOutputService_Request(metaclass=Metaclass_Robotiq3FGripperOutputService_Request):
    """Message class 'Robotiq3FGripperOutputService_Request'."""

    __slots__ = [
        '_output_registers',
    ]

    _fields_and_field_types = {
        'output_registers': 'robotiq_3f_gripper_ros2_interfaces/Robotiq3FGripperOutputRegisters',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['robotiq_3f_gripper_ros2_interfaces', 'msg'], 'Robotiq3FGripperOutputRegisters'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from robotiq_3f_gripper_ros2_interfaces.msg import Robotiq3FGripperOutputRegisters
        self.output_registers = kwargs.get('output_registers', Robotiq3FGripperOutputRegisters())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.output_registers != other.output_registers:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def output_registers(self):
        """Message field 'output_registers'."""
        return self._output_registers

    @output_registers.setter
    def output_registers(self, value):
        if __debug__:
            from robotiq_3f_gripper_ros2_interfaces.msg import Robotiq3FGripperOutputRegisters
            assert \
                isinstance(value, Robotiq3FGripperOutputRegisters), \
                "The 'output_registers' field must be a sub message of type 'Robotiq3FGripperOutputRegisters'"
        self._output_registers = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_Robotiq3FGripperOutputService_Response(type):
    """Metaclass of message 'Robotiq3FGripperOutputService_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('robotiq_3f_gripper_ros2_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'robotiq_3f_gripper_ros2_interfaces.srv.Robotiq3FGripperOutputService_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__robotiq3_f_gripper_output_service__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__robotiq3_f_gripper_output_service__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__robotiq3_f_gripper_output_service__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__robotiq3_f_gripper_output_service__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__robotiq3_f_gripper_output_service__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Robotiq3FGripperOutputService_Response(metaclass=Metaclass_Robotiq3FGripperOutputService_Response):
    """Message class 'Robotiq3FGripperOutputService_Response'."""

    __slots__ = [
        '_success',
        '_log',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'log': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.log = kwargs.get('log', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.success != other.success:
            return False
        if self.log != other.log:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def success(self):
        """Message field 'success'."""
        return self._success

    @success.setter
    def success(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'success' field must be of type 'bool'"
        self._success = value

    @builtins.property
    def log(self):
        """Message field 'log'."""
        return self._log

    @log.setter
    def log(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'log' field must be of type 'str'"
        self._log = value


class Metaclass_Robotiq3FGripperOutputService(type):
    """Metaclass of service 'Robotiq3FGripperOutputService'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('robotiq_3f_gripper_ros2_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'robotiq_3f_gripper_ros2_interfaces.srv.Robotiq3FGripperOutputService')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__robotiq3_f_gripper_output_service

            from robotiq_3f_gripper_ros2_interfaces.srv import _robotiq3_f_gripper_output_service
            if _robotiq3_f_gripper_output_service.Metaclass_Robotiq3FGripperOutputService_Request._TYPE_SUPPORT is None:
                _robotiq3_f_gripper_output_service.Metaclass_Robotiq3FGripperOutputService_Request.__import_type_support__()
            if _robotiq3_f_gripper_output_service.Metaclass_Robotiq3FGripperOutputService_Response._TYPE_SUPPORT is None:
                _robotiq3_f_gripper_output_service.Metaclass_Robotiq3FGripperOutputService_Response.__import_type_support__()


class Robotiq3FGripperOutputService(metaclass=Metaclass_Robotiq3FGripperOutputService):
    from robotiq_3f_gripper_ros2_interfaces.srv._robotiq3_f_gripper_output_service import Robotiq3FGripperOutputService_Request as Request
    from robotiq_3f_gripper_ros2_interfaces.srv._robotiq3_f_gripper_output_service import Robotiq3FGripperOutputService_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
