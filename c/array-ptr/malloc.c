#include <stdio.h>
#include <stdlib.h>

int main() {
  int len = 100;
  int *data = (int *)malloc(len * sizeof(int));
  for (int i = 0; i < len; ++i) {
    printf("%d\n", *(data + i));
  }
  free(data);
  return 0;
}
