# generated from rosidl_generator_py/resource/_idl.py.em
# with input from robotiq_3f_gripper_ros2_interfaces:msg/Robotiq3FGripperOutputRegisters.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Robotiq3FGripperOutputRegisters(type):
    """Metaclass of message 'Robotiq3FGripperOutputRegisters'."""

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
                'robotiq_3f_gripper_ros2_interfaces.msg.Robotiq3FGripperOutputRegisters')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__robotiq3_f_gripper_output_registers
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__robotiq3_f_gripper_output_registers
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__robotiq3_f_gripper_output_registers
            cls._TYPE_SUPPORT = module.type_support_msg__msg__robotiq3_f_gripper_output_registers
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__robotiq3_f_gripper_output_registers

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Robotiq3FGripperOutputRegisters(metaclass=Metaclass_Robotiq3FGripperOutputRegisters):
    """Message class 'Robotiq3FGripperOutputRegisters'."""

    __slots__ = [
        '_r_act',
        '_r_mod',
        '_r_gto',
        '_r_atr',
        '_r_pra',
        '_r_spa',
        '_r_fra',
    ]

    _fields_and_field_types = {
        'r_act': 'uint8',
        'r_mod': 'uint8',
        'r_gto': 'uint8',
        'r_atr': 'uint8',
        'r_pra': 'uint8',
        'r_spa': 'uint8',
        'r_fra': 'uint8',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.r_act = kwargs.get('r_act', int())
        self.r_mod = kwargs.get('r_mod', int())
        self.r_gto = kwargs.get('r_gto', int())
        self.r_atr = kwargs.get('r_atr', int())
        self.r_pra = kwargs.get('r_pra', int())
        self.r_spa = kwargs.get('r_spa', int())
        self.r_fra = kwargs.get('r_fra', int())

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
        if self.r_act != other.r_act:
            return False
        if self.r_mod != other.r_mod:
            return False
        if self.r_gto != other.r_gto:
            return False
        if self.r_atr != other.r_atr:
            return False
        if self.r_pra != other.r_pra:
            return False
        if self.r_spa != other.r_spa:
            return False
        if self.r_fra != other.r_fra:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def r_act(self):
        """Message field 'r_act'."""
        return self._r_act

    @r_act.setter
    def r_act(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'r_act' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'r_act' field must be an unsigned integer in [0, 255]"
        self._r_act = value

    @builtins.property
    def r_mod(self):
        """Message field 'r_mod'."""
        return self._r_mod

    @r_mod.setter
    def r_mod(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'r_mod' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'r_mod' field must be an unsigned integer in [0, 255]"
        self._r_mod = value

    @builtins.property
    def r_gto(self):
        """Message field 'r_gto'."""
        return self._r_gto

    @r_gto.setter
    def r_gto(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'r_gto' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'r_gto' field must be an unsigned integer in [0, 255]"
        self._r_gto = value

    @builtins.property
    def r_atr(self):
        """Message field 'r_atr'."""
        return self._r_atr

    @r_atr.setter
    def r_atr(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'r_atr' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'r_atr' field must be an unsigned integer in [0, 255]"
        self._r_atr = value

    @builtins.property
    def r_pra(self):
        """Message field 'r_pra'."""
        return self._r_pra

    @r_pra.setter
    def r_pra(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'r_pra' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'r_pra' field must be an unsigned integer in [0, 255]"
        self._r_pra = value

    @builtins.property
    def r_spa(self):
        """Message field 'r_spa'."""
        return self._r_spa

    @r_spa.setter
    def r_spa(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'r_spa' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'r_spa' field must be an unsigned integer in [0, 255]"
        self._r_spa = value

    @builtins.property
    def r_fra(self):
        """Message field 'r_fra'."""
        return self._r_fra

    @r_fra.setter
    def r_fra(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'r_fra' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'r_fra' field must be an unsigned integer in [0, 255]"
        self._r_fra = value
