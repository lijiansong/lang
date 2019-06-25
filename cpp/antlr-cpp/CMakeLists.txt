cmake_minimum_required(VERSION 3.5)

set(EXECUTABLE_OUTPUT_PATH ${CMAKE_CURRENT_BINARY_DIR}/bin)
set(LIBRARY_OUTPUT_PATH ${CMAKE_CURRENT_BINARY_DIR}/lib)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "RELEASE" CACHE STRING "" FORCE)
endif()

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -fPIC")

include_directories(
  ${PROJECT_SOURCE_DIR}/include
  ${PROJECT_SOURCE_DIR}/lib/antlr4-runtime
  ${PROJECT_SOURCE_DIR}/lib/antlr4-runtime/misc
  ${PROJECT_SOURCE_DIR}/lib/antlr4-runtime/atn
  ${PROJECT_SOURCE_DIR}/lib/antlr4-runtime/dfa
  ${PROJECT_SOURCE_DIR}/lib/antlr4-runtime/tree
  ${PROJECT_SOURCE_DIR}/lib/antlr4-runtime/support
  ${PROJECT_SOURCE_DIR}/lib
  )

add_subdirectory(lib)
add_subdirectory(tools)
#add_subdirectory(tests)
