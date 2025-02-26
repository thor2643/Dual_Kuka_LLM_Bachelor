# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_set_moveit_coords_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED set_moveit_coords_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(set_moveit_coords_FOUND FALSE)
  elseif(NOT set_moveit_coords_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(set_moveit_coords_FOUND FALSE)
  endif()
  return()
endif()
set(_set_moveit_coords_CONFIG_INCLUDED TRUE)

# output package information
if(NOT set_moveit_coords_FIND_QUIETLY)
  message(STATUS "Found set_moveit_coords: 2.0.0 (${set_moveit_coords_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'set_moveit_coords' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${set_moveit_coords_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(set_moveit_coords_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${set_moveit_coords_DIR}/${_extra}")
endforeach()
