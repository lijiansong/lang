/*
 * REF:
 * http://www.ruanyifeng.com/blog/2010/06/ieee_floating-point_representation.html
 * https://en.wikipedia.org/wiki/Kahan_summation_algorithm
 *
 * */

#include <stdio.h>
#include <stdlib.h>

int main() {
  // example 1
  float a = 0.3f, b = 0.6f;
  float c = a + b;
  printf("%f\n", c);
  printf("0.3 + 0.6 = %f\n", c);

  // example 2
  int num=9;
  float* pFloat=&num;
  printf("num: %d\n",num);
  printf("*pFloat: %f\n",*pFloat);
  *pFloat=9.0;
  printf("num: %d\n",num);
  printf("*pFloat: %f\n",*pFloat);

  // example 3
  a = 20000000.0f;
  b = 1.f;
  c = a + b;
  float d = c - a;
  printf("a: %f\n", a);
  printf("b: %f\n", b);
  printf("a + b: %f\n", c);
  printf("c - a: %f\n", d);

  // example 4
  float sum = 0.f;
  int i;
  for (i = 0; i < 20000000; ++i) {
    float x = 1.f;
    sum += x;
  }
  // result would be 16777216.000000
  printf("sum: %f\n", sum);

  // Kahan summation for example 4
  sum = 0.f;
  c = 0.f;
  for (i = 0; i < 20000000; ++i) {
    float x = 1.f;
    float y = x - c;
    float t = sum + y;
    c = (t - sum) - y;
    sum = t;
  }
  printf("sum: %f\n", sum);

  return 0;
}
