# generated from rosidl_generator_py/resource/_idl.py.em
# with input from project_interfaces:srv/GetObjectInfo.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_GetObjectInfo_Request(type):
    """Metaclass of message 'GetObjectInfo_Request'."""

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
                'project_interfaces.srv.GetObjectInfo_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_object_info__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_object_info__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_object_info__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_object_info__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_object_info__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetObjectInfo_Request(metaclass=Metaclass_GetObjectInfo_Request):
    """Message class 'GetObjectInfo_Request'."""

    __slots__ = [
        '_object_name',
    ]

    _fields_and_field_types = {
        'object_name': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.object_name = kwargs.get('object_name', str())

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
        if self.object_name != other.object_name:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def object_name(self):
        """Message field 'object_name'."""
        return self._object_name

    @object_name.setter
    def object_name(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'object_name' field must be of type 'str'"
        self._object_name = value


# Import statements for member types

# Member 'orientations'
# Member 'grasp_widths'
import array  # noqa: E402, I100

# already imported above
# import builtins

import math  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_GetObjectInfo_Response(type):
    """Metaclass of message 'GetObjectInfo_Response'."""

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
                'project_interfaces.srv.GetObjectInfo_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_object_info__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_object_info__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_object_info__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_object_info__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_object_info__response

            from geometry_msgs.msg import Point
            if Point.__class__._TYPE_SUPPORT is None:
                Point.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetObjectInfo_Response(metaclass=Metaclass_GetObjectInfo_Response):
    """Message class 'GetObjectInfo_Response'."""

    __slots__ = [
        '_object_count',
        '_centers',
        '_orientations',
        '_grasp_widths',
    ]

    _fields_and_field_types = {
        'object_count': 'int32',
        'centers': 'sequence<geometry_msgs/Point>',
        'orientations': 'sequence<float>',
        'grasp_widths': 'sequence<float>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('float')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('float')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.object_count = kwargs.get('object_count', int())
        self.centers = kwargs.get('centers', [])
        self.orientations = array.array('f', kwargs.get('orientations', []))
        self.grasp_widths = array.array('f', kwargs.get('grasp_widths', []))

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
        if self.object_count != other.object_count:
            return False
        if self.centers != other.centers:
            return False
        if self.orientations != other.orientations:
            return False
        if self.grasp_widths != other.grasp_widths:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def object_count(self):
        """Message field 'object_count'."""
        return self._object_count

    @object_count.setter
    def object_count(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'object_count' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'object_count' field must be an integer in [-2147483648, 2147483647]"
        self._object_count = value

    @builtins.property
    def centers(self):
        """Message field 'centers'."""
        return self._centers

    @centers.setter
    def centers(self, value):
        if __debug__:
            from geometry_msgs.msg import Point
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, Point) for v in value) and
                 True), \
                "The 'centers' field must be a set or sequence and each value of type 'Point'"
        self._centers = value

    @builtins.property
    def orientations(self):
        """Message field 'orientations'."""
        return self._orientations

    @orientations.setter
    def orientations(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'f', \
                "The 'orientations' array.array() must have the type code of 'f'"
            self._orientations = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -3.402823466e+38 or val > 3.402823466e+38) or math.isinf(val) for val in value)), \
                "The 'orientations' field must be a set or sequence and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"
        self._orientations = array.array('f', value)

    @builtins.property
    def grasp_widths(self):
        """Message field 'grasp_widths'."""
        return self._grasp_widths

    @grasp_widths.setter
    def grasp_widths(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'f', \
                "The 'grasp_widths' array.array() must have the type code of 'f'"
            self._grasp_widths = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -3.402823466e+38 or val > 3.402823466e+38) or math.isinf(val) for val in value)), \
                "The 'grasp_widths' field must be a set or sequence and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"
        self._grasp_widths = array.array('f', value)


class Metaclass_GetObjectInfo(type):
    """Metaclass of service 'GetObjectInfo'."""

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
                'project_interfaces.srv.GetObjectInfo')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__get_object_info

            from project_interfaces.srv import _get_object_info
            if _get_object_info.Metaclass_GetObjectInfo_Request._TYPE_SUPPORT is None:
                _get_object_info.Metaclass_GetObjectInfo_Request.__import_type_support__()
            if _get_object_info.Metaclass_GetObjectInfo_Response._TYPE_SUPPORT is None:
                _get_object_info.Metaclass_GetObjectInfo_Response.__import_type_support__()


class GetObjectInfo(metaclass=Metaclass_GetObjectInfo):
    from project_interfaces.srv._get_object_info import GetObjectInfo_Request as Request
    from project_interfaces.srv._get_object_info import GetObjectInfo_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
