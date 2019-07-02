# Tensor Contraction

```
tf.tensordot(
    a,
    b,
    axes,
    name=None
)
```

Tensor contraction of a and b along specified axes.

Tensordot (also known as tensor contraction) sums the product of elements from `a` and `b` over the indices specified by `a_axes` and `b_axes`.

The lists `a_axes` and `b_axes` specify those pairs of axes along which to contract the tensors. The axis `a_axes[i]` of `a` must have the same dimension as axis `b_axes[i]` of `b` for all `i` in `range(0, len(a_axes))`.

The lists `a_axes` and `b_axes` must have identical length and consist of unique integers that specify valid axes for each of the tensors.

Example 1: When a and b are matrices (order 2), the case axes = 1 is equivalent to matrix multiplication.

Example 2: When `a` and `b` are matrices (order 2), the case `axes = [[1], [0]]` is equivalent to matrix multiplication.

Example 3: Suppose that \\(a_{ijk}\\) and \\(b_{lmn}\\) represent two
  tensors of order 3. Then, `contract(a, b, [[0], [2]])` is the order 4 tensor
  \\(c_{jklm}\\) whose entry
  corresponding to the indices \\((j,k,l,m)\\) is given by:

  \\( c_{jklm} = \sum_i a_{ijk} b_{lmi} \\).

In general, `order(c) = order(a) + order(b) - 2*len(axes[0])`.


## REF

- TensorFlow API docs: <https://www.tensorflow.org/api_docs/python/tf/tensordot>
- TensorFlow GitHub repo: <https://github.com/tensorflow/tensorflow/blob/r1.14/tensorflow/python/ops/math_ops.py>
