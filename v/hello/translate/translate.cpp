#include <iostream>
#include <string>
#include <vector>

int main() {
  std::vector<std::string> s;
  s.push_back("V is ");
  s.push_back("awesome");
  std::cout << s.size() << std::endl;
  return 0;
}
