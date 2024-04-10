include(Compiler/Intel)
__compiler_intel(Fortran)

set(CMAKE_Fortran_SUBMODULE_SEP "@")
set(CMAKE_Fortran_SUBMODULE_EXT ".smod")

set(CMAKE_Fortran_MODDIR_FLAG "-module ")
set(CMAKE_Fortran_FORMAT_FIXED_FLAG "-fixed")
set(CMAKE_Fortran_FORMAT_FREE_FLAG "-free")

set(CMAKE_Fortran_COMPILE_WITH_DEFINES 1)

set(CMAKE_Fortran_CREATE_PREPROCESSED_SOURCE "<CMAKE_Fortran_COMPILER> <DEFINES> <INCLUDES> <FLAGS> -E <SOURCE> > <PREPROCESSED_SOURCE>")
set(CMAKE_Fortran_CREATE_ASSEMBLY_SOURCE "<CMAKE_Fortran_COMPILER> <DEFINES> <INCLUDES> <FLAGS> -S <SOURCE> -o <ASSEMBLY_SOURCE>")

if(CMAKE_HOST_WIN32)
  # MSVC-like
  set(CMAKE_Fortran_PREPROCESS_SOURCE
    "<CMAKE_Fortran_COMPILER> -fpp <DEFINES> <INCLUDES> <FLAGS> -P <SOURCE> -Fi<PREPROCESSED_SOURCE>")
else()
  # GNU-like
  set(CMAKE_Fortran_PREPROCESS_SOURCE
    "<CMAKE_Fortran_COMPILER> -fpp <DEFINES> <INCLUDES> <FLAGS> -P <SOURCE> -o <PREPROCESSED_SOURCE>")
endif()

set(CMAKE_Fortran_COMPILE_OPTIONS_PREPROCESS_ON "-fpp")
set(CMAKE_Fortran_COMPILE_OPTIONS_PREPROCESS_OFF "-nofpp")
