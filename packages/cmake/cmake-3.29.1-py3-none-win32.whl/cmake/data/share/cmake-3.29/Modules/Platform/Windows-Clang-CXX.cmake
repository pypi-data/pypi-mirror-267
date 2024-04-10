include(Platform/Windows-Clang)
set(_COMPILE_CXX_MSVC " -TP")
__windows_compiler_clang(CXX)

if("x${CMAKE_CXX_COMPILER_FRONTEND_VARIANT}" STREQUAL "xMSVC")
  if((NOT DEFINED CMAKE_DEPENDS_USE_COMPILER OR CMAKE_DEPENDS_USE_COMPILER)
      AND CMAKE_GENERATOR MATCHES "Makefiles|WMake"
      AND CMAKE_DEPFILE_FLAGS_CXX)
    set(CMAKE_CXX_DEPENDS_USE_COMPILER TRUE)
  endif()
elseif("x${CMAKE_CXX_COMPILER_FRONTEND_VARIANT}" STREQUAL "xGNU")
  if((NOT DEFINED CMAKE_DEPENDS_USE_COMPILER OR CMAKE_DEPENDS_USE_COMPILER)
      AND CMAKE_GENERATOR MATCHES "Makefiles|WMake"
      AND CMAKE_DEPFILE_FLAGS_CXX)
    # dependencies are computed by the compiler itself
    set(CMAKE_CXX_DEPFILE_FORMAT gcc)
    set(CMAKE_CXX_DEPENDS_USE_COMPILER TRUE)
  endif()
endif()
