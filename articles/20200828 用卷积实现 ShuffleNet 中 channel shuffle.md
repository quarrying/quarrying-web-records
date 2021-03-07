#! https://zhuanlan.zhihu.com/p/203549964

# 用卷积实现 ShuffleNet 中 channel shuffle

ShuffleNet 中引入了 channel shuffle, 用来进行不同分组的特征之间的信息流动, 以提高性能. channel shuffle 在实现时需要用到维度重排, 在通用计算平台 (CPU/GPU) 上自然是有很多库提供维度重排算子的支持 (如 TensorFlow 中的 `tf.transpose`, PyTorch 中的 `torch.Tensor.permute` 等). 但在一些定制的硬件平台 (如 NPU) 上, 并不支持维度重排算子, 这就导致炼丹师辛辛苦苦训练的 ShuffleNet-like 模型不能在这些平台上落地 (当然最好的方法是根据定制硬件平台支持的算子列表设计网络, 从源头上规避这个问题, 但这不是本文要考虑的). 本文拟讨论: 如何用常规的 NN 算子实现 channel shuffle 算子?

来看一下 channel shuffle 操作的输入输出: 设输入尺寸为 $(B, C, H, W)$ , 则输出尺寸也是 $(B, C, H, W)$ , 另外 channel shuffle 只会改变某个位置上特征 (C 维) 的维度顺序. 简单分析一下, 可以用输出通道为 C 的 1x1 的卷积操作来实现 channel shuffle (这一转换是以牺牲一定的效率为代价的). 参考代码如下:

```python
"""
作者: 采石工
博客: http://www.cnblogs.com/quarryman/
发布时间: 2020年08月28日
版权声明: 自由分享, 保持署名-非商业用途-非衍生, 知识共享3.0协议.
"""
import torch


def shuffle_channel(x, num_groups):
    """channel shuffle 的常规实现
    """
    batch_size, num_channels, height, width = x.size()
    assert num_channels % num_groups == 0

    x = x.view(batch_size, num_groups, num_channels // num_groups, height, width)
    x = x.permute(0, 2, 1, 3, 4)
    return x.contiguous().view(batch_size, num_channels, height, width)


def create_channel_shuffle_conv_kernel(num_channels, num_groups):
    channels_per_group = num_channels // num_groups
    conv_kernel = torch.zeros(num_channels, num_channels, 1, 1)
    for k in range(num_channels):
        index = (k % num_groups) * channels_per_group + k // num_groups
        conv_kernel[k, index, 0, 0] = 1
    return conv_kernel


def shuffle_channel_v2(x, num_groups):
    """用卷积实现 channel shuffle
    """
    batch_size, num_channels, height, width = x.size()
    assert num_channels % num_groups == 0

    conv_kernel = create_channel_shuffle_conv_kernel(num_channels, num_groups)
    return torch.conv2d(x, conv_kernel)


if __name__ == '__main__':
    batch_size, num_channels, height, width = 4, 16, 7, 7
    x = torch.randn(batch_size, num_channels, height, width)
    y1 = shuffle_channel(x, 4)
    y2 = shuffle_channel_v2(x, 4)
    print(torch.allclose(y1, y2))
```

***
### **更新记录**
- 20200828, 发布
### **版权声明**
版权声明: 自由分享, 保持署名-非商业用途-非衍生, 知识共享3.0协议.  
如果你对本文有疑问或建议, 欢迎留言! 转载请保留版权声明!



