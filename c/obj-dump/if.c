#include <time.h>
#include <stdlib.h>

int main() {
  srand(time(NULL));
  int r = rand() % 2;
  int a = 100;
  if (r == 0) {
    a = 0;
  } else {
    a = 1;
  }
  return 0;
}
