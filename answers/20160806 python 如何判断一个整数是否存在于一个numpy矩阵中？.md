#! https://www.zhihu.com/question/28550627/answer/115383425

[comment]: <> (Answer URL: https://www.zhihu.com/question/28550627/answer/115383425)
[comment]: <> (Question Title: python 如何判断一个整数是否存在于一个numpy矩阵中？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2016-08-06 21:55:46)

前面已经有人回答过，使用关键词in可以判断一个元素是否在数组或矩阵内，答主这里补充一下，在NumPy中如何获取某个元素在数组或矩阵中的索引（index）。  

    
```python
>>> l = [0, 1, 2, 3, 1]
# 判断一个项目是否在 list 内
>>> l in l
False
>>> 0 in l
True
>>> 4 in l
False

# 回顾一下 list 的 index
# tuple, str 也有 index 方法
# return first index of value.
>>> [0, 1, 2, 3, 1].index(1)
1
# Raises ValueError if the value is not present.
>>> [0, 1, 2, 3, 1].index(5)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: 5 is not in list

# 创建测试数组和矩阵
>>> import numpy as np
>>> a = np.arange(10).reshape((2, 5))
>>> a[1, 0] = 2
>>> m = np.mat(a)
>>> a
array([[0, 1, 2, 3, 4],
        [2, 6, 7, 8, 9]])
>>> m
matrix([[0, 1, 2, 3, 4],
        [2, 6, 7, 8, 9]])
    
# 判断一个元素是否在数组和矩阵内
>>> 9 in a
True
>>> 9 in m
True
>>> 10 in a
False
>>> 10 in m
False
# 判断一行元素是否在数组和矩阵内
>>> [0, 1, 2, 3, 4] in a
True
>>> [0, 1, 2, 3, 4] in m
True
# 判断一列元素是否在数组和矩阵内
>>> [1, 6] in a
False
>>> [1, 6] in m
False
>>> [1, 6] in a.T
True
>>> [1, 6] in m.T
True
# 比较朴素的结论
>>> a in a
True

# 返回满足某个条件的所有元素的索引
# 具体使用方法可以 help(np.where) 或 help(np.nonzero)
>>> np.where(a == 2)
(array([0, 1], dtype=int64), array([2, 0], dtype=int64))
>>> np.where(m == 2)
(matrix([[0, 1]], dtype=int64), matrix([[2, 0]], dtype=int64))
>>> np.nonzero(a == 2)
(array([0, 1], dtype=int64), array([2, 0], dtype=int64))
>>> np.nonzero(m == 2)
(matrix([[0, 1]], dtype=int64), matrix([[2, 0]], dtype=int64))
>>> np.where(a == 10)
(array([], dtype=int64), array([], dtype=int64))
>>> np.where(m == 10)
(matrix([], shape=(1L, 0L), dtype=int64), matrix([], shape=(1L, 0L), dtype=int64))
```

