add_library(Parse STATIC
            SceneLexer.cpp
            SceneParser.cpp
            SceneBaseVisitor.cpp
            SceneVisitor.cpp)

include_directories(
  ${PROJECT_SOURCE_DIR}/lib/antlr4-runtime
  ${PROJECT_SOURCE_DIR}/lib/antlr4-runtime/misc
  ${PROJECT_SOURCE_DIR}/lib/antlr4-runtime/atn
  ${PROJECT_SOURCE_DIR}/lib/antlr4-runtime/dfa
  ${PROJECT_SOURCE_DIR}/lib/antlr4-runtime/tree
  ${PROJECT_SOURCE_DIR}/lib/antlr4-runtime/support
  ${PROJECT_SOURCE_DIR}/lib
  )
