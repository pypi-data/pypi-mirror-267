set(CMAKE_SHARED_LIBRARY_C_FLAGS "-G 0")
set(CMAKE_SHARED_LIBRARY_SUFFIX "..o")
set(CMAKE_DL_LIBS "")
set(CMAKE_SHARED_LIBRARY_LINK_C_FLAGS "-Wl,-D,08000000")
include(Platform/UnixPaths)
