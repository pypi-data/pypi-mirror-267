# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

#[=======================================================================[.rst:
UsePkgConfig
------------

Obsolete pkg-config module for CMake, use FindPkgConfig instead.



This module defines the following macro:

PKGCONFIG(package includedir libdir linkflags cflags)

Calling PKGCONFIG will fill the desired information into the 4 given
arguments, e.g.  PKGCONFIG(libart-2.0 LIBART_INCLUDE_DIR
LIBART_LINK_DIR LIBART_LINK_FLAGS LIBART_CFLAGS) if pkg-config was NOT
found or the specified software package doesn't exist, the variable
will be empty when the function returns, otherwise they will contain
the respective information
#]=======================================================================]

find_program(PKGCONFIG_EXECUTABLE NAMES pkg-config )

macro(PKGCONFIG _package _include_DIR _link_DIR _link_FLAGS _cflags)
  message(STATUS
    "WARNING: you are using the obsolete 'PKGCONFIG' macro, use FindPkgConfig")
# reset the variables at the beginning
  set(${_include_DIR})
  set(${_link_DIR})
  set(${_link_FLAGS})
  set(${_cflags})

  # if pkg-config has been found
  if(PKGCONFIG_EXECUTABLE)

    execute_process(COMMAND ${PKGCONFIG_EXECUTABLE} ${_package} --exists RESULT_VARIABLE _return_VALUE OUTPUT_VARIABLE _pkgconfigDevNull )

    # and if the package of interest also exists for pkg-config, then get the information
    if(NOT _return_VALUE)

      execute_process(COMMAND ${PKGCONFIG_EXECUTABLE} ${_package} --variable=includedir
        OUTPUT_VARIABLE ${_include_DIR} OUTPUT_STRIP_TRAILING_WHITESPACE )
      string(REGEX REPLACE "[\r\n]" " " ${_include_DIR} "${${_include_DIR}}")

      execute_process(COMMAND ${PKGCONFIG_EXECUTABLE} ${_package} --variable=libdir
        OUTPUT_VARIABLE ${_link_DIR} OUTPUT_STRIP_TRAILING_WHITESPACE )
      string(REGEX REPLACE "[\r\n]" " " ${_link_DIR} "${${_link_DIR}}")

      execute_process(COMMAND ${PKGCONFIG_EXECUTABLE} ${_package} --libs
        OUTPUT_VARIABLE ${_link_FLAGS} OUTPUT_STRIP_TRAILING_WHITESPACE )
      string(REGEX REPLACE "[\r\n]" " " ${_link_FLAGS} "${${_link_FLAGS}}")

      execute_process(COMMAND ${PKGCONFIG_EXECUTABLE} ${_package} --cflags
        OUTPUT_VARIABLE ${_cflags} OUTPUT_STRIP_TRAILING_WHITESPACE )
      string(REGEX REPLACE "[\r\n]" " " ${_cflags} "${${_cflags}}")

    else()

      message(STATUS "PKGCONFIG() indicates that ${_package} is not installed (install the package which contains ${_package}.pc if you want to support this feature)")

    endif()

  # if pkg-config has NOT been found, INFORM the user
  else()

    message(STATUS "WARNING: PKGCONFIG() indicates that the tool pkg-config has not been found on your system. You should install it.")

  endif()

endmacro()

mark_as_advanced(PKGCONFIG_EXECUTABLE)
