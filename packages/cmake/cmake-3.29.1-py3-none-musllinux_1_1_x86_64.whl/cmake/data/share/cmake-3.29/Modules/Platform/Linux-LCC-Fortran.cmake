include(Platform/Linux-LCC)
__linux_compiler_lcc(Fortran)
if (CMAKE_Fortran_COMPILER_VERSION VERSION_GREATER_EQUAL "1.26.03")
  set(CMAKE_SHARED_LIBRARY_LINK_Fortran_FLAGS "-lgfortran")
elseif (CMAKE_Fortran_COMPILER_VERSION VERSION_GREATER_EQUAL "1.24.01")
  set(CMAKE_SHARED_LIBRARY_LINK_Fortran_FLAGS "-llfortran")
else()
  unset(CMAKE_Fortran_CREATE_PREPROCESSED_SOURCE)
endif()
