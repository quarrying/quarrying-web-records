#! https://www.zhihu.com/answer/2194330159


[//]: # (Answer URL: https://www.zhihu.com/question/494598512)
[//]: # (我想问一下，在深度学习网络中，inception结构的思想，和SPP的思想有什么区别吗？)
[//]: # (Author Name: https://www.zhihu.com/people/quarrying)

题主说的没错, 它们都可以实现多尺度 (多感受野尺寸) 的特征输出, 下面分析它们的由来:

池化层输出的感受野由其输入的感受野和特征步长, 以及池化层的 **核尺寸**  共同决定.

卷积层输出的感受野由其输入的感受野和特征步长, 以及卷积层的 **核尺寸** 和 **膨胀系数** 共同决定.

所以一个输入要想得到多尺度 (多感受野尺寸) 的输出, 方法可能有 (不全):
1) 经过不同 **核尺寸** (和相应的 **填充尺寸**) 的 **池化层**, 融合它们的输出特征, 此对应于 SPP (Spatial Pyramid Pooling). 
2) 经过不同 **膨胀系数** (和相应的 **填充尺寸**) 的 **卷积层**, 融合它们的输出特征, 此对应于 ASPP (Atrous Spatial Pyramid Pooling).
3) 经过不同 **核尺寸** (和相应的 **填充尺寸**) 的 **卷积层**, 融合它们的输出特征, 此对应于简化版的 Inception Module.
4) 先经过不同 **步长** 的卷积层或池化层, 再归一化到相同的尺寸进行融合 (可联想到 FPN, PANet 等 cross-scale feature fusion 方案).
5) 上述方法的组合.

**References**
- [关于感受野的总结](https://zhuanlan.zhihu.com/p/40267131)

