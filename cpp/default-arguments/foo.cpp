#include <iostream>

void point(int x = 3, int y = 4) {
  std::cout << __func__ << "(" << x << ", " << y << ")\n";
}

template <class... T> struct C { void a(int n = 0, T...); };

int a(int n = 0, ...) { return n; }

template <class... T> void b(int i = 0, T... args) {}

namespace N {
void f(int x, int = 1);
} // namespace N

using N::f;
void g() {
  f(7); // calls f(7, 1);
  /* f();  // error*/
}

namespace N {
void f(int = 2, int x) { std::cout << __func__ << '\n'; }
} // namespace N

/// Note: in clang 9.0, drop an err msg:
// error: no matching function for call to 'f'
void h() {
  // calls f(2, 1);
  // f();
}

struct Base {
  virtual void f(int a = 7) {}
};

struct Derived : Base {
  void f(int a) override {}
};

void m() {
  Derived d;
  Base &b = d;
  b.f(); // OK: calls Derived::f(7)

  // d.f(); // Error: no default
}

int main() {
  {
    point(1, 2); // calls point(1,2)
    point(1);    // calls point(1,4)
    point();     // calls point(3,4)
  }
  {
    C<int> c; // OK; instantiates declaration void C::f(int n = 0, int)
  }
  {
    b(4);
    int i = 10;
    b(i);
  }
  { a(100, 100); }
  { m(); }
  return 0;
}
