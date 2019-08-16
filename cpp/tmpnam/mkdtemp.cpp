#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>

#include <unistd.h> //mkdtemp

//#define DISABLE

#ifdef DISABLE
#ifdef _WIN32
// define something for Windows (32-bit and 64-bit, this part is common)
#ifdef _WIN64
// define something for Windows (64-bit only)
#else
// define something for Windows (32-bit only)
#endif
#elif __APPLE__
#include <experimental/filesystem>
#if TARGET_IPHONE_SIMULATOR
// iOS Simulator
#elif TARGET_OS_IPHONE
// iOS device
#elif TARGET_OS_MAC
// Other kinds of Mac OS
#else
#error "Unknown Apple platform"
#endif
#elif __linux__
// linux
#include <filesystem>
#elif __unix__ // all unices not caught above
// Unix
#elif defined(_POSIX_VERSION)
// POSIX
#else
#error "Unknown compiler"
#endif

namespace fs = std::filesystem;

#endif // DISABLE

int main() {
  // http://man7.org/linux/man-pages/man3/mkdtemp.3.html
  char tmp_name[L_tmpnam];
  mkdtemp(strcpy(tmp_name, "/tmp/phaeton-XXXXXXXXX"));
  std::cout << "temporary file name: " << tmp_name << '\n';
}
