#include <stdint.h>
#include <stdio.h>

#define MM_ALIGNMENT 32
#define MM_ALIGN_LEFT(x) (uint8_t *)((uintptr_t)(x) & ~(uintptr_t)(MM_ALIGNMENT - 1))
#define MM_ALIGN_RIGHT(x) (uint8_t *)((uintptr_t)(x + MM_ALIGNMENT - 1) & ~(uintptr_t)(MM_ALIGNMENT - 1))

int main() {
  int a = 63;
  int b = 64;
  printf("%d, left align: %d\n", a, MM_ALIGN_LEFT(a));
  printf("%d, right align: %d\n", a, MM_ALIGN_RIGHT(a));
  printf("%d, left align: %d\n", b, MM_ALIGN_LEFT(b));
  printf("%d, right align: %d\n", b, MM_ALIGN_RIGHT(b));
  return 0;
}
