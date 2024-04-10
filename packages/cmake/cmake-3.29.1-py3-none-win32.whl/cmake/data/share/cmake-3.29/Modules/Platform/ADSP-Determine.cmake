if(IS_DIRECTORY "$ENV{ADSP_ROOT}")
    file(TO_CMAKE_PATH "$ENV{ADSP_ROOT}" CMAKE_ADSP_ROOT)
endif()

macro(_find_adsp_root path_pattern)
  set(CMAKE_ADSP_ROOT "")
  set(_adsp_root_version "0")
  file(GLOB _adsp_root_paths "${path_pattern}")
  foreach(_current_adsp_root_path IN LISTS _adsp_root_paths)
    string(REGEX MATCH "([0-9\\.]+)/?$" _current_adsp_root_version "${_current_adsp_root_path}")
    if(_current_adsp_root_version VERSION_GREATER _adsp_root_version)
      set(CMAKE_ADSP_ROOT "${_current_adsp_root_path}")
      set(_adsp_root_version "${_current_adsp_root_version}")
    endif()
  endforeach()
endmacro()

if(NOT CMAKE_ADSP_ROOT)
  _find_adsp_root("C:/Analog Devices/CrossCore Embedded Studio *")
endif()
if(NOT CMAKE_ADSP_ROOT)
  _find_adsp_root("C:/Program Files (x86)/Analog Devices/VisualDSP *")
endif()
if(NOT CMAKE_ADSP_ROOT)
  _find_adsp_root("/opt/analog/cces *")
endif()
