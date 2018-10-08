// https://gcc.gnu.org/onlinedocs/gcc/Vector-Extensions.html
typedef int v4si __attribute__((vector_size(16)));

int main() {
  v4si a, b, c;
  c = a + b;
}
