#include <iostream>
#include <map>
#include <string>

extern std::map<std::string, std::string> BlkTypeMap;

int main() {
  for (auto it : BlkTypeMap) {
    std::cout << it.first << ' ' << it.second << '\n';
  }
  return 0;
}
