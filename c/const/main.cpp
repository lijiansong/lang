#include <stdio.h>

#include "ref.h"

int c = a + 1;
int main() {
  printf("a: %d\n", a);
  printf("b: %d\n", b);
  printf("c: %d\n", c);
  return 0;
}
