#! https://www.zhihu.com/question/49571479/answer/116840869

[comment]: <> (Answer URL: https://www.zhihu.com/question/49571479/answer/116840869)
[comment]: <> (Question Title: 在numpy中如何合并不同维数的array？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2016-08-14 22:00:36)

在NumPy中可以利用如下的函数进行数组或矩阵的连接：

- hstack : Stack arrays in sequence horizontally (column wise).
- vstack : Stack arrays in sequence vertically (row wise).
- dstack : Stack arrays in sequence depth wise (along third axis).
- concatenate : Join a sequence of arrays together.
- r_ : Translates slice objects to concatenation along the first axis.
- c_ : Translates slice objects to concatenation along the second axis.

题主需要的是在第三维（或轴）上的连接，见如下的代码：

    
```python
#coding=utf-8
import numpy as np

# 因为是生成随机数做测试，设置固定随机数种子，可以保证每次结果一致
np.random.seed(0) 
RGB = np.random.randint(0, 255, (5, 5, 3))
alpha = np.random.randint(0, 255, (5, 5))
RGBA = np.dstack((RGB, alpha))
print('RGB = \n {}'.format(RGB))
print('alpha = \n {}'.format(alpha))
print('RGBA = \n {}'.format(RGBA))
print('RGBA[:, :, 3] = \n {}'.format(RGBA[: ,:, 3]))
```

