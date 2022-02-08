#! https://www.zhihu.com/question/403268066/answer/1301103401

[comment]: <> (Answer URL: https://www.zhihu.com/question/403268066/answer/1301103401)
[comment]: <> (Question Title: 为什么 总平方和\(SST\)=残差平方和\(SSE\)+回归平方和\(SSR\) ?)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2020-06-25 01:04:57)

设观测值  $\vec y = \left[ y_1;y_2; \cdots ;y_m \right]$  ,  $\bar y = {\vec
1}^T\vec y/m$  是观测值  $\vec y$  的各分量的均值,  $\hat{ \vec{y}}$  是观测值  $\vec y$
的估计值.

$TSS = \left\| {\vec y - \bar y\vec 1} \right\|_2^2$  . Total sum of squares
(TSS ) 亦被称为 SST.

$RSS = \left\| {\vec y - \hat{ \vec y}} \right\|_2^2$  . Residual sum of
squares (RSS) 亦被称为 the sum of squared errors of prediction (SSE).

$ESS = \left\| {\hat {\vec y} - \bar y\vec 1} \right\|_2^2$  . Explained sum
of squares (ESS) 亦被称为 the sum of squares due to regression (SSR).

$$\begin{aligned} TSS 
&= \left\| {\vec y - \bar y\vec 1} \right\|_2^2 = \left\| {\vec y - \hat {\vec y} + \hat {\vec y} - \bar y\vec 1} \right\|_2^2 \\
&= \left\| {\vec y - \hat {\vec y}} \right\|_2^2 + \left\| {\hat {\vec y} - \bar y\vec 1} \right\|_2^2 + 2\left\langle {\vec y - \hat {\vec y},\hat {\vec y} - \bar y\vec 1} \right\rangle \\
&= RSS + ESS + 2\left\langle {\vec y - \hat {\vec y},\hat {\vec y} - \bar y\vec 1} \right\rangle \\
&= RSS + ESS + 2\left( {{{\vec y}^T}\hat {\vec y} - {{\hat {\vec y}}^T}\hat {\vec y} - \bar y\left( {{{\vec y}^T}\vec 1 - {{\hat {\vec y}}^T}\vec 1} \right)} \right) \\
\end{aligned}$$

下面证明当  $\hat{ \vec y}$  是线性估计时,  $TSS = RSS + ESS$  .

线性回归问题:  $\hat {\vec \theta} = \arg {\min _{\vec \theta }}\sum\limits_{i =
1}^m {{{\left( {{y_i} - {{\vec \theta }^T}{{\vec x}_i}} \right)}^2}} = \arg
{\min _{\vec \theta }}{\left\| {\vec y - X\vec \theta } \right\|^2}$  , 式中
${\vec x_i} = \left[ {1;\vec x'_i} \right]$  为  $n+1$  维向量,  $i = 1,2, \cdots
,m$  ,  $X = \left[ {\vec x}_1^T;{\vec x}_2^T; \cdots ;{\vec x}_m^T \right]$
.

令  $J\left( {\vec \theta } \right) = \frac{1}{2}{\left\| {\vec y - X\vec
\theta } \right\|^2}$  , 求其梯度  $\frac{{\partial J\left( {\vec \theta }
\right)}}{{\partial \vec \theta }} = \frac{{\partial J\left( {\vec \theta }
\right)}}{{\partial \left( {\vec y - X\vec \theta } \right)}}\frac{{\partial
\left( {\vec y - X\vec \theta } \right)}}{{\partial \vec \theta }} = - {\left(
{\vec y - X\vec \theta } \right)^T}X$  .

所以  ${X^T}\left( {\vec y - X\hat {\vec \theta} } \right) = {X^T}\vec y -
{X^T}X\hat {\vec \theta} = \vec 0 \Rightarrow \hat {\vec \theta} = {\left(
{{X^T}X} \right)^{ - 1}}{X^T}\vec y$  ,

于是  $\hat {\vec y} = X\hat {\vec \theta} = X{\left( {{X^T}X} \right)^{ -
1}}{X^T}\vec y$  , 将其代入  ${\vec y^T}\hat {\vec y}$  和  $\hat {\vec y^T}\hat
{\vec y}$  , 可得:

$${\vec y^T}\hat {\vec y} = {\vec y^T}X{\left( {{X^T}X} \right)^{ -
1}}{X^T}\vec y$$

$$\begin{aligned} {{\hat {\vec y}}^T}\hat {\vec y} &= {\left( {X{{\left(
{{X^T}X} \right)}^{ - 1}}{X^T}\vec y} \right)^T}X{\left( {{X^T}X} \right)^{ -
1}}{X^T}\vec y \\\ &= {{\vec y}^T}X{\left( {{X^T}X} \right)^{ -
T}}{X^T}X{\left( {{X^T}X} \right)^{ - 1}}{X^T}\vec y \\\ &= {{\vec
y}^T}X{\left( {{X^T}X} \right)^{ - 1}}{X^T}\vec y \\\ \end{aligned}$$

可见  ${\vec y^T}\hat {\vec y} - {\hat {\vec y}^T}\hat {\vec y} = 0$  .

另外又因为  ${X^T}\vec y - {X^T}X\hat {\vec \theta} = \vec 0 \Rightarrow {X^T}\vec
y - {X^T}\hat {\vec y} = \vec 0$  , 而  $X$  的第一列全为1, 即  $X^T$  的第一行全为1, 所以
${\vec 1^T}\vec y - {\vec 1^T}\hat {\vec y} = 0$  .

综上  ${\vec y^T}\hat {\vec y} - {\hat {\vec y}^T}\hat {\vec y} - \bar y\left(
{{{\vec y}^T}\vec 1 - {{\hat {\vec y}}^T}\vec 1} \right) = 0$  , 即  $TSS = RSS + ESS$  .

不妨用下面的代码验证一下:

```python
import numpy as np

def calc_tss(y):
    y_bar = np.mean(y)
    return np.sum((y - y_bar)**2)
    
def calc_rss_and_ess(y):
    num_samples = len(y)
    
    # 构造一个随机的设计矩阵 (design matrix)
    feature_dim = 3
    x = np.random.randn(num_samples, feature_dim)
    x[:, 0] = 1
    
    results = np.linalg.lstsq(x, y)
    y_hat = np.sum(x * results[0], axis=1)
    y_bar = np.mean(y)
    rss = np.sum((y - y_hat)**2)
    ess = np.sum((y_hat - y_bar)**2)
    return rss, ess
    
if __name__ == '__main__':
    num_samples = 100
    y = np.random.randn(num_samples)
    tss = calc_tss(y)
    rss, ess = calc_rss_and_ess(y)
    print(tss, rss, ess, np.allclose(tss, rss + ess))
```

上面的证明看起来有点复杂, 如果大家有更简单的证明, 欢迎回复.

