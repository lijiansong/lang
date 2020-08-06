#include <chrono>
#include <iostream>
#include <unistd.h>

namespace foo {

class Timer {
public:
  double elapsed() const {
    return std::chrono::duration<double>(
               std::chrono::high_resolution_clock::now().time_since_epoch())
        .count();
  }
};

} // namespace foo

int main() {
  foo::Timer t;
  double t1 = t.elapsed();
  std::cout << "t1 = " << t1 << std::endl;
  sleep(1);
  double t2 = t.elapsed();
  std::cout << "t2 = " << t2 << std::endl;
  std::cout << "delta = " << t2 - t1 << " ms" << std::endl;
  return 0;
}
