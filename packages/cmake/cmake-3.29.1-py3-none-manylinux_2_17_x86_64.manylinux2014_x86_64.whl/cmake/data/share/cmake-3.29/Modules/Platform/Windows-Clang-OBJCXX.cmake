include(Platform/Windows-Clang)
__windows_compiler_clang(OBJCXX)

if("x${CMAKE_OBJCXX_COMPILER_FRONTEND_VARIANT}" STREQUAL "xMSVC")
  if((NOT DEFINED CMAKE_DEPENDS_USE_COMPILER OR CMAKE_DEPENDS_USE_COMPILER)
      AND CMAKE_GENERATOR MATCHES "Makefiles|WMake"
      AND CMAKE_DEPFILE_FLAGS_OBJCXX)
    set(CMAKE_OBJCXX_DEPENDS_USE_COMPILER TRUE)
  endif()
elseif("x${CMAKE_OBJCXX_COMPILER_FRONTEND_VARIANT}" STREQUAL "xGNU")
  if((NOT DEFINED CMAKE_DEPENDS_USE_COMPILER OR CMAKE_DEPENDS_USE_COMPILER)
      AND CMAKE_GENERATOR MATCHES "Makefiles|WMake"
      AND CMAKE_DEPFILE_FLAGS_OBJCXX)
    # dependencies are computed by the compiler itself
    set(CMAKE_OBJCXX_DEPFILE_FORMAT gcc)
    set(CMAKE_OBJCXX_DEPENDS_USE_COMPILER TRUE)
  endif()
endif()
