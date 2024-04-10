# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

include(Compiler/CrayClang)
__compiler_cray_clang(C)

set(CMAKE_C_COMPILE_OPTIONS_EXPLICIT_LANGUAGE -x c)

string(APPEND CMAKE_C_FLAGS_MINSIZEREL_INIT " -DNDEBUG")
string(APPEND CMAKE_C_FLAGS_RELEASE_INIT " -DNDEBUG")

set(CMAKE_C90_STANDARD_COMPILE_OPTION  -std=c90)
set(CMAKE_C90_EXTENSION_COMPILE_OPTION -std=gnu90)
set(CMAKE_C90_STANDARD__HAS_FULL_SUPPORT ON)

set(CMAKE_C99_STANDARD_COMPILE_OPTION  -std=c99)
set(CMAKE_C99_EXTENSION_COMPILE_OPTION -std=gnu99)
set(CMAKE_C99_STANDARD__HAS_FULL_SUPPORT ON)

set(CMAKE_C11_STANDARD_COMPILE_OPTION  -std=c11)
set(CMAKE_C11_EXTENSION_COMPILE_OPTION -std=gnu11)
set(CMAKE_C11_STANDARD__HAS_FULL_SUPPORT ON)

set(CMAKE_C17_STANDARD_COMPILE_OPTION  -std=c17)
set(CMAKE_C17_EXTENSION_COMPILE_OPTION -std=gnu17)

set(CMAKE_C23_STANDARD_COMPILE_OPTION  -std=c2x)
set(CMAKE_C23_EXTENSION_COMPILE_OPTION -std=gnu2x)

__compiler_check_default_language_standard(C 15.0.0 17)
