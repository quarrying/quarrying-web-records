#! https://zhuanlan.zhihu.com/p/147901986

# softmax函数和softmax交叉熵损失函数的梯度
softmax 函数和 softmax 交叉熵损失函数是机器学习中常见的函数，本文不打算对它们进行详细的叙述，而只是利用矩阵微积分的方式来推导它们的梯度（网上的很多推导都是分情况的计算梯度或Jacobi矩阵的某个分量）。公式虽然多了点，但相信大家看了肯定会有收获的。

##  **符号约定**

在行文之前，先做一些符号约定。

$I$，单位矩阵。

$\vec{1}$，全1向量。

$1\{{\cdot}\}$，指示函数，在  $\cdot$  为真或假时分别取值1,0。

$\left[ {{x_1};{x_2}; \cdots ;{x_n}} \right]$  ，列向量。

$\left[ {{x_1},{x_2}, \cdots ,{x_n}} \right]$  ，行向量。

$\operatorname{diag} \left( {\vec x} \right)$  ，对角矩阵，其对角线元素为  $\vec{x}$  。

${f^ \circ }\left( \cdot \right)$  ，按元素函数。例如  ${\exp ^ \circ }\left( {\vec x} \right) = \left[ {\exp \left( {{x_1}} \right);\exp \left( {{x_2}} \right); \cdots ;\exp \left( {{x_n}} \right)} \right]$  。

##  **微分法则**

1）  $dA = 0$  ，其中矩阵  $A$  不是  $X$  的函数。

2）  $d\left( {aX} \right) = adX$  ，其中标量  $a$  不是  $X$  的函数。

3）和法则（sum rule）：  $d\left( {X + Y} \right) = dX + dY$  。

由2）和3）可见，微分算子是线性算子。

4）乘积法则（product rule）：  $d\left( {XY} \right) = \left( {dX} \right)Y + X\left( {dY} \right)$  。

这些微分法则在下面的梯度推导中均有用到。

##  **softmax函数的梯度**

softmax 函数定义为：

$$\operatorname{softmax} \left( {\vec x} \right) = \frac{{\left[ {\exp \left(
{{x_1}} \right); \cdots ;\exp \left( {{x_n}} \right)}
\right]}}{{\sum\nolimits_{i = 1}^n {\exp \left( {{x_i}} \right)} }} =
\frac{{{{\exp }^ \circ }\left( {\vec x} \right)}}{{{{\vec 1}^T}{{\exp }^ \circ
}\left( {\vec x} \right)}}$$

softmax 函数的梯度：  $\nabla \operatorname{softmax} \left( {\vec x} \right) =
\operatorname{diag} \left( {\operatorname{softmax} \left( {\vec x} \right)}
\right) - \operatorname{softmax} \left( {\vec x}
\right){\operatorname{softmax} ^T}\left( {\vec x} \right)$

证明如下：

由乘积法则可得：  $d\frac{{{{\exp }^ \circ }\left( {\vec x} \right)}}{{{{\vec
1}^T}{{\exp }^ \circ }\left( {\vec x} \right)}} = \frac{{d{{\exp }^ \circ
}\left( {\vec x} \right)}}{{{{\vec 1}^T}{{\exp }^ \circ }\left( {\vec x}
\right)}} + {\exp ^ \circ }\left( {\vec x} \right)d\frac{1}{{{{\vec
1}^T}{{\exp }^ \circ }\left( {\vec x} \right)}}$

易证  $d{\exp ^ \circ }\left( {\vec x} \right) = \operatorname{diag} \left({{{\exp }^ \circ }\left( {\vec x} \right)} \right)d\vec x$  （根据定义直接计算）。

$$\begin{gathered} d\frac{1}{{{{\vec 1}^T}{{\exp }^ \circ }\left( {\vec x}
\right)}} = - \frac{{d{{\vec 1}^T}{{\exp }^ \circ }\left( {\vec x}
\right)}}{{{{\left( {{{\vec 1}^T}{{\exp }^ \circ }\left( {\vec x} \right)}
\right)}^2}}} = - \frac{{{{\vec 1}^T}d{{\exp }^ \circ }\left( {\vec x}
\right)}}{{{{\left( {{{\vec 1}^T}{{\exp }^ \circ }\left( {\vec x} \right)}
\right)}^2}}} \\ = - \frac{{{{\vec 1}^T}\operatorname{diag} \left( {{{\exp }^
\circ }\left( {\vec x} \right)} \right)d\vec x}}{{{{\left( {{{\vec 1}^T}{{\exp
}^ \circ }\left( {\vec x} \right)} \right)}^2}}} \\ 
\end{gathered}$$

因为  ${\vec b^T}\operatorname{diag} \left( {\vec a} \right) = {\vec b^T} \circ {\vec a^T}$  （  $\circ$  表示Hadamard积，这个性质感兴趣的朋友可以自己推导一下），所以  ${\vec 1^T}\operatorname{diag} \left( {{{\exp }^ \circ }\left( {\vec x} \right)} \right) = {\vec 1^T} \circ {\exp ^{ \circ T}}\left( {\vec x} \right) = {\exp^{ \circ T}}\left( {\vec x} \right)$  ，于是

$d\frac{1}{{{{\vec 1}^T}{{\exp }^ \circ }\left( {\vec x} \right)}} = -
\frac{{{{\exp }^{ \circ T}}\left( {\vec x} \right)d\vec x}}{{{{\left( {{{\vec
1}^T}{{\exp }^ \circ }\left( {\vec x} \right)} \right)}^2}}}$  。

综上  $d\frac{{{{\exp }^ \circ }\left( {\vec x} \right)}}{{{{\vec 1}^T}{{\exp }^
\circ }\left( {\vec x} \right)}} = \left[ {\frac{{\operatorname{diag} \left(
{{{\exp }^ \circ }\left( {\vec x} \right)} \right)}}{{{{\vec 1}^T}{{\exp }^
\circ }\left( {\vec x} \right)}} - \frac{{{{\exp }^ \circ }\left( {\vec x}
\right){{\exp }^{ \circ T}}\left( {\vec x} \right)}}{{{{\left( {{{\vec
1}^T}{{\exp }^ \circ }\left( {\vec x} \right)} \right)}^2}}}} \right]d\vec x$
。所以

$$\begin{aligned} 
\nabla \operatorname{softmax} \left( {\vec x} \right) &=
\frac{{\operatorname{diag} \left( {{{\exp }^ \circ }\left( {\vec x} \right)}
\right)}}{{{{\vec 1}^T}{{\exp }^ \circ }\left( {\vec x} \right)}} -
\frac{{{{\exp }^ \circ }\left( {\vec x} \right){{\exp }^{ \circ T}}\left(
{\vec x} \right)}}{{{{\left( {{{\vec 1}^T}{{\exp }^ \circ }\left( {\vec x}
\right)} \right)}^2}}} \\ &= \operatorname{diag} \left(
{\operatorname{softmax} \left( {\vec x} \right)} \right) -
\operatorname{softmax} \left( {\vec x} \right){\operatorname{softmax}
^T}\left( {\vec x} \right) \\ 
\end{aligned}$$

##  softmax交叉熵损失函数的梯度

已知  $S = \bigcup\nolimits_{i = 1}^N {\left\{ {\left\langle {{{\vec x}_i},{y_i}} \right\rangle } \right\}}$  ，  ${y_i} \in 1 \cdots n$  为 label， ${\vec x_i}$  为feature。

softmax交叉熵损失函数的数学形式为：

$\operatorname{softmax\_loss} \left( S \right) = -
\frac{1}{N}\sum\nolimits_{i = 1}^N {{{\vec e}^T}\left( {{y_i}} \right){{\log
}^ \circ }\operatorname{softmax} \left( {{{\vec x}_i}} \right)}$  。

其中  $\vec e\left( {{y_i}} \right) = {\begin{bmatrix} {1\left\{ {{y_i} = 1} \right\};}&{ \cdots ;}&{1\left\{ {{y_i} = n} \right\}} \end{bmatrix}}$  ，即  ${y_i}$  的 one-hot 编码，  ${\vec 1^T}\vec e\left({{y_i}} \right) = 1$  恒成立。

softmax 交叉熵损失函数的梯度为：

$$\nabla \operatorname{softmax\_loss} \left( S \right) =
\frac{1}{N}\sum\nolimits_{i = 1}^N {\left( {\operatorname{softmax} \left(
{{{\vec x}_i}} \right) - \vec e\left( {{y_i}} \right)} \right)}$$

证明如下：

欲求  $\operatorname{softmax\_loss} \left( S \right)$  的导数，我们先需要得到  ${\log ^\circ }\operatorname{softmax} \left( {{{\vec x}_i}} \right)$  的导数，不妨记 $\operatorname{log\_softmax} \left( {\vec x} \right) = {\log ^ \circ }\operatorname{softmax} \left( {\vec x} \right)$  。

$$\begin{aligned} d\log\_\operatorname{softmax} \left( {\vec x} \right) 
&= d{\log ^ \circ }\frac{{{{\exp }^ \circ }\left( {\vec x} \right)}}{{{{\vec1}^T}{{\exp }^ \circ }\left( {\vec x} \right)}} \\ 
&= d\left( {\vec x - \log\left( {{{\vec 1}^T}{{\exp }^ \circ }\left( {\vec x} \right)} \right)\vec 1}\right) \\ 
&= d\vec x - \vec 1d\left( {\log \left( {{{\vec 1}^T}{{\exp }^\circ }\left( {\vec x} \right)} \right)} \right) \\ 
\end{aligned}$$

上式中的  $\log \left( {{{\vec 1}^T}{{\exp }^ \circ }\left( {\vec x} \right)}\right)$  在数学中常被称为log-sum-exp函数（由其计算方式得名），不妨记为  $\operatorname{LSE} \left({\vec x} \right)$  。

$$d\operatorname{LSE} \left( {\vec x} \right) 
= \frac{{{{\vec 1}^T}d{{\exp }^\circ }\left( {\vec x} \right)}}{{{{\vec 1}^T}{{\exp }^ \circ }\left( {\vec x}\right)}} 
= \frac{{{{\vec 1}^T}\operatorname{diag} \left( {{{\exp }^ \circ}\left( {\vec x} \right)} \right)d\vec x}}{{{{\vec 1}^T}{{\exp }^ \circ}\left( {\vec x} \right)}} 
= \frac{{{{\exp }^ \circ }\left( {{{\vec x}^T}}\right)}}{{{{\vec 1}^T}{{\exp }^ \circ }\left( {\vec x} \right)}}d\vec x 
={\operatorname{softmax} ^T}\left( {\vec x} \right)d\vec x$$

所以  $\nabla \operatorname{LSE} \left( {\vec x} \right) = \operatorname{softmax} \left( {\vec x} \right)$ ，可见 LSE 函数的梯度是 softmax 函数。于是得到

$$\begin{aligned} d\log\_\operatorname{softmax} \left( {\vec x} \right) 
&= d\vec x - \vec 1d\left( {\log \left( {{{\vec 1}^T}{{\exp }^ \circ }\left( {\vec x} \right)} \right)} \right) \\ 
&= d\vec x - \vec 1{\operatorname{softmax} ^T}\left( {\vec x} \right)d\vec x \\ 
&= \left( {I - \vec 1{{\operatorname{softmax} }^T}\left( {\vec x} \right)} \right)d\vec x \\
\end{aligned}$$

所以  $\nabla \operatorname{log\_softmax} \left( {\vec x} \right) = I - \vec 1{\operatorname{softmax} ^T}\left( {\vec x} \right)$  。

利用上面的结论可得，softmax交叉熵损失函数的梯度：

$$\begin{aligned} 
\nabla \operatorname{softmax\_loss} \left( S \right) 
&= -\frac{1}{N}\sum\nolimits_{i = 1}^N {\left( {I - \operatorname{softmax} \left({{{\vec x}_i}} \right){{\vec 1}^T}} \right)\vec e\left( {{y_i}} \right)} \\
&= \frac{1}{N}\sum\nolimits_{i = 1}^N {\left( {\operatorname{softmax} \left({{{\vec x}_i}} \right){{\vec 1}^T}\vec e\left( {{y_i}} \right) - \vec e\left({{y_i}} \right)} \right)} \\ 
&= \frac{1}{N}\sum\nolimits_{i = 1}^N {\left({\operatorname{softmax} \left( {{{\vec x}_i}} \right) - \vec e\left( {{y_i}}\right)} \right)} \\ 
\end{aligned}$$

##  综合

上面推的一大堆的公式，可以总结为下面的表格。

![](https://pic1.zhimg.com/v2-6fba470f63fa42d570857c64ba0b234c_b.jpg)

***

### **更新记录**
- 20200612, 发布
  
### **版权声明**
版权声明: 自由分享, 保持署名-非商业用途-非衍生, 知识共享3.0协议.  
如果你对本文有疑问或建议, 欢迎留言! 转载请保留版权声明!

