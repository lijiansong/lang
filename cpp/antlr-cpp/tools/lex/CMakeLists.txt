# Add incldue path for 'lex.yy.h' and 'lang.tab.hh'
include_directories(${TENSORIR_LANG_OUTPUT_DIR})

add_executable(scene-lex main.cpp)
target_link_libraries(scene-lex Parse
                                antlr4_static)
