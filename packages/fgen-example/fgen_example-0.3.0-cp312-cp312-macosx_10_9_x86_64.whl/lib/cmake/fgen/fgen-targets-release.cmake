#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "fgen::fgen-lib" for configuration "Release"
set_property(TARGET fgen::fgen-lib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(fgen::fgen-lib PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "Fortran"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libfgen.a"
  )

list(APPEND _cmake_import_check_targets fgen::fgen-lib )
list(APPEND _cmake_import_check_files_for_fgen::fgen-lib "${_IMPORT_PREFIX}/lib/libfgen.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
