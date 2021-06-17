#include <stdio.h>
#include <stdlib.h>

unsigned long get_sp() {
  __asm__("movl %esp, %eax");
}

int main() {
  printf("malloc: %p\n", malloc(16));
  printf("stack: 0x%lx\n", get_sp());
  return 0;
}
