#! https://www.zhihu.com/question/444458765/answer/1741163043

[comment]: <> (Answer URL: https://www.zhihu.com/question/444458765/answer/1741163043)
[comment]: <> (Question Title: OpenCV模式匹配中的ccorr是什么的缩写？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2021-02-21 11:49:15)

 
设待匹配图像为  $I(\vec x)$, 模板图像为 $T(\vec x)$, $\Omega$ 表示模板图像的定义域, 即 $\Omega = \operatorname{dom} T \subseteq \operatorname{dom} I$ . 为了简洁, 下面采用积分和多元函数的形式来列写公式, 二维离散形式的公式可以参考 [[1][]] (注意两者符号标记有差异). 注: 笔者注的地方是答主的看法, 未必正确, 仅供参考.

##  TM_SQDIFF

SQDIFF 的全称为 Sum of Squared Difference (SSD), 意即差的平方和.

$$E\left( {\vec d} \right) = \int_\Omega {{{\left| {I\left( {\vec x + \vec d}
\right) - T\left( {\vec x} \right)} \right|}^2}d\vec x}$$

##  TM_SQDIFF_NORMED

SQDIFF_NORMED 的全称为 Normalized Sum of Squared Difference, 意即归一化差的平方和.

$$E\left( {\vec d} \right) = \frac{{\int_\Omega {{{\left| {I\left( {\vec x +
\vec d} \right) - T\left( {\vec x} \right)} \right|}^2}d\vec x} }}{{\sqrt
{\left( {\int_\Omega {{I^2}\left( {\vec x + \vec d} \right)d\vec x} }
\right)\left( {\int_\Omega {{T^2}\left( {\vec x} \right)d\vec x} } \right)}
}}$$

补充一个: 平均平方误差或均方误差（Mean Squared Difference, MSD 或 Mean Squared Error, MSE).

$$E\left( {\vec d} \right) = \frac{1}{{\left| \Omega \right|}}\int_\Omega
{{{\left| {I\left( {\vec x + \vec d} \right) - T\left( {\vec x} \right)}
\right|}^2}d\vec x}$$

##  TM_CCORR

CCORR 的全称为 Cross Correlation, 意即互相关.

$$E\left( {\vec d} \right) = \int_\Omega {I\left( {\vec x + \vec d}
\right)T\left( {\vec x} \right)d\vec x}$$

##  TM_CCORR_NORMED

CCORR_NORMED 的全称为 Normalized Cross Correlation (NCC), 意即归一化互相关.

$$E\left( {\vec d} \right) = \frac{{\int_\Omega {I\left( {\vec x + \vec d}
\right)T\left( {\vec x} \right)d\vec x} }}{{\sqrt {\left( {\int_\Omega
{{I^2}\left( {\vec x + \vec d} \right)d\vec x} } \right)\left( {\int_\Omega
{{T^2}\left( {\vec x} \right)d\vec x} } \right)} }}$$

##  TM_CCOEFF

CCOEFF 的全称为 Correlation Coefficient, 意即相关系数. 笔者注: 相关系数即零均值互相关 (Zero-mean Cross Correlation; ZCC).

$$E\left( {\vec d} \right) = \int_\Omega {\left( {I\left( {\vec x + \vec d}
\right) - {{\bar I}_{\vec d}}} \right)\left( {T\left( {\vec x} \right) - \bar
T} \right)d\vec x}$$

其中  $\bar T = \frac{1}{{\left| \Omega \right|}}\int_\Omega {T\left( {\vec x} \right)d\vec x}$  和  ${\bar I_{\vec d}} = \frac{1}{{\left| \Omega \right|}}\int_\Omega {I\left( {\vec x + \vec d} \right)d\vec x}$  .

##  TM_CCOEFF_NORMED

CCOEFF_NORMED 的全称为 Normalized Correlation Coefficient, 意即归一化相关系数. 笔者注: 归一化相关系数即零均值归一化互相关 (Zero-mean Normalized Cross Correlation; ZNCC), ZNCC 也可以简称为 NCC.

$$E\left( {\vec d} \right) = \frac{{\int_\Omega {\left( {I\left( {\vec x +
\vec d} \right) - {{\bar I}_{\vec d}}} \right)\left( {T\left( {\vec x} \right)
- \bar T} \right)d\vec x} }}{{\sqrt {\left( {\int_\Omega {{{\left| {I\left(
{\vec x + \vec d} \right) - {{\bar I}_{\vec d}}} \right|}^2}d\vec x} }
\right)\left( {\int_\Omega {{{\left| {T\left( {\vec x} \right) - \bar T}
\right|}^2}d\vec x} } \right)} }}$$

[1]: https://docs.opencv.org/4.0.1/df/dfb/group__imgproc__object.html
