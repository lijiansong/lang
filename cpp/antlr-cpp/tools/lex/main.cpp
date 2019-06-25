#include <iostream>

#include "antlr4-runtime/antlr4-runtime.h"

#include "Scene/Parse/SceneLexer.h"
#include "Scene/Parse/SceneParser.h"

using namespace antlr4;

int main(int argc, const char* argv[]) {

  if (argc < 2) {
    std::cout << "Usage: demo IN_FILE\n";
    return -1;
  }

  std::ifstream stream;
  stream.open(argv[1]);
  ANTLRInputStream input(stream);
  SceneLexer lexer(&input);
  CommonTokenStream tokens(&lexer);
  SceneParser parser(&tokens);
  SceneParser::FileContext* tree = parser.file();

  return 0;
}
