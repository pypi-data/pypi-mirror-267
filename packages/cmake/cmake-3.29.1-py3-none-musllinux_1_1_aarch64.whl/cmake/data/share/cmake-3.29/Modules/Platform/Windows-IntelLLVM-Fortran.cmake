include(Platform/Windows-IntelLLVM)
set(CMAKE_BUILD_TYPE_INIT Debug)
set(_COMPILE_Fortran " /fpp")
set(CMAKE_Fortran_MODDIR_FLAG "-module:")
set(CMAKE_Fortran_STANDARD_LIBRARIES_INIT "user32.lib")
__windows_compiler_intel(Fortran)
if(CMAKE_MSVC_RUNTIME_LIBRARY_DEFAULT)
  set(_LIBSDLL "")
  set(_DBGLIBS "")
  set(_THREADS "")
else()
  set(_LIBSDLL " /libs:dll")
  set(_DBGLIBS " /dbglibs")
  set(_THREADS " /threads")
endif()

cmake_policy(GET CMP0092 _cmp0092)
if(NOT _cmp0092 STREQUAL "NEW")
  string(APPEND CMAKE_Fortran_FLAGS_INIT " /W1")
endif()
unset(_cmp0092)

string(APPEND CMAKE_Fortran_FLAGS_INIT " /nologo /fpp${_LIBSDLL}${_THREADS}")
string(APPEND CMAKE_Fortran_FLAGS_DEBUG_INIT " /Od /debug:full${_DBGLIBS}")
string(APPEND CMAKE_Fortran_FLAGS_MINSIZEREL_INIT " /O1 /DNDEBUG")
string(APPEND CMAKE_Fortran_FLAGS_RELEASE_INIT " /O2 /DNDEBUG")
string(APPEND CMAKE_Fortran_FLAGS_RELWITHDEBINFO_INIT " /O2 /debug:full /DNDEBUG")
unset(_LIBSDLL)
unset(_DBGLIBS)
unset(_THREADS)

set(CMAKE_Fortran_COMPILE_OPTIONS_MSVC_RUNTIME_LIBRARY_MultiThreaded         -threads -libs:static)
set(CMAKE_Fortran_COMPILE_OPTIONS_MSVC_RUNTIME_LIBRARY_MultiThreadedDLL      -threads -libs:dll)
set(CMAKE_Fortran_COMPILE_OPTIONS_MSVC_RUNTIME_LIBRARY_MultiThreadedDebug    -threads -libs:static -dbglibs)
set(CMAKE_Fortran_COMPILE_OPTIONS_MSVC_RUNTIME_LIBRARY_MultiThreadedDebugDLL -threads -libs:dll    -dbglibs)
set(CMAKE_Fortran_COMPILE_OPTIONS_MSVC_DEBUG_INFORMATION_FORMAT_Embedded        -Z7)
set(CMAKE_Fortran_COMPILE_OPTIONS_MSVC_DEBUG_INFORMATION_FORMAT_ProgramDatabase -Zi)

# Intel Fortran for Windows supports single-threaded RTL but it is
# not implemented by the Visual Studio integration.
if(NOT CMAKE_GENERATOR MATCHES "Visual Studio")
  set(CMAKE_Fortran_COMPILE_OPTIONS_MSVC_RUNTIME_LIBRARY_SingleThreaded                 -libs:static)
  set(CMAKE_Fortran_COMPILE_OPTIONS_MSVC_RUNTIME_LIBRARY_SingleThreadedDLL              -libs:dll)
  set(CMAKE_Fortran_COMPILE_OPTIONS_MSVC_RUNTIME_LIBRARY_SingleThreadedDebug            -libs:static -dbglibs)
  set(CMAKE_Fortran_COMPILE_OPTIONS_MSVC_RUNTIME_LIBRARY_SingleThreadedDebugDLL         -libs:dll    -dbglibs)
endif()
