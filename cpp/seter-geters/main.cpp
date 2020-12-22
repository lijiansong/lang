#include "house.h"
#include <iostream>

int main() {
  House h;
  h.SetHeight(18);
  std::cout << h.GetHeight() << std::endl;
  h.SetHeight(-100);
  std::cout << h.GetHeight() << std::endl;
  return 0;
}
