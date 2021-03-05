#! https://www.zhihu.com/question/400039617/answer/1270642900

[comment]: <> (Answer URL: https://www.zhihu.com/question/400039617/answer/1270642900)
[comment]: <> (Question Title: 如何计算CNN中batch normalization的计算复杂度（FLOPs）？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2020-06-08 10:16:46)

下面分析在推理 (或者说测试) 时 BN 层的计算量:

设  $X$  是 BN 层的输入, 其尺寸为  $B \times H \times W \times C$  ;  $\mu$  是BN 层的 moving mean,  ${\sigma ^2}$  是 BN 层的 moving variance,  $\gamma$  是BN 层的 scale,  $\beta$ 是 BN 层的 shift, 它们的尺寸均为  $1 \times 1 \times 1 \times C$  . 为了简化推导, 设  $B = 1$  , 并令  ${X_k} = {X_{0,\cdot,\cdot,k}}$  ,  ${\mu _k} = {\mu _{0,0,0,k}}$  , ${\sigma _k} = {\sigma _{0,0,0,k}}$  ,  ${\gamma _k} = {\gamma _{0,0,0,k}}$  , ${\beta _k} = {\beta _{0,0,0,k}}$  ,  $k = 1,2, \cdots ,C$  . 则BN层的输出的第k个通道为:

$${\gamma _k}\frac{{{X_k} - {\mu _k}I}}{{\sqrt {\sigma _k^2 + \varepsilon } }}
+ {\beta _k}I = \frac{{{\gamma _k}}}{{\sqrt {\sigma _k^2 + \varepsilon }
}}{X_k} + {\beta _k}I - \frac{{{\gamma _k}{\mu _k}I}}{{\sqrt {\sigma _k^2 +
\varepsilon } }}$$

式中  $I$  是全1矩阵(而不是单位矩阵),  $\varepsilon$  是一个很小的正数, 防止除零的发生.

令  ${\alpha _k} = \frac{{{\gamma _k}}}{{\sqrt {\sigma _k^2 + \varepsilon } }}$, 则  ${\gamma _k}\frac{{{X_k} - {\mu _k}I}}{{\sqrt {\sigma _k^2 + \varepsilon} }} + {\beta _k}I = {\alpha _k}{X_k} + \left( {{\beta _k} - {\alpha _k}{\mu_k}} \right)I$  . 由于  ${\mu _k},{\sigma _k},{\gamma _k},{\beta _k}$  都是已知的, ${\alpha _k}$  和  ${\beta _k} - {\alpha _k}{\mu _k}$  可以预先计算 (NCNN中就是这样做的  [1]), 在推理时不会占用额外的计算时间, 于是  ${\alpha _k}{X_k} + \left( {{\beta _k} - {\alpha_k}{\mu _k}} \right)I$  的计算量只有  $H \times W$  次乘法运算和  $H \times W$  次加法运算, 对于C个通道计算量则有  $H \times W \times C$  次乘法运算和  $H \times W \times C$  次加法运算. 这个计算量相对于一般卷积层的计算量是很小的. 对于一般卷积则需要  ${H_{out}} \times {W_{out}} \times {C_{out}}\times {K_h} \times {K_w} \times {C_{in}}$  次乘法运算,  ${H_{out}} \times {W_{out}} \times {C_{out}} \times {K_h} \times {K_w} \times {C_{in}}$ 次加法运算(有偏置项) 或  ${H_{out}} \times {W_{out}} \times {C_{out}} \times \left( {{K_h} \times {K_w} \times {C_{in}} - 1} \right)$  次加法运算(无偏置项), 这些符号可以顾名思义, 这里就不赘述了, 详细的推导可以参考  [2]  .

另外如果网络采用 Conv-BN-ReLU 的设置, 则 BN 的参数还可以折叠 (fold) 到前面的卷积层的参数中, 这时 BN 的计算被包含到卷积的计算中了.

##  参考

  1. ^  [ https://github.com/Tencent/ncnn/blob/c61a60bfc67fcc5d8cdce20ad2ab65ba19f2b6c8/src/layer/batchnorm.cpp#L36 ](https://github.com/Tencent/ncnn/blob/c61a60bfc67fcc5d8cdce20ad2ab65ba19f2b6c8/src/layer/batchnorm.cpp#L36)
  2. ^  [ https://zhuanlan.zhihu.com/p/137719986 ](https://zhuanlan.zhihu.com/p/137719986)

