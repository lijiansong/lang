int *B0;
int B1[100], B2[100];
int B3[200];
int main() {
  int cond = 1;
  char *p, *q;
  B0 = B3;
  B1[0] = 10;
  if (cond)
    q = &B1[2];
  else
    q = B2;
  *q = B1[0];
  p = B0;
  *p = *q;
}
