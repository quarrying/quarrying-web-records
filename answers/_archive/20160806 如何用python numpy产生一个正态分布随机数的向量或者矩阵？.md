#! https://www.zhihu.com/question/39823283/answer/115241445

[comment]: <> (Answer URL: https://www.zhihu.com/question/39823283/answer/115241445)
[comment]: <> (Question Title: 如何用python numpy产生一个正态分布随机数的向量或者矩阵？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2016-08-06 01:05:12)

一般的正态分布可以通过标准正态分布配合数学期望向量和协方差矩阵得到。如下代码，可以得到满足一维和二维正态分布的样本。希望有用，如有错误，欢迎指正！  

    
```python
import numpy as np
from numpy.linalg import cholesky
import matplotlib.pyplot as plt

sampleNo = 1000;
# 一维正态分布
# 下面三种方式是等效的
mu = 3
sigma = 0.1
np.random.seed(0)
s = np.random.normal(mu, sigma, sampleNo )
plt.subplot(141)
plt.hist(s, 30, normed=True)

np.random.seed(0)
s = sigma * np.random.randn(sampleNo ) + mu
plt.subplot(142)
plt.hist(s, 30, normed=True)

np.random.seed(0)
s = sigma * np.random.standard_normal(sampleNo ) + mu
plt.subplot(143)
plt.hist(s, 30, normed=True)

# 二维正态分布
mu = np.array([[1, 5]])
Sigma = np.array([[1, 0.5], [1.5, 3]])
R = cholesky(Sigma)
s = np.dot(np.random.randn(sampleNo, 2), R) + mu
plt.subplot(144)
# 注意绘制的是散点图，而不是直方图
plt.plot(s[:,0],s[:,1],'+')
plt.show()
```

  
![](https://pic4.zhimg.com/50/3275aace2c66dcc10d91a1bccb89aa71_hd.jpg?source=1940ef5c)

