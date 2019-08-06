// REF: https://zh.cppreference.com/w/cpp/io/manip/endl
#include <chrono>
#include <iostream>

template <typename Diff> void log_progress(Diff d) {
  std::cout << std::chrono::duration_cast<std::chrono::milliseconds>(d).count()
            << " ms passed" << std::endl;
}

template <typename Diff> void log_progress_n(Diff d) {
  std::cout << std::chrono::duration_cast<std::chrono::milliseconds>(d).count()
            << " ms passed" << '\n';
}

int main() {
  // std::endl
  {
    std::cout.sync_with_stdio(false);
    volatile int sink = 0;

    auto t1 = std::chrono::high_resolution_clock::now();

    for (int j = 0; j < 5; ++j) {
      for (int n = 0; n < 20000; ++n)
        for (int m = 0; m < 40000; ++m)
          sink += m * n;

      auto now = std::chrono::high_resolution_clock::now();
      log_progress(now - t1);
    }
  }
  std::cout << "===-----------------------------------===\n";
  // '\n'
  {
    //std::cout.sync_with_stdio(false);
    volatile int sink = 0;

    auto t1 = std::chrono::high_resolution_clock::now();

    for (int j = 0; j < 5; ++j) {
      for (int n = 0; n < 10000; ++n)
        for (int m = 0; m < 20000; ++m)
          sink += m * n;

      auto now = std::chrono::high_resolution_clock::now();
      log_progress_n(now - t1);
    }
  }
}
