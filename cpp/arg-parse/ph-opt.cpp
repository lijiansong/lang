#include "cxxopts.hpp"

#include <iostream>

#define CXXOPTS_USE_UNICODE

cxxopts::ParseResult parse(int argc, char *argv[]) {
  try {
    cxxopts::Options options(argv[0], "Phaeton optimizer command line options");
    options.positional_help("[optional args]").show_positional_help();

    options.allow_unrecognised_options().add_options()
        ("h, help", "Print help")
        ("i, input", "Input phaeton source file", cxxopts::value<std::string>())
        ("l, lang", "Emit target language, currently supports: Numpy, OpenMP, OpenCL, CUDA, BANG, CCE, TPU",cxxopts::value<std::string>()->default_value("OpenMP"))
        ("o, output", "Output file",cxxopts::value<std::string>()->default_value("a.cpp"))
        ("positional", "Positional arguments: these are the arguments that are entered "
               "without an option",cxxopts::value<std::vector<std::string>>())
        ;

    options.add_options("Group")("c,compile", "compile")(
        "d,drop", "drop", cxxopts::value<std::vector<std::string>>());

    //options.parse_positional({"input", "output", "positional"});
    options.parse_positional({"input", "positional"});

    auto result = options.parse(argc, argv);

    if (result.count("help")) {
      std::cout << options.help({"", "Group"}) << std::endl;
      exit(0);
    }

    if (result.count("input")) {
      std::cout << "Input = " << result["input"].as<std::string>() << std::endl;
    }

    if (result.count("lang")) {
      std::cout << "Target language = " << result["lang"].as<std::string>()
                << std::endl;
    } else {
      std::cout << "Default target language = OpenMP\n";
    }

    if (result.count("output")) {
      std::cout << "Output = " << result["output"].as<std::string>()
                << std::endl;
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

    std::cout << "Arguments remain = " << argc << std::endl;

    return result;

  } catch (const cxxopts::OptionException &e) {
    std::cout << "error parsing options: " << e.what() << std::endl;
    exit(1);
  }
}

int main(int argc, char *argv[]) {
  auto result = parse(argc, argv);
  auto arguments = result.arguments();
  std::cout << "Saw " << arguments.size() << " arguments" << std::endl;

  return 0;
}
