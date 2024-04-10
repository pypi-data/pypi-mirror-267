include(Compiler/IntelLLVM)
__compiler_intel_llvm(C)

if("x${CMAKE_C_COMPILER_FRONTEND_VARIANT}" STREQUAL "xMSVC")
  set(CMAKE_C_COMPILE_OPTIONS_EXPLICIT_LANGUAGE -TC)
  set(CMAKE_C_CLANG_TIDY_DRIVER_MODE "cl")
  set(CMAKE_C_INCLUDE_WHAT_YOU_USE_DRIVER_MODE "cl")
  if((NOT DEFINED CMAKE_DEPENDS_USE_COMPILER OR CMAKE_DEPENDS_USE_COMPILER)
      AND CMAKE_GENERATOR MATCHES "Makefiles|WMake"
      AND CMAKE_DEPFILE_FLAGS_C)
    set(CMAKE_C_DEPENDS_USE_COMPILER TRUE)
  endif()
else()
  set(CMAKE_C_COMPILE_OPTIONS_EXPLICIT_LANGUAGE -x c)
  if((NOT DEFINED CMAKE_DEPENDS_USE_COMPILER OR CMAKE_DEPENDS_USE_COMPILER)
      AND CMAKE_GENERATOR MATCHES "Makefiles|WMake"
      AND CMAKE_DEPFILE_FLAGS_C)
    # dependencies are computed by the compiler itself
    set(CMAKE_C_DEPFILE_FORMAT gcc)
    set(CMAKE_C_DEPENDS_USE_COMPILER TRUE)
  endif()

  string(APPEND CMAKE_C_FLAGS_MINSIZEREL_INIT " -DNDEBUG")
  string(APPEND CMAKE_C_FLAGS_RELEASE_INIT " -DNDEBUG")
  string(APPEND CMAKE_C_FLAGS_RELWITHDEBINFO_INIT " -DNDEBUG")
endif()

set(CMAKE_C90_STANDARD__HAS_FULL_SUPPORT ON)
set(CMAKE_C99_STANDARD__HAS_FULL_SUPPORT ON)
set(CMAKE_C11_STANDARD__HAS_FULL_SUPPORT ON)

if(NOT "x${CMAKE_C_SIMULATE_ID}" STREQUAL "xMSVC")
  set(CMAKE_C90_STANDARD_COMPILE_OPTION "-std=c90")
  set(CMAKE_C90_EXTENSION_COMPILE_OPTION "-std=gnu90")

  set(CMAKE_C99_STANDARD_COMPILE_OPTION "-std=c99")
  set(CMAKE_C99_EXTENSION_COMPILE_OPTION "-std=gnu99")

  set(CMAKE_C11_STANDARD_COMPILE_OPTION "-std=c11")
  set(CMAKE_C11_EXTENSION_COMPILE_OPTION "-std=gnu11")

  set(CMAKE_C17_STANDARD_COMPILE_OPTION "-std=c17")
  set(CMAKE_C17_EXTENSION_COMPILE_OPTION "-std=gnu17")

  set(CMAKE_C23_STANDARD_COMPILE_OPTION "-std=c2x")
  set(CMAKE_C23_EXTENSION_COMPILE_OPTION "-std=gnu2x")
else()
  # clang-cl doesn't have any of these
  set(CMAKE_C90_STANDARD_COMPILE_OPTION "")
  set(CMAKE_C90_EXTENSION_COMPILE_OPTION "")

  set(CMAKE_C99_STANDARD_COMPILE_OPTION "")
  set(CMAKE_C99_EXTENSION_COMPILE_OPTION "")

  set(CMAKE_C11_STANDARD_COMPILE_OPTION "")
  set(CMAKE_C11_EXTENSION_COMPILE_OPTION "")

  set(CMAKE_C17_STANDARD_COMPILE_OPTION "")
  set(CMAKE_C17_EXTENSION_COMPILE_OPTION "")

  set(CMAKE_C23_STANDARD_COMPILE_OPTION "")
  set(CMAKE_C23_EXTENSION_COMPILE_OPTION "")
endif()

__compiler_check_default_language_standard(C 2020 17)
