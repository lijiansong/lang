#ifndef _MATHUTILS_HPP_
#define _MATHUTILS_HPP_

#include <cmath>
#include <cstdint>
#include <functional>

///
/// @brief Contains fundamental type defintions used by the project.
///
namespace MathUtils {
namespace Base {

/// Mathematical function of type double
/// @see https://caiorss.github.io/C-Cpp-Notes/Doxygen-documentation.html
using MathFunc = std::function<double(double)>;

/// Generic math function
/// @tparam T Any float-point type such as float, double or long double
template <class T> using MathFuncGen = std::function<T(T)>;

/// @brief Mathematical error code
enum class MathErrorCode : std::uint32_t {
  /// Bit 0 (value 0x00 or 0) not set => Means no error
  E_OK = 0x00,
  /// bit 0 (value 0x01 or 1) means that an error of any type happened
  E_ERROR = 0x01,
  /// bit 1 (value 0x02 or 2) Overflow error
  E_OVERFLOW = 0x02,
  /// bit 2 (value 0x04 or 4) Undeflow error
  E_UNDERFLOW = 0x04,
  /// bit 3 (value 0x08 or 8) Not a number
  E_NAN = 0x08,
  /// bit 4 (value 0x10 or 16) Root, series or algorithm result doesn't
  /// converge.
  E_CONVERGENCE = 0x10,
  /// bit 5  (value 0x20 or 16) Maximum iterations reached
  E_MAX_ITER = 0x20
};

/// @brief Represents a math numerical result with an error code.
/// @see   MathErrorCode
///
struct MathResult {
  /// Computation result
  double result;
  ///  Error code => 0 (Success), other than zero means error.
  /// @see MathErrorCode
  ///
  ErrorCodecode error_code;
};
} // namespace Base
} // namespace MathUtils

/** @brief Contains non-linear equations solvers */
namespace MathUtils::Solvers {
// Note: Nested namespaces are only available in C++17.
using namespace MathUtils::Base;

///
/// @brief Solves non-linear equation with Newton method.
///
/// @details
///  Solves a non-linear equation using the Newton method which uses the
///  function and its derivate function for finding a suitable approximation
///  to the equation root.
///
/// @see   MathUtils::Base::MathFunc
/// @see   https://en.wikipedia.org/wiki/Newton%27s_method
/// @todo  Implement unit test with lots of test cases.
///
/// @param fun  Non-linear function f(x)
/// @param dfun Derivative of non-linear function df(x) = d/dx f(x)
/// @param x0   Initial guess
/// @param eps  Tolerance for stopping criteria.
/// @return     Equation result object containing result and error code.
///
MathResult NewtonSolver(MathFunc fun, MathFunc dfun, double x0, double eps);

///  @brief Solves non-linear equation with Newton method.
///
///  @tparam T   Any float-point type such as float, double or long double
///  @param fun  Non-linear function f(x)
///  @param dfun Derivative of non-linear function df(x) = d/dx f(x)
///  @param x0   Initial guess
///  @param eps  Tolerance for stopping criteria.
///  @return     Equation result as a float point type T.
///
///  @details
///  Solves non-linear equation using Newton method. This function needs two
///  functions, the function to be solved @p fun and its derivate @p dfun
///
///  @note     The function f(x) must be continues and differentiable.
///  @warning  Throws NonCoverge exception when the root is not found.
///
///  @see NewtonSolver
///  @see https://en.wikipedia.org/wiki/Newton%27s_method
///
///  Example:
///  @code
///    // Solve f(x) = x^2 - 25.0 , df(x) = 2x around x0 = 10.0
///    auto fun = [](double x){ return x * x -  25.0 };
///    auto dfun = [](double x){ return 2 * x; }
///
///    double root = GenericNewtonsolver(fun, dfun, 10.0, 0.001);
///    std::cout << "Root = " << root << std::endl;
///  @endcode
///
template <typename T>
auto GenericNewtonSolver(MathFuncGen<T> fun, MathFuncGen<T> dfun, T x0, T eps)
    -> T;

/** @brief Clear chart screen.
 *  @return Void
 */
void clear_screen();

} // namespace MathUtils::Solvers

namespace MathUtils {

/// @brief Class for plotting cuves, equations and differential equations.
/// @author Ghost Author
class XYChart {
public:
  /// @brief Construct plot object with a given dimension.
  ///
  /// @pre The chart size must not be negative.
  ///
  /// @param width  Initial XYChart width
  /// @param height Initial XYChart length
  ///
  XYChart(double width, double length);

  /// Class destructor
  virtual ~XYChart() = default;

  /// @brief Clear chart
  /// @details Clear all drawings and plots in the chart area.
  virtual void clear();

  /// @brief Add curve x[i], y[i] to chart
  ///
  /// @pre  Precondition: the arrays x[] and y[] must have size n.
  /// @post There are no post conditions.
  ///
  /// @param n  array size
  /// @param x  array of x-coordinates values
  /// @param y  array of y-coordinates values
  /// @return   Void
  ///
  /// @details
  /// Plot the curve compriseds of points P[i] = (X[i], Y[i]),
  /// where i = 0, 1, 2... n - 1.
  ///
  void addCurve(size_t n, const double x[], const double y[]);

  /// Copy constructor
  XYChart(Plotter const &) = delete;
  /// Copy-assignment operator
  XYChart &operator=(XYChart const &) = delete;

private:
};

} // namespace MathUtils

/**  @brief C++ implementation of Fotran BLAS daxypy
     Computes the equation ys[i] <- xs[i] * alpha + beta

     @note Function with C-linkage.

     @param[in]      n      Array size. Size of xs and ys
     @param[in]      xs     Input  array xs
     @param[in, out] ys     Output array ys
     @param[in]      alpha  Linear coefficient
     @Return         Void
  */
extern "C" auto daxpy(size_t n, double const *xs, double *ys, double alpha,
                      double beta) -> void;

#endif
