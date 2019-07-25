#include "wrapper.h"

#include "colors.h"

#include <iostream>
#include <set>
#include <string>

#define CXXOPTS_USE_UNICODE

const std::set<std::string> VALID_LANG= {"Numpy", "OpenMP", "Bang", "Cuda", "OpenCL", "Julia", "CCE"};

void create_options(Options &options) {
  options.positional_help("[optional args]").show_positional_help();
  options.allow_unrecognised_options().add_options()("h, help", "Print help")(
      "i, input", "Input phaeton source file", cxxopts::value<std::string>())(
      "l, lang",
      "Emit target language, currently supports: Numpy, OpenMP, OpenCL, CUDA, "
      "BANG, CCE, TPU",
      cxxopts::value<std::string>()->default_value("OpenMP"))(
      "o, output", "Output file",
      cxxopts::value<std::string>()->default_value("a.cpp"))(
      "positional",
      "These are the arguments that are entered "
      "without an option",
      cxxopts::value<std::vector<std::string>>())
      ("ast-dump", "Phaeton AST dump");

  options.parse_positional({"input", "positional"});
}

ParseResult parse_args(Options &options, int &argc, char **argv) {
  if (argc < 2) {
    std::cerr << "ph-opt:" << FRED(" error: ")
              << "no input files! Usage see option '--help'.\n";
    exit(-1);
  }

  try {
    auto result = options.parse(argc, argv);
    std::cout << "Arguments remain = " << argc << std::endl;
    return result;
  } catch (const cxxopts::OptionException &e) {
    std::cout << "error parsing options: " << e.what() << std::endl;
    exit(1);
  }
}

void build_jobs(const Options &options, const ParseResult &result) {
  if (result.count("help")) {
    std::cout << options.help({"", "Group"}) << std::endl;
    exit(0);
  }

  if (result.count("input")) {
    std::cout << "Input = " << result["input"].as<std::string>() << std::endl;
  }

  if (result.count("ast-dump")) {
    std::cout << "Option = AST dump" << std::endl;
  }

  if (result.count("lang")) {
    std::string tgt_lang = result["lang"].as<std::string>();
    std::cout << "Target language = " << tgt_lang
              << std::endl;
    if (VALID_LANG.count(tgt_lang)) {
      if (!std::strcmp(tgt_lang.c_str(), "Numpy")) {
         std::cout << FRED("Match\n");
      }
    }
  } else {
    std::cout << "Default target language = OpenMP\n";
  }

  if (result.count("output")) {
    std::cout << "Output = " << result["output"].as<std::string>() << std::endl;
  } else {
    std::cout << "Default output = a.cpp\n";
  }

  if (result.count("positional")) {
    std::cout << "Positional = {";
    auto &v = result["positional"].as<std::vector<std::string>>();
    for (const auto &s : v) {
      std::cout << s << ", ";
    }
    std::cout << "}" << std::endl;
  }
}

int main(int argc, char *argv[]) {
  Options options(argv[0], "Phaeton optimizer command line options");
  create_options(options);
  auto result = parse_args(options, argc, argv);
  auto arguments = result.arguments();
  std::cout << "Saw " << arguments.size() << " arguments" << std::endl;

  build_jobs(options, result);

  return 0;
}
