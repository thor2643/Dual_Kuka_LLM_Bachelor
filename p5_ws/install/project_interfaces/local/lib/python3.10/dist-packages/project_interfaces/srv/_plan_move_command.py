# generated from rosidl_generator_py/resource/_idl.py.em
# with input from project_interfaces:srv/PlanMoveCommand.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_PlanMoveCommand_Request(type):
    """Metaclass of message 'PlanMoveCommand_Request'."""

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
            module = import_type_support('project_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'project_interfaces.srv.PlanMoveCommand_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__plan_move_command__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__plan_move_command__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__plan_move_command__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__plan_move_command__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__plan_move_command__request

            from geometry_msgs.msg import Point
            if Point.__class__._TYPE_SUPPORT is None:
                Point.__class__.__import_type_support__()

            from geometry_msgs.msg import Quaternion
            if Quaternion.__class__._TYPE_SUPPORT is None:
                Quaternion.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PlanMoveCommand_Request(metaclass=Metaclass_PlanMoveCommand_Request):
    """Message class 'PlanMoveCommand_Request'."""

    __slots__ = [
        '_arm',
        '_position',
        '_orientation',
    ]

    _fields_and_field_types = {
        'arm': 'string',
        'position': 'geometry_msgs/Point',
        'orientation': 'geometry_msgs/Quaternion',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Quaternion'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.arm = kwargs.get('arm', str())
        from geometry_msgs.msg import Point
        self.position = kwargs.get('position', Point())
        from geometry_msgs.msg import Quaternion
        self.orientation = kwargs.get('orientation', Quaternion())

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
        if self.arm != other.arm:
            return False
        if self.position != other.position:
            return False
        if self.orientation != other.orientation:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def arm(self):
        """Message field 'arm'."""
        return self._arm

    @arm.setter
    def arm(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'arm' field must be of type 'str'"
        self._arm = value

    @builtins.property
    def position(self):
        """Message field 'position'."""
        return self._position

    @position.setter
    def position(self, value):
        if __debug__:
            from geometry_msgs.msg import Point
            assert \
                isinstance(value, Point), \
                "The 'position' field must be a sub message of type 'Point'"
        self._position = value

    @builtins.property
    def orientation(self):
        """Message field 'orientation'."""
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        if __debug__:
            from geometry_msgs.msg import Quaternion
            assert \
                isinstance(value, Quaternion), \
                "The 'orientation' field must be a sub message of type 'Quaternion'"
        self._orientation = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_PlanMoveCommand_Response(type):
    """Metaclass of message 'PlanMoveCommand_Response'."""

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
            module = import_type_support('project_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'project_interfaces.srv.PlanMoveCommand_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__plan_move_command__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__plan_move_command__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__plan_move_command__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__plan_move_command__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__plan_move_command__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PlanMoveCommand_Response(metaclass=Metaclass_PlanMoveCommand_Response):
    """Message class 'PlanMoveCommand_Response'."""

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


class Metaclass_PlanMoveCommand(type):
    """Metaclass of service 'PlanMoveCommand'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('project_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'project_interfaces.srv.PlanMoveCommand')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__plan_move_command

            from project_interfaces.srv import _plan_move_command
            if _plan_move_command.Metaclass_PlanMoveCommand_Request._TYPE_SUPPORT is None:
                _plan_move_command.Metaclass_PlanMoveCommand_Request.__import_type_support__()
            if _plan_move_command.Metaclass_PlanMoveCommand_Response._TYPE_SUPPORT is None:
                _plan_move_command.Metaclass_PlanMoveCommand_Response.__import_type_support__()


class PlanMoveCommand(metaclass=Metaclass_PlanMoveCommand):
    from project_interfaces.srv._plan_move_command import PlanMoveCommand_Request as Request
    from project_interfaces.srv._plan_move_command import PlanMoveCommand_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
