#! https://www.zhihu.com/question/50139392/answer/119762057

[comment]: <> (Answer URL: https://www.zhihu.com/question/50139392/answer/119762057)
[comment]: <> (Question Title: 求教theano中基础教程中Jacobian和Hessian矩阵部分的一些问题?)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2016-08-30 23:33:51)

`T.sum(x**2)` 的意思很好理解，就是 TensorVariable 各元素平方之和。显然地，对于向量而言，`T.sum(x**2)` 等于向量L2范数的平方，对于矩阵而言，`T.sum(x**2)` 等于矩阵F范数的平方。测试代码如下：  

    
```python
#coding=utf-8
import numpy as np
import theano.tensor as T
from theano import function

x = T.vector('x')
f = function([x], T.sum(x ** 2))
f2 = function([x], x.norm(2) ** 2)
x_np = np.random.rand(10)
print(f(x_np))
print(f2(x_np))
print(np.sum(x_np ** 2))
print(np.linalg.norm(x_np, 2) ** 2)

X = T.matrix('X')
f = function([X], T.sum(X ** 2))
f2 = function([X], X.norm(2) ** 2)
X_np = np.random.rand(10, 10)
print(f(X_np))
print(f2(X_np))
print(np.sum(X_np ** 2))
print(np.linalg.norm(X_np, 'fro') ** 2)
```

  
关于Rop和Lop，题主提供的链接中已经说的很清楚了，引用如下：  

> The R operator is built to evaluate the product between a Jacobian and a
> vector, namely  $\frac{\partial f(x)}{\partial x} v$  . The formulation can
> be extended even for x being a matrix, or a tensor in general, case in which
> also the Jacobian becomes a tensor and the product becomes some kind of
> tensor product.  
>  In similitude to the R-operator, the L-operator would compute a row vector
> times the Jacobian. The mathematical formula would be  $v \frac{\partial
> f(x)}{\partial x}$  . The L-operator is also supported for generic tensors
> (not only for vectors).

原链接提供的例子难以理解的原因可能是例子中是对矩阵进行求导，我写了一段代码，希望可以有助于理解。  

    
```python
#coding=utf-8
import theano
import theano.tensor as T
import numpy as np

W = T.dmatrix('W')
V = T.dmatrix('V')
x = T.dvector('x')
y = T.dot(x, W)
f = theano.function([W, x, V], T.tensordot(T.jacobian(y, W),V))
g = theano.function([W, x, V], T.Rop(y, W, V))

W = np.array([[1, 1], [1, 1]])
V = np.array([[3, 2], [2, 2]])
x = np.array([2, 1])
print(f(W, x, V))
print(g(W, x, V))

W = T.dmatrix('W')
v = T.dvector('v')
x = T.dvector('x')
y = T.dot(x, W)
f = theano.function([W, x, v], T.tensordot(v, T.jacobian(y, W), 1))
g = theano.function([v, x], T.Lop(y, W, v))
h = theano.function([W, x, v], T.Lop(y, W, v),  on_unused_input='ignore')

W = np.array([[1, 1], [1, 1]])
v = np.array([2, 2])
x = np.array([2, 1])
print(f(W, x, v))
print(g(v, x))
print(h(W, x, v))
```

