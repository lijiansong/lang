#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <string>

//#define DISABLE

#ifdef DISABLE
#ifdef _WIN32
   //define something for Windows (32-bit and 64-bit, this part is common)
   #ifdef _WIN64
      //define something for Windows (64-bit only)
   #else
      //define something for Windows (32-bit only)
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
    #   error "Unknown Apple platform"
    #endif
#elif __linux__
    // linux
    #include <filesystem>
#elif __unix__ // all unices not caught above
    // Unix
#elif defined(_POSIX_VERSION)
    // POSIX
#else
#   error "Unknown compiler"
#endif

namespace fs = std::filesystem;

#endif // DISABLE

int main() {
  // std::tmpnam
  std::string name1 = std::tmpnam(nullptr);
  std::cout << "temporary file name: " << name1 << '\n';

  char name2[L_tmpnam];
  if (std::tmpnam(name2)) {
    std::cout << "temporary file name: " << name2 << '\n';
  }

#ifdef DISABLE
  // std::tmpfile
  std::FILE* tmpf = std::tmpfile();
    std::fputs("Hello, world", tmpf);
    std::rewind(tmpf);
    char buf[6];
    std::fgets(buf, sizeof buf, tmpf);
    std::cout << buf << '\n';

    // Linux-specific method to display the tmpfile name
    std::cout << fs::read_symlink(
                     fs::path("/proc/self/fd") / std::to_string(fileno(tmpf))
                 ) << '\n';
#endif // DISABLE
}
