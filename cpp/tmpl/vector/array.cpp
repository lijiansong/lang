#include <iostream>
#include <vector>

int main() {
  static const int shape_values[] = {2, 3, 5, 5, 5};
  // Constructor similar to: std::vector<std::string> words2(words1.begin(),
  // words1.end());
  std::vector<int> shape_size(shape_values, shape_values + 5);
  // 2 3 5 5 5
  for (int i = 0; i < shape_size.size(); ++i) {
    std::cout << shape_size[i] << ' ';
  }
  return 0;
}
