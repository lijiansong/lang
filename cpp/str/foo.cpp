#include <iostream>
#include <string>
#include <vector>

/// String delimiter.
std::vector<std::string> SplitString(std::string &str,
                                        std::string delimiter) {
  size_t pos_start = 0, pos_end, delim_len = delimiter.length();
  std::string token;
  std::vector<std::string> res;
  while ((pos_end = str.find(delimiter, pos_start)) != std::string::npos) {
    token = str.substr(pos_start, pos_end - pos_start);
    pos_start = pos_end + delim_len;
    res.push_back(token);
  }
  res.push_back(str.substr(pos_start));
  return res;
}

int main() {
  std::string input_str = "Malloc 1000 Free 1000";
  std::string delimiter = " ";
  auto res = SplitString(input_str, delimiter);
  for (auto &str : res) {
    std::cout << str << std::endl;
  }
  return 0;
}
