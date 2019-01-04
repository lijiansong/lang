#include <stdio.h>

#include "a.h"
#include "b.h"
int c = a + 1;
int d = b + 1;
int main() {
  printf("c: %d\n", c);
  printf("d: %d\n", d);
  return 0;
}

