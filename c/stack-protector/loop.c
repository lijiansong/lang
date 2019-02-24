/*
 * This example is related with the byte alignment and memory alloction of compiler,
 * 3 array elements integer type with the variable i, we can get 16 bytes alignmnet.
 *
 * If we dump the compiler default option, you will find -stack-protector.
 * gcc loop.c -fno-stack-protector
 *
 * */

#include <stdio.h>

int main() {
    int i = 0;
    int a[3] = {0};
    for (; i <= 3; ++i) {
      // Here, if we enable -fno-stack-protector compiler option,
      // if i == 3, and combine with stack address,
      // a[3] will point to the address of i, so the loop will never end.
      a[i] = 0;
      printf("hello world\n");
    }
    return 0;
}
