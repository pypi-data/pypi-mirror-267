#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "test-drive::test-drive-lib" for configuration "Release"
set_property(TARGET test-drive::test-drive-lib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(test-drive::test-drive-lib PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "Fortran"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libtest-drive.a"
  )

list(APPEND _cmake_import_check_targets test-drive::test-drive-lib )
list(APPEND _cmake_import_check_files_for_test-drive::test-drive-lib "${_IMPORT_PREFIX}/lib64/libtest-drive.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
