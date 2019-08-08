#include <iostream>
#include <vector>

auto make_function(int &x) {
  return [&] { std::cout << x << '\n'; };
}

void f3() {
  float x, &r = x;
  [=] { // x and r are not captured (appearance in a decltype operand is not an
        // odr-use)
    decltype(x) y1;        // y1 has type float
    decltype((x)) y2 = y1; // y2 has type float const& because this lambda
                           // is not mutable and x is an lvalue
    decltype(r) r1 = y1;   // r1 has type float& (transformation not considered)
    decltype((r)) r2 = y2; // r2 has type float const&
  };
}

int main() {
  /// 1. For every parameter in params whose type is specified as auto, an
  /// invented template parameter is added to template-params, in order of
  /// appearance. The invented template parameter may be a parameter pack if the
  /// corresponding function member of params is a function parameter pack.
  {
    // generic lambda, operator() is a template with two parameters
    auto glambda = [](auto a, auto &&b) { return a < b; };
    bool b = glambda(3, 3.14); // ok

    // generic lambda, operator() is a template with one parameter
    auto vglambda = [](auto printer) {
      return [=](auto &&... ts) // generic lambda, ts is a parameter pack
      {
        printer(std::forward<decltype(ts)>(ts)...);
        return [=] { printer(ts...); }; // nullary lambda (takes no parameters)
      };
    };
    auto p = vglambda(
        [](auto v1, auto v2, auto v3) { std::cout << v1 << v2 << v3; });
    auto q = p(1, 'a', 3.14); // outputs 1a3.14
    q();                      // outputs 1a3.14
  }
  std::cout << "\n-------------------------\n";
  {
    int i = 3;
    auto f = make_function(i); // the use of x in f binds directly to i
    i = 5;
    f(); // OK; prints 5
  }
  std::cout << "\n-------------------------\n";
  { f3(); }
  std::cout << "\n-------------------------\n";
  /// If a lambda-expression appears in a default argument, it cannot explicitly
  /// or implicitly capture anything.

  /// Members of anonymous unions cannot be captured.

  /// If a nested lambda m2 captures something that is also captured by the
  /// immediately enclosing lambda m1, then m2's capture is transformed as
  /// follows:
  /// - if the enclosing lambda m1 captures by copy, m2 is capturing the
  /// non-static member of m1's closure type, not the original variable or this.
  /// - if the enclosing lambda m1 by reference, m2 is capturing the original
  /// variable or this.
  {
    int a = 1, b = 1, c = 1;

    auto m1 = [a, &b, &c]() mutable {
      auto m2 = [a, b, &c]() mutable {
        std::cout << a << b << c << '\n';
        a = 4;
        b = 4;
        c = 4;
      };
      a = 3;
      b = 3;
      c = 3;
      m2();
    };

    a = 2, b = 2, c = 2;

    m1();                             // calls m2() and prints 123
    std::cout << a << b << c << '\n'; // prints 234
  }
  std::cout << "\n-------------------------\n";
  {
    std::vector<int> c = {1, 2, 3, 4, 5, 6, 7};
    int x = 5;
    c.erase(std::remove_if(c.begin(), c.end(), [x](int n) { return n < x; }),
            c.end());

    std::cout << "c: ";
    std::for_each(c.begin(), c.end(), [](int i) { std::cout << i << ' '; });
    std::cout << '\n';

    // the type of a closure cannot be named, but can be inferred with auto
    // since C++14, lambda could own default arguments
    auto func1 = [](int i = 6) { return i + 4; };
    std::cout << "func1: " << func1() << '\n';

    // like all callable objects, closures can be captured in std::function
    // (this may incur unnecessary overhead)
    std::function<int(int)> func2 = [](int i) { return i + 4; };
    std::cout << "func2: " << func2(6) << '\n';
  }
  return 0;
}
