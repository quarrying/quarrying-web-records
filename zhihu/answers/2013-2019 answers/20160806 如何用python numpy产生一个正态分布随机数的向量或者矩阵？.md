#! https://www.zhihu.com/question/39823283/answer/115241445

[comment]: <> (Answer URL: https://www.zhihu.com/question/39823283/answer/115241445)
[comment]: <> (Question Title: 如何用python numpy产生一个正态分布随机数的向量或者矩阵？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2016-08-06 01:05:12)

感谢 [@漠漠上寒](https://www.zhihu.com/people/guo-yong-zhi-24-48) 指出原回答的错误, 特此更新一次答案.

先引入一些有用的数学结论:

若 $X \sim N(\mu, \sigma^2)$, $Y = a X + d$, 则 $Y \sim N(a\mu + d, d^2\sigma^2)$

若 $\vec{X} \sim N(\vec{\mu}, \Sigma)$, $\vec{Y} = A \vec{X} + \vec{d}$, 则 $\vec{Y} \sim N(A\vec{\mu} + \vec{d}, A \Sigma A^T)$.

特别地,

若 $X \sim N(0, 1)$, $Y = \mu X + \sigma$, 则 $Y \sim N(\mu, \sigma^2)$

若 $\vec{X} \sim N(\vec{0}, I)$, $\vec{Y} = L \vec{X} + \vec{\mu}$, 则 $\vec{Y} \sim N(\vec{\mu}, L L^T)$.

在 NumPy 中可以:
1) 直接使用 `np.random.normal` 生成一组符合一维正态分布的标量; 直接使用 `np.random.multivariate_normal` 生成一组符合一维或多维正态分布的向量.
2) 先用 `np.random.randn` (或 `np.random.standard_normal`) 生成一组符合一维或多维的标准正态分布的标量或向量, 再利用上面的结论.

## 测试代码
```python
import numpy as np
import matplotlib.pyplot as plt


def verify_mu_and_cov(mu, cov, x):
    print('mu_true: {}'.format(mu))
    print('mu_calc: {}'.format(np.mean(x, axis=0)))
    print('Sigma_true: \n{}'.format(cov))
    print('Sigma_calc: \n{}'.format(np.cov(x, rowvar=False, ddof=0)))
    print('Sigma_calc: \n{}'.format(np.cov(x, rowvar=False, ddof=1)))
    print('=======================')
    

if __name__ == '__main__':
    num_samples = 1000

    # 一维正态分布, 绘制直方图
    mu = 3
    sigma = 0.1

    x = np.random.normal(mu, sigma, num_samples)
    verify_mu_and_cov(mu, sigma**2, x)
    plt.subplot(121)
    plt.hist(x, 30, histtype='step', density=True)
    x = sigma * np.random.randn(num_samples) + mu
    verify_mu_and_cov(mu, sigma**2, x)
    plt.hist(x, 30, histtype='step', density=True)

    # 二维正态分布, 绘制散点图
    mu = np.array([1, 5])
    Sigma = np.array([[1, 0.5], [1.5, 3]]) # 需为半正定矩阵
    Sigma = 0.5 * (Sigma + Sigma.T)        # 使之成为对称阵
    L = np.linalg.cholesky(Sigma)          # Sigma = L*L^T

    x = np.random.multivariate_normal(mu, Sigma, num_samples)
    verify_mu_and_cov(mu, Sigma, x)
    plt.subplot(122)
    plt.plot(x[:,0], x[:,1], '+')
    x = np.dot(np.random.randn(num_samples, 2), L.T) + mu
    verify_mu_and_cov(mu, Sigma, x)
    plt.plot(x[:,0], x[:,1], '+')
    plt.show()
```
显示图形:

![一维和二维正态分布](https://pic4.zhimg.com/80/v2-9fd730d02ed4e1afa1a4d5c1ec014bc1.png)

----
- 20160806 发布答案
- 20211202 修改答案

