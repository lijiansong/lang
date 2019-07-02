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

This operation corresponds to `numpy.tensordot(a, b, axes)`.

Example 1: When a and b are matrices (order 2), the case axes = 1 is equivalent to matrix multiplication.

Example 2: When `a` and `b` are matrices (order 2), the case `axes = [[1], [0]]` is equivalent to matrix multiplication.

Example 3: Suppose that \\(a_{ijk}\\) and \\(b_{lmn}\\) represent two
  tensors of order 3. Then, `contract(a, b, [[0], [2]])` is the order 4 tensor
  \\(c_{jklm}\\) whose entry
  corresponding to the indices \\((j,k,l,m)\\) is given by:

  \\( c_{jklm} = \sum_i a_{ijk} b_{lmi} \\).

In general, `order(c) = order(a) + order(b) - 2*len(axes[0])`.

```
张量的`缩并运算`就是所谓的tensor contraction, 这是矩阵乘法的推广,可以理解成张量的乘法.

给定两个张量,如果它们有某些维度的长度相同,就可以在相应的维度上进行类似于内积的运算,然后以余下的维度构成一个新的张量,这就是tensor contraction
向量和矩阵都是低阶的张量（一般来讲向量是1阶的,矩阵是2阶的）, 比如说m*k的张量（矩阵）A和k*n的张量（也是矩阵）B的在维度k方向上进行缩并,就相当于A*B这样的运算,得到m*n的张量.

对于高阶的张量而言, 可以同时在多个维度上缩并,比如k1*k2*k3的张量A和k2*k3*k4的张量B,可以在k2维度上缩并得到k1*k3*k4的张量,也可以在k3维度上缩并得到k1*k2*k4的张量,还可以在k2和k3的维度上同时缩并得到k1*k4的张量,具体用哪个维度由实际的问题所决定.

```


## REF

- TensorFlow API docs: <https://www.tensorflow.org/api_docs/python/tf/tensordot>
- TensorFlow GitHub repo: <https://github.com/tensorflow/tensorflow/blob/r1.14/tensorflow/python/ops/math_ops.py>
- Numpy tensor dot API docs: <https://docs.scipy.org/doc/numpy/reference/generated/numpy.tensordot.html>
- 矩阵张量点积的图形化表达: <https://liwt31.github.io/2018/01/22/graphical_matrix/>
- Tensor dot blog: <https://www.machenxiao.com/blog/tensordot>
