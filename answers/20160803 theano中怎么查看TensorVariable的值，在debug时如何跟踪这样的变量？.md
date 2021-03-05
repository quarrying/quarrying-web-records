#! https://www.zhihu.com/question/49131386/answer/114660038

[comment]: <> (Answer URL: https://www.zhihu.com/question/49131386/answer/114660038)
[comment]: <> (Question Title: theano中怎么查看TensorVariable的值，在debug时如何跟踪这样的变量？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2016-08-03 00:39:08)

在Theano中，TensorConstant类型变量可以用value属性获取其值，TensorSharedVariable类型变量可以用get_value方法和set_value方法获取和设置其值，而TensorVariable类型变量是没有值的，无从获取，只能通过对这个变量进行赋值（evaluate）来取值。  

    
```python
>>> import theano
>>> import theano.tensor as T
>>> import numpy as np

>>> x = T.constant(1)
>>> type(x)
<class 'theano.tensor.var.TensorConstant'>
>>> x.value
array(1, dtype=int8)

>>> x = theano.shared(1)
>>> type(x)
<class 'theano.tensor.sharedvar.ScalarSharedVariable'>
>>> x.get_value()
array(1)
>>> x.set_value(np.array(2))
>>> x.get_value()
array(2)

>>> x = T.scalar()
>>> type(x)
<class 'theano.tensor.var.TensorVariable'>
>>> y = x ** 2
>>> y.eval({x:2})
array(4.0)
```

  
Theano是有名的难调试。至于如何在调试时观察TensorVariable变量，个人建议在创建TensorVariable时，为其赋以一个独特的名字，再配合以theano.pp打印。  

    
```python
>>> x = T.scalar()
>>> y = x ** 2
>>> print(x)
<TensorType(float64, scalar)>
>>> print(y)
Elemwise{pow,no_inplace}.0
>>> pp(x)
'<TensorType(float64, scalar)>'
>>> pp(y)
'(<TensorType(float64, scalar)> ** TensorConstant{2})'

>>> x = T.scalar('x')
>>> y = x ** 2
>>> print(x)
x
>>> print(y)
Elemwise{pow,no_inplace}.0
>>> pp(x)
'x'
>>> pp(y)
'(x ** TensorConstant{2})'
```

  
以上，希望回答对你有用。如有错误，还请各位指正！

