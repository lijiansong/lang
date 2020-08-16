#include <iostream>
#include <sstream>

int main() {
  int a = 1;
  int *p_a = &a;
  // store p_a into a string stream.
  std::stringstream ss_a;
  ss_a << p_a;
  std::cout << "ss_a str: " << ss_a.str() << std::endl;

  // convert p_a from string stream.
  std::stringstream convert(ss_a.str());
  void *convert_pa = nullptr;
  convert >> convert_pa;
  auto pa = static_cast<int *>(convert_pa);
  std::cout << "hex convert_pa:" << std::hex << convert_pa << std::endl;
  std::cout << "hex pa" << std::hex << pa << std::endl;
  std::cout << "*convert_pa: " << *pa << std::endl;
}
