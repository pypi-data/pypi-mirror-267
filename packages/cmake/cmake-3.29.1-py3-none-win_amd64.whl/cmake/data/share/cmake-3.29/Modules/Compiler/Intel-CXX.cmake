include(Compiler/Intel)
__compiler_intel(CXX)

string(APPEND CMAKE_CXX_FLAGS_MINSIZEREL_INIT " -DNDEBUG")
string(APPEND CMAKE_CXX_FLAGS_RELEASE_INIT " -DNDEBUG")
string(APPEND CMAKE_CXX_FLAGS_RELWITHDEBINFO_INIT " -DNDEBUG")

set(CMAKE_DEPFILE_FLAGS_CXX "-MD -MT <DEP_TARGET> -MF <DEP_FILE>")
if((NOT DEFINED CMAKE_DEPENDS_USE_COMPILER OR CMAKE_DEPENDS_USE_COMPILER)
    AND CMAKE_GENERATOR MATCHES "Makefiles|WMake")
  # dependencies are computed by the compiler itself
  set(CMAKE_CXX_DEPFILE_FORMAT gcc)
  set(CMAKE_CXX_DEPENDS_USE_COMPILER TRUE)
endif()

if("x${CMAKE_CXX_SIMULATE_ID}" STREQUAL "xMSVC")

  set(CMAKE_CXX_CLANG_TIDY_DRIVER_MODE "cl")
  set(CMAKE_CXX_INCLUDE_WHAT_YOU_USE_DRIVER_MODE "cl")

  if (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 19.0.0)
    set(CMAKE_CXX20_STANDARD_COMPILE_OPTION "-Qstd=c++20")
    set(CMAKE_CXX20_EXTENSION_COMPILE_OPTION "-Qstd=c++20")
  endif()

  if (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 18.0.0)
    set(CMAKE_CXX17_STANDARD_COMPILE_OPTION "-Qstd=c++17")
    set(CMAKE_CXX17_EXTENSION_COMPILE_OPTION "-Qstd=c++17")
  endif()

  if (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 16.0)
    set(CMAKE_CXX14_STANDARD_COMPILE_OPTION "-Qstd=c++14")
    set(CMAKE_CXX14_EXTENSION_COMPILE_OPTION "-Qstd=c++14")
  endif()

  if (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 13.0)
    set(CMAKE_CXX11_STANDARD_COMPILE_OPTION "-Qstd=c++11")
    set(CMAKE_CXX11_EXTENSION_COMPILE_OPTION "-Qstd=c++11")
  elseif (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 12.1)
    set(CMAKE_CXX11_STANDARD_COMPILE_OPTION "-Qstd=c++0x")
    set(CMAKE_CXX11_EXTENSION_COMPILE_OPTION "-Qstd=c++0x")
  endif()

  if (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 12.1)
    set(CMAKE_CXX98_STANDARD_COMPILE_OPTION "")
    set(CMAKE_CXX98_EXTENSION_COMPILE_OPTION "")
    set(CMAKE_CXX98_STANDARD__HAS_FULL_SUPPORT ON)
  endif()

else()

  set(CMAKE_CXX_COMPILE_OPTIONS_EXPLICIT_LANGUAGE -x c++)

  if (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 19.0.0)
    set(CMAKE_CXX20_STANDARD_COMPILE_OPTION "-std=c++20")
    set(CMAKE_CXX20_EXTENSION_COMPILE_OPTION "-std=gnu++20")
  endif()

  if (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 18.0.0)
    set(CMAKE_CXX17_STANDARD_COMPILE_OPTION "-std=c++17")
    set(CMAKE_CXX17_EXTENSION_COMPILE_OPTION "-std=gnu++17")
  endif()

  if (CMAKE_CXX_COMPILER_VERSION VERSION_GREATER_EQUAL 17.0)
    set(CMAKE_CXX14_STANDARD__HAS_FULL_SUPPORT ON)
  endif()

  if (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 15.0.2)
    set(CMAKE_CXX14_STANDARD_COMPILE_OPTION "-std=c++14")
  elseif (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 15.0.0)
    set(CMAKE_CXX14_STANDARD_COMPILE_OPTION "-std=c++1y")
  endif()

  # Intel 15.0.2 accepts c++14 instead of c++1y, but not gnu++14
  # instead of gnu++1y.  Intel 17.0.0 accepts gnu++14 too.
  if(NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 17.0)
    set(CMAKE_CXX14_EXTENSION_COMPILE_OPTION "-std=gnu++14")
  elseif (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 15.0.0)
    set(CMAKE_CXX14_EXTENSION_COMPILE_OPTION "-std=gnu++1y")
  endif()

  if (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 15.0)
    set(CMAKE_CXX11_STANDARD__HAS_FULL_SUPPORT ON)
  endif()

  if (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 13.0)
    set(CMAKE_CXX11_STANDARD_COMPILE_OPTION "-std=c++11")
    set(CMAKE_CXX11_EXTENSION_COMPILE_OPTION "-std=gnu++11")
  elseif (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 12.1)
    set(CMAKE_CXX11_STANDARD_COMPILE_OPTION "-std=c++0x")
    set(CMAKE_CXX11_EXTENSION_COMPILE_OPTION "-std=gnu++0x")
  endif()

  if (NOT CMAKE_CXX_COMPILER_VERSION VERSION_LESS 12.1)
    set(CMAKE_CXX98_STANDARD_COMPILE_OPTION "-std=c++98")
    set(CMAKE_CXX98_EXTENSION_COMPILE_OPTION "-std=gnu++98")
    set(CMAKE_CXX98_STANDARD__HAS_FULL_SUPPORT ON)
  endif()

endif()

__compiler_check_default_language_standard(CXX 12.1 98)

set(CMAKE_CXX_CREATE_PREPROCESSED_SOURCE "<CMAKE_CXX_COMPILER> <DEFINES> <INCLUDES> <FLAGS> -E <SOURCE> > <PREPROCESSED_SOURCE>")
set(CMAKE_CXX_CREATE_ASSEMBLY_SOURCE "<CMAKE_CXX_COMPILER> <DEFINES> <INCLUDES> <FLAGS> -S <SOURCE> -o <ASSEMBLY_SOURCE>")
