# generated from rosidl_generator_py/resource/_idl.py.em
# with input from robotiq_3f_gripper_ros2_interfaces:action/Robotiq3FGripperOutputGoal.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Robotiq3FGripperOutputGoal_Goal(type):
    """Metaclass of message 'Robotiq3FGripperOutputGoal_Goal'."""

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
                'robotiq_3f_gripper_ros2_interfaces.action.Robotiq3FGripperOutputGoal_Goal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__robotiq3_f_gripper_output_goal__goal
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__robotiq3_f_gripper_output_goal__goal
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__robotiq3_f_gripper_output_goal__goal
            cls._TYPE_SUPPORT = module.type_support_msg__action__robotiq3_f_gripper_output_goal__goal
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__robotiq3_f_gripper_output_goal__goal

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


class Robotiq3FGripperOutputGoal_Goal(metaclass=Metaclass_Robotiq3FGripperOutputGoal_Goal):
    """Message class 'Robotiq3FGripperOutputGoal_Goal'."""

    __slots__ = [
        '_output_registers_goal',
    ]

    _fields_and_field_types = {
        'output_registers_goal': 'robotiq_3f_gripper_ros2_interfaces/Robotiq3FGripperOutputRegisters',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['robotiq_3f_gripper_ros2_interfaces', 'msg'], 'Robotiq3FGripperOutputRegisters'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from robotiq_3f_gripper_ros2_interfaces.msg import Robotiq3FGripperOutputRegisters
        self.output_registers_goal = kwargs.get('output_registers_goal', Robotiq3FGripperOutputRegisters())

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
        if self.output_registers_goal != other.output_registers_goal:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def output_registers_goal(self):
        """Message field 'output_registers_goal'."""
        return self._output_registers_goal

    @output_registers_goal.setter
    def output_registers_goal(self, value):
        if __debug__:
            from robotiq_3f_gripper_ros2_interfaces.msg import Robotiq3FGripperOutputRegisters
            assert \
                isinstance(value, Robotiq3FGripperOutputRegisters), \
                "The 'output_registers_goal' field must be a sub message of type 'Robotiq3FGripperOutputRegisters'"
        self._output_registers_goal = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_Robotiq3FGripperOutputGoal_Result(type):
    """Metaclass of message 'Robotiq3FGripperOutputGoal_Result'."""

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
                'robotiq_3f_gripper_ros2_interfaces.action.Robotiq3FGripperOutputGoal_Result')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__robotiq3_f_gripper_output_goal__result
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__robotiq3_f_gripper_output_goal__result
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__robotiq3_f_gripper_output_goal__result
            cls._TYPE_SUPPORT = module.type_support_msg__action__robotiq3_f_gripper_output_goal__result
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__robotiq3_f_gripper_output_goal__result

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Robotiq3FGripperOutputGoal_Result(metaclass=Metaclass_Robotiq3FGripperOutputGoal_Result):
    """Message class 'Robotiq3FGripperOutputGoal_Result'."""

    __slots__ = [
        '_result',
    ]

    _fields_and_field_types = {
        'result': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.result = kwargs.get('result', str())

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
        if self.result != other.result:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def result(self):
        """Message field 'result'."""
        return self._result

    @result.setter
    def result(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'result' field must be of type 'str'"
        self._result = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_Robotiq3FGripperOutputGoal_Feedback(type):
    """Metaclass of message 'Robotiq3FGripperOutputGoal_Feedback'."""

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
                'robotiq_3f_gripper_ros2_interfaces.action.Robotiq3FGripperOutputGoal_Feedback')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__robotiq3_f_gripper_output_goal__feedback
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__robotiq3_f_gripper_output_goal__feedback
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__robotiq3_f_gripper_output_goal__feedback
            cls._TYPE_SUPPORT = module.type_support_msg__action__robotiq3_f_gripper_output_goal__feedback
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__robotiq3_f_gripper_output_goal__feedback

            from robotiq_3f_gripper_ros2_interfaces.msg import Robotiq3FGripperInputRegisters
            if Robotiq3FGripperInputRegisters.__class__._TYPE_SUPPORT is None:
                Robotiq3FGripperInputRegisters.__class__.__import_type_support__()

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


class Robotiq3FGripperOutputGoal_Feedback(metaclass=Metaclass_Robotiq3FGripperOutputGoal_Feedback):
    """Message class 'Robotiq3FGripperOutputGoal_Feedback'."""

    __slots__ = [
        '_input_registers',
        '_output_registers',
    ]

    _fields_and_field_types = {
        'input_registers': 'robotiq_3f_gripper_ros2_interfaces/Robotiq3FGripperInputRegisters',
        'output_registers': 'robotiq_3f_gripper_ros2_interfaces/Robotiq3FGripperOutputRegisters',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['robotiq_3f_gripper_ros2_interfaces', 'msg'], 'Robotiq3FGripperInputRegisters'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['robotiq_3f_gripper_ros2_interfaces', 'msg'], 'Robotiq3FGripperOutputRegisters'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from robotiq_3f_gripper_ros2_interfaces.msg import Robotiq3FGripperInputRegisters
        self.input_registers = kwargs.get('input_registers', Robotiq3FGripperInputRegisters())
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
        if self.input_registers != other.input_registers:
            return False
        if self.output_registers != other.output_registers:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def input_registers(self):
        """Message field 'input_registers'."""
        return self._input_registers

    @input_registers.setter
    def input_registers(self, value):
        if __debug__:
            from robotiq_3f_gripper_ros2_interfaces.msg import Robotiq3FGripperInputRegisters
            assert \
                isinstance(value, Robotiq3FGripperInputRegisters), \
                "The 'input_registers' field must be a sub message of type 'Robotiq3FGripperInputRegisters'"
        self._input_registers = value

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


class Metaclass_Robotiq3FGripperOutputGoal_SendGoal_Request(type):
    """Metaclass of message 'Robotiq3FGripperOutputGoal_SendGoal_Request'."""

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
                'robotiq_3f_gripper_ros2_interfaces.action.Robotiq3FGripperOutputGoal_SendGoal_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__robotiq3_f_gripper_output_goal__send_goal__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__robotiq3_f_gripper_output_goal__send_goal__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__robotiq3_f_gripper_output_goal__send_goal__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__robotiq3_f_gripper_output_goal__send_goal__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__robotiq3_f_gripper_output_goal__send_goal__request

            from robotiq_3f_gripper_ros2_interfaces.action import Robotiq3FGripperOutputGoal
            if Robotiq3FGripperOutputGoal.Goal.__class__._TYPE_SUPPORT is None:
                Robotiq3FGripperOutputGoal.Goal.__class__.__import_type_support__()

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Robotiq3FGripperOutputGoal_SendGoal_Request(metaclass=Metaclass_Robotiq3FGripperOutputGoal_SendGoal_Request):
    """Message class 'Robotiq3FGripperOutputGoal_SendGoal_Request'."""

    __slots__ = [
        '_goal_id',
        '_goal',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'goal': 'robotiq_3f_gripper_ros2_interfaces/Robotiq3FGripperOutputGoal_Goal',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['robotiq_3f_gripper_ros2_interfaces', 'action'], 'Robotiq3FGripperOutputGoal_Goal'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_Goal
        self.goal = kwargs.get('goal', Robotiq3FGripperOutputGoal_Goal())

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
        if self.goal_id != other.goal_id:
            return False
        if self.goal != other.goal:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if __debug__:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value

    @builtins.property
    def goal(self):
        """Message field 'goal'."""
        return self._goal

    @goal.setter
    def goal(self, value):
        if __debug__:
            from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_Goal
            assert \
                isinstance(value, Robotiq3FGripperOutputGoal_Goal), \
                "The 'goal' field must be a sub message of type 'Robotiq3FGripperOutputGoal_Goal'"
        self._goal = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_Robotiq3FGripperOutputGoal_SendGoal_Response(type):
    """Metaclass of message 'Robotiq3FGripperOutputGoal_SendGoal_Response'."""

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
                'robotiq_3f_gripper_ros2_interfaces.action.Robotiq3FGripperOutputGoal_SendGoal_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__robotiq3_f_gripper_output_goal__send_goal__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__robotiq3_f_gripper_output_goal__send_goal__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__robotiq3_f_gripper_output_goal__send_goal__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__robotiq3_f_gripper_output_goal__send_goal__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__robotiq3_f_gripper_output_goal__send_goal__response

            from builtin_interfaces.msg import Time
            if Time.__class__._TYPE_SUPPORT is None:
                Time.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Robotiq3FGripperOutputGoal_SendGoal_Response(metaclass=Metaclass_Robotiq3FGripperOutputGoal_SendGoal_Response):
    """Message class 'Robotiq3FGripperOutputGoal_SendGoal_Response'."""

    __slots__ = [
        '_accepted',
        '_stamp',
    ]

    _fields_and_field_types = {
        'accepted': 'boolean',
        'stamp': 'builtin_interfaces/Time',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.accepted = kwargs.get('accepted', bool())
        from builtin_interfaces.msg import Time
        self.stamp = kwargs.get('stamp', Time())

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
        if self.accepted != other.accepted:
            return False
        if self.stamp != other.stamp:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def accepted(self):
        """Message field 'accepted'."""
        return self._accepted

    @accepted.setter
    def accepted(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'accepted' field must be of type 'bool'"
        self._accepted = value

    @builtins.property
    def stamp(self):
        """Message field 'stamp'."""
        return self._stamp

    @stamp.setter
    def stamp(self, value):
        if __debug__:
            from builtin_interfaces.msg import Time
            assert \
                isinstance(value, Time), \
                "The 'stamp' field must be a sub message of type 'Time'"
        self._stamp = value


class Metaclass_Robotiq3FGripperOutputGoal_SendGoal(type):
    """Metaclass of service 'Robotiq3FGripperOutputGoal_SendGoal'."""

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
                'robotiq_3f_gripper_ros2_interfaces.action.Robotiq3FGripperOutputGoal_SendGoal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__robotiq3_f_gripper_output_goal__send_goal

            from robotiq_3f_gripper_ros2_interfaces.action import _robotiq3_f_gripper_output_goal
            if _robotiq3_f_gripper_output_goal.Metaclass_Robotiq3FGripperOutputGoal_SendGoal_Request._TYPE_SUPPORT is None:
                _robotiq3_f_gripper_output_goal.Metaclass_Robotiq3FGripperOutputGoal_SendGoal_Request.__import_type_support__()
            if _robotiq3_f_gripper_output_goal.Metaclass_Robotiq3FGripperOutputGoal_SendGoal_Response._TYPE_SUPPORT is None:
                _robotiq3_f_gripper_output_goal.Metaclass_Robotiq3FGripperOutputGoal_SendGoal_Response.__import_type_support__()


class Robotiq3FGripperOutputGoal_SendGoal(metaclass=Metaclass_Robotiq3FGripperOutputGoal_SendGoal):
    from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_SendGoal_Request as Request
    from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_SendGoal_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_Robotiq3FGripperOutputGoal_GetResult_Request(type):
    """Metaclass of message 'Robotiq3FGripperOutputGoal_GetResult_Request'."""

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
                'robotiq_3f_gripper_ros2_interfaces.action.Robotiq3FGripperOutputGoal_GetResult_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__robotiq3_f_gripper_output_goal__get_result__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__robotiq3_f_gripper_output_goal__get_result__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__robotiq3_f_gripper_output_goal__get_result__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__robotiq3_f_gripper_output_goal__get_result__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__robotiq3_f_gripper_output_goal__get_result__request

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Robotiq3FGripperOutputGoal_GetResult_Request(metaclass=Metaclass_Robotiq3FGripperOutputGoal_GetResult_Request):
    """Message class 'Robotiq3FGripperOutputGoal_GetResult_Request'."""

    __slots__ = [
        '_goal_id',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())

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
        if self.goal_id != other.goal_id:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if __debug__:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_Robotiq3FGripperOutputGoal_GetResult_Response(type):
    """Metaclass of message 'Robotiq3FGripperOutputGoal_GetResult_Response'."""

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
                'robotiq_3f_gripper_ros2_interfaces.action.Robotiq3FGripperOutputGoal_GetResult_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__robotiq3_f_gripper_output_goal__get_result__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__robotiq3_f_gripper_output_goal__get_result__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__robotiq3_f_gripper_output_goal__get_result__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__robotiq3_f_gripper_output_goal__get_result__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__robotiq3_f_gripper_output_goal__get_result__response

            from robotiq_3f_gripper_ros2_interfaces.action import Robotiq3FGripperOutputGoal
            if Robotiq3FGripperOutputGoal.Result.__class__._TYPE_SUPPORT is None:
                Robotiq3FGripperOutputGoal.Result.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Robotiq3FGripperOutputGoal_GetResult_Response(metaclass=Metaclass_Robotiq3FGripperOutputGoal_GetResult_Response):
    """Message class 'Robotiq3FGripperOutputGoal_GetResult_Response'."""

    __slots__ = [
        '_status',
        '_result',
    ]

    _fields_and_field_types = {
        'status': 'int8',
        'result': 'robotiq_3f_gripper_ros2_interfaces/Robotiq3FGripperOutputGoal_Result',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['robotiq_3f_gripper_ros2_interfaces', 'action'], 'Robotiq3FGripperOutputGoal_Result'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.status = kwargs.get('status', int())
        from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_Result
        self.result = kwargs.get('result', Robotiq3FGripperOutputGoal_Result())

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
        if self.status != other.status:
            return False
        if self.result != other.result:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def status(self):
        """Message field 'status'."""
        return self._status

    @status.setter
    def status(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'status' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'status' field must be an integer in [-128, 127]"
        self._status = value

    @builtins.property
    def result(self):
        """Message field 'result'."""
        return self._result

    @result.setter
    def result(self, value):
        if __debug__:
            from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_Result
            assert \
                isinstance(value, Robotiq3FGripperOutputGoal_Result), \
                "The 'result' field must be a sub message of type 'Robotiq3FGripperOutputGoal_Result'"
        self._result = value


class Metaclass_Robotiq3FGripperOutputGoal_GetResult(type):
    """Metaclass of service 'Robotiq3FGripperOutputGoal_GetResult'."""

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
                'robotiq_3f_gripper_ros2_interfaces.action.Robotiq3FGripperOutputGoal_GetResult')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__robotiq3_f_gripper_output_goal__get_result

            from robotiq_3f_gripper_ros2_interfaces.action import _robotiq3_f_gripper_output_goal
            if _robotiq3_f_gripper_output_goal.Metaclass_Robotiq3FGripperOutputGoal_GetResult_Request._TYPE_SUPPORT is None:
                _robotiq3_f_gripper_output_goal.Metaclass_Robotiq3FGripperOutputGoal_GetResult_Request.__import_type_support__()
            if _robotiq3_f_gripper_output_goal.Metaclass_Robotiq3FGripperOutputGoal_GetResult_Response._TYPE_SUPPORT is None:
                _robotiq3_f_gripper_output_goal.Metaclass_Robotiq3FGripperOutputGoal_GetResult_Response.__import_type_support__()


class Robotiq3FGripperOutputGoal_GetResult(metaclass=Metaclass_Robotiq3FGripperOutputGoal_GetResult):
    from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_GetResult_Request as Request
    from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_GetResult_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_Robotiq3FGripperOutputGoal_FeedbackMessage(type):
    """Metaclass of message 'Robotiq3FGripperOutputGoal_FeedbackMessage'."""

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
                'robotiq_3f_gripper_ros2_interfaces.action.Robotiq3FGripperOutputGoal_FeedbackMessage')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__robotiq3_f_gripper_output_goal__feedback_message
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__robotiq3_f_gripper_output_goal__feedback_message
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__robotiq3_f_gripper_output_goal__feedback_message
            cls._TYPE_SUPPORT = module.type_support_msg__action__robotiq3_f_gripper_output_goal__feedback_message
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__robotiq3_f_gripper_output_goal__feedback_message

            from robotiq_3f_gripper_ros2_interfaces.action import Robotiq3FGripperOutputGoal
            if Robotiq3FGripperOutputGoal.Feedback.__class__._TYPE_SUPPORT is None:
                Robotiq3FGripperOutputGoal.Feedback.__class__.__import_type_support__()

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Robotiq3FGripperOutputGoal_FeedbackMessage(metaclass=Metaclass_Robotiq3FGripperOutputGoal_FeedbackMessage):
    """Message class 'Robotiq3FGripperOutputGoal_FeedbackMessage'."""

    __slots__ = [
        '_goal_id',
        '_feedback',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'feedback': 'robotiq_3f_gripper_ros2_interfaces/Robotiq3FGripperOutputGoal_Feedback',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['robotiq_3f_gripper_ros2_interfaces', 'action'], 'Robotiq3FGripperOutputGoal_Feedback'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_Feedback
        self.feedback = kwargs.get('feedback', Robotiq3FGripperOutputGoal_Feedback())

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
        if self.goal_id != other.goal_id:
            return False
        if self.feedback != other.feedback:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if __debug__:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value

    @builtins.property
    def feedback(self):
        """Message field 'feedback'."""
        return self._feedback

    @feedback.setter
    def feedback(self, value):
        if __debug__:
            from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_Feedback
            assert \
                isinstance(value, Robotiq3FGripperOutputGoal_Feedback), \
                "The 'feedback' field must be a sub message of type 'Robotiq3FGripperOutputGoal_Feedback'"
        self._feedback = value


class Metaclass_Robotiq3FGripperOutputGoal(type):
    """Metaclass of action 'Robotiq3FGripperOutputGoal'."""

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
                'robotiq_3f_gripper_ros2_interfaces.action.Robotiq3FGripperOutputGoal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_action__action__robotiq3_f_gripper_output_goal

            from action_msgs.msg import _goal_status_array
            if _goal_status_array.Metaclass_GoalStatusArray._TYPE_SUPPORT is None:
                _goal_status_array.Metaclass_GoalStatusArray.__import_type_support__()
            from action_msgs.srv import _cancel_goal
            if _cancel_goal.Metaclass_CancelGoal._TYPE_SUPPORT is None:
                _cancel_goal.Metaclass_CancelGoal.__import_type_support__()

            from robotiq_3f_gripper_ros2_interfaces.action import _robotiq3_f_gripper_output_goal
            if _robotiq3_f_gripper_output_goal.Metaclass_Robotiq3FGripperOutputGoal_SendGoal._TYPE_SUPPORT is None:
                _robotiq3_f_gripper_output_goal.Metaclass_Robotiq3FGripperOutputGoal_SendGoal.__import_type_support__()
            if _robotiq3_f_gripper_output_goal.Metaclass_Robotiq3FGripperOutputGoal_GetResult._TYPE_SUPPORT is None:
                _robotiq3_f_gripper_output_goal.Metaclass_Robotiq3FGripperOutputGoal_GetResult.__import_type_support__()
            if _robotiq3_f_gripper_output_goal.Metaclass_Robotiq3FGripperOutputGoal_FeedbackMessage._TYPE_SUPPORT is None:
                _robotiq3_f_gripper_output_goal.Metaclass_Robotiq3FGripperOutputGoal_FeedbackMessage.__import_type_support__()


class Robotiq3FGripperOutputGoal(metaclass=Metaclass_Robotiq3FGripperOutputGoal):

    # The goal message defined in the action definition.
    from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_Goal as Goal
    # The result message defined in the action definition.
    from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_Result as Result
    # The feedback message defined in the action definition.
    from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_Feedback as Feedback

    class Impl:

        # The send_goal service using a wrapped version of the goal message as a request.
        from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_SendGoal as SendGoalService
        # The get_result service using a wrapped version of the result message as a response.
        from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_GetResult as GetResultService
        # The feedback message with generic fields which wraps the feedback message.
        from robotiq_3f_gripper_ros2_interfaces.action._robotiq3_f_gripper_output_goal import Robotiq3FGripperOutputGoal_FeedbackMessage as FeedbackMessage

        # The generic service to cancel a goal.
        from action_msgs.srv._cancel_goal import CancelGoal as CancelGoalService
        # The generic message for get the status of a goal.
        from action_msgs.msg._goal_status_array import GoalStatusArray as GoalStatusMessage

    def __init__(self):
        raise NotImplementedError('Action classes can not be instantiated')
