#include <time.h>
#include <stdlib.h>

int main() {
  srand(time(NULL));
  int r = rand() % 3;
  int a = 100;
  switch(r) {
    case 0:
        a = 0;
        break;
    case 1:
        a = 1;
        break;
    case 2:
        a = 2;
        break;
  }
  return 0;
}
