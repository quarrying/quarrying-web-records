#! https://www.zhihu.com/question/320285746/answer/1267910681

[comment]: <> (Answer URL: https://www.zhihu.com/question/320285746/answer/1267910681)
[comment]: <> (Question Title: 如何用python或者pytorch实现一个神奇的操作？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2020-06-06 18:20:22)

可以参考下面的代码, 没有显式地使用循环, 而是利用了 np.pad 和 np.take, 关键之处是计算平移后的索引. 代码没有进行参数检查和充分的测试, 请慎用.

```python
import numpy as np

def strange_func(x, h_offset):
    h_offset = np.expand_dims(np.squeeze(np.asarray(h_offset)), 0)
    top_pad_size = np.abs(np.minimum(np.min(h_offset), 0))
    bottom_pad_size = np.maximum(np.max(h_offset), 0)
    x_padded = np.pad(x, ((top_pad_size, bottom_pad_size),(0, 0)), mode='constant')
    indices = np.reshape(np.arange(x_padded.shape[0] * x_padded.shape[1]), 
                            (x_padded.shape[1], x_padded.shape[0])).T
    indices = (indices + h_offset)[top_pad_size:-bottom_pad_size, :]
    return np.take(x_padded.T.flat, indices)
    
if __name__ == '__main__':
    h, w = 7, 6
    h_offset = [1, -1, 2, 0, -3, 0]
    x = np.ones((h, w))
    y = strange_func(x, h_offset)
    print(x)
    print(y)
```
输出结果为
```
[[1. 1. 1. 1. 1. 1.]
    [1. 1. 1. 1. 1. 1.]
    [1. 1. 1. 1. 1. 1.]
    [1. 1. 1. 1. 1. 1.]
    [1. 1. 1. 1. 1. 1.]
    [1. 1. 1. 1. 1. 1.]
    [1. 1. 1. 1. 1. 1.]]
[[1. 0. 1. 1. 0. 1.]
    [1. 1. 1. 1. 0. 1.]
    [1. 1. 1. 1. 0. 1.]
    [1. 1. 1. 1. 1. 1.]
    [1. 1. 1. 1. 1. 1.]
    [1. 1. 0. 1. 1. 1.]
    [0. 1. 0. 1. 1. 1.]]
```
