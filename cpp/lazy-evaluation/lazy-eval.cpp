// REF: https://web.archive.org/web/20090421155750/http://ubiety.uwaterloo.ca/~tveldhui/papers/Expression-Templates/exprtmpl.html

#include <cmath>
#include <iostream>

using namespace std;

template <typename A> class DExpr {
  A a_;

public:
  DExpr(const A &x = A()) : a_(x) {}
  double operator()(double x) const { return a_(x); }
};

class DExprIdentity {
public:
  double operator()(double x) const { return x; }
};

typedef DExpr<DExprIdentity> DPlaceholder;

class DExprLiteral {
  double value_;

public:
  DExprLiteral(double value) : value_(value) {}
  double operator()(double x) const { return value_; }
};

class DApAdd {
public:
  static double apply(double a, double b) { return a + b; }
};

class DApSub {
public:
  static double apply(double a, double b) { return a - b; }
};

class DApDivide {
public:
  static double apply(double a, double b) { return a / b; }
};

class DApMultiply {
public:
  static double apply(double a, double b) { return a * b; }
};

class DApSine {
public:
  static double apply(double a) { return std::sin(a); }
};

class DApCosine {
public:
  static double apply(double a) { return std::cos(a); }
};

template <typename A, typename B, typename Op> class DBinExprOp {
  A a_;
  B b_;

public:
  DBinExprOp(const A &a, const B &b) : a_(a), b_(b) {}
  double operator()(double x) const { return Op::apply(a_(x), b_(x)); }
};

template <typename A, typename Op> class DUniExprOp {
  A a_;

public:
  DUniExprOp(const A &a) : a_(a) {}
  double operator()(double x) const { return Op::apply(a_(x)); }
};

template <class A>
DExpr<DBinExprOp<DExprLiteral, DExpr<A>, DApAdd>> operator+(double x,
                                                            const DExpr<A> &a) {
  typedef DBinExprOp<DExprLiteral, DExpr<A>, DApAdd> ExprT;
  return DExpr<ExprT>(ExprT(DExprLiteral(x), a));
}

template <class A>
DExpr<DBinExprOp<DExprLiteral, DExpr<A>, DApAdd>> operator+(const DExpr<A> &a,
                                                            double x) {
  return x + a;
}

template <class A>
DExpr<DBinExprOp<DExprLiteral, DExpr<A>, DApSub>> operator-(double x,
                                                            const DExpr<A> &a) {
  typedef DBinExprOp<DExprLiteral, DExpr<A>, DApSub> ExprT;
  return DExpr<ExprT>(ExprT(DExprLiteral(x), a));
}

template <class A>
DExpr<DBinExprOp<DExpr<A>, DExprLiteral, DApSub>> operator-(const DExpr<A> &a,
                                                            double x) {
  typedef DBinExprOp<DExpr<A>, DExprLiteral, DApSub> ExprT;
  return DExpr<ExprT>(ExprT(a, DExprLiteral(x)));
}

template <class A>
DExpr<DBinExprOp<DExprLiteral, DExpr<A>, DApMultiply>>
operator*(double x, const DExpr<A> &a) {
  typedef DBinExprOp<DExprLiteral, DExpr<A>, DApMultiply> ExprT;
  return DExpr<ExprT>(ExprT(DExprLiteral(x), a));
}

template <class A>
DExpr<DBinExprOp<DExprLiteral, DExpr<A>, DApMultiply>>
operator*(const DExpr<A> &a, double x) {
  return x * a;
}

template <class A>
DExpr<DBinExprOp<DExprLiteral, DExpr<A>, DApDivide>>
operator/(double x, const DExpr<A> &a) {
  typedef DBinExprOp<DExprLiteral, DExpr<A>, DApDivide> ExprT;
  return DExpr<ExprT>(ExprT(DExprLiteral(x), a));
}

template <class A>
DExpr<DBinExprOp<DExpr<A>, DExprLiteral, DApDivide>>
operator/(const DExpr<A> &a, double x) {
  typedef DBinExprOp<DExpr<A>, DExprLiteral, DApDivide> ExprT;
  return DExpr<ExprT>(ExprT(a, DExprLiteral(x)));
}

template <class A, class B>
DExpr<DBinExprOp<DExpr<A>, DExpr<B>, DApAdd>> operator+(const DExpr<A> &a,
                                                        const DExpr<B> &b) {
  typedef DBinExprOp<DExpr<A>, DExpr<B>, DApAdd> ExprT;
  return DExpr<ExprT>(ExprT(a, b));
}

template <class A, class B>
DExpr<DBinExprOp<DExpr<A>, DExpr<B>, DApSub>> operator-(const DExpr<A> &a,
                                                        const DExpr<B> &b) {
  typedef DBinExprOp<DExpr<A>, DExpr<B>, DApSub> ExprT;
  return DExpr<ExprT>(ExprT(a, b));
}

template <class A, class B>
DExpr<DBinExprOp<DExpr<A>, DExpr<B>, DApMultiply>>
operator*(const DExpr<A> &a, const DExpr<B> &b) {
  typedef DBinExprOp<DExpr<A>, DExpr<B>, DApMultiply> ExprT;
  return DExpr<ExprT>(ExprT(a, b));
}

template <class A, class B>
DExpr<DBinExprOp<DExpr<A>, DExpr<B>, DApDivide>> operator/(const DExpr<A> &a,
                                                           const DExpr<B> &b) {
  typedef DBinExprOp<DExpr<A>, DExpr<B>, DApDivide> ExprT;
  return DExpr<ExprT>(ExprT(a, b));
}

template <typename A>
DExpr<DUniExprOp<DExpr<A>, DApSine>> sin(const DExpr<A> &a) {
  typedef DUniExprOp<DExpr<A>, DApSine> ExprT;
  return DExpr<ExprT>(ExprT(a));
}

template <typename A>
DExpr<DUniExprOp<DExpr<A>, DApCosine>> cos(const DExpr<A> &a) {
  typedef DUniExprOp<DExpr<A>, DApCosine> ExprT;
  return DExpr<ExprT>(ExprT(a));
}

template <class Expr>
void eval(DExpr<Expr> expr, double x) {
  std::cout << expr(x) << endl;
}

int main() {
  DPlaceholder x;
  eval(sin(x) * cos(x * 2.0 + 1.0), -6.28);
  return 0;
}
