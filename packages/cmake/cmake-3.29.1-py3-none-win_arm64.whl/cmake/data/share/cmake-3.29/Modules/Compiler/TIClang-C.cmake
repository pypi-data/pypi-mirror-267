include(Compiler/Clang-C)
include(Compiler/TIClang)
__compiler_ticlang(C)

if((NOT DEFINED CMAKE_DEPENDS_USE_COMPILER OR CMAKE_DEPENDS_USE_COMPILER)
    AND CMAKE_GENERATOR MATCHES "Makefiles|WMake"
    AND CMAKE_DEPFILE_FLAGS_C)
  # dependencies are computed by the compiler itself
  set(CMAKE_C_DEPFILE_FORMAT gcc)
  set(CMAKE_C_DEPENDS_USE_COMPILER TRUE)
endif()

set(CMAKE_C90_STANDARD_COMPILE_OPTION "-std=c90")
set(CMAKE_C90_EXTENSION_COMPILE_OPTION "-std=gnu90")
set(CMAKE_C90_STANDARD__HAS_FULL_SUPPORT ON)

set(CMAKE_C99_STANDARD_COMPILE_OPTION "-std=c99")
set(CMAKE_C99_EXTENSION_COMPILE_OPTION "-std=gnu99")
set(CMAKE_C99_STANDARD__HAS_FULL_SUPPORT ON)

set(CMAKE_C11_STANDARD_COMPILE_OPTION "-std=c11")
set(CMAKE_C11_EXTENSION_COMPILE_OPTION "-std=gnu11")
set(CMAKE_C11_STANDARD__HAS_FULL_SUPPORT ON)
