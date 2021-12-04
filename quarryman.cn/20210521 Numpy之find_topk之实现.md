#! https://zhuanlan.zhihu.com/p/374269641

# NumPy 之实现 find_topk
返回数组中的前 K 个最大或最小的元素在现实中有着广泛的应用, 如推荐系统中返回 TopK 推荐商品, ImageNet 数据集评估中的 Top5 准确率的计算. 在不少代码框架中都有该功能的实现, 如 TensorFlow 中的 `tf.math.top_k`, PyTorch 中的 `torch.topk`. 笔者搜索了一圈, 发现 NumPy 中竟然没有此功能的函数. 但搜到了一些热心网友的实现, 如: [用numpy实现topk函数（并排序）](https://blog.csdn.net/SoftPoeter/article/details/86629329 ) 等. 这些非官方实现一般都只支持二维数组 (当然对于大部分应用已经够用了), 笔者拟进一步, 实现更通用的版本: 多维数组任意维度上的 topk 元素查找. 参考代码如下


## **代码实现**
```python
import random

import torch
import numpy as np


def find_topk(a, k, axis=-1, largest=True, sorted=True):
    if axis is None:
        axis_size = a.size
    else:
        axis_size = a.shape[axis]
    assert 1 <= k <= axis_size

    a = np.asanyarray(a)
    if largest:
        index_array = np.argpartition(a, axis_size-k, axis=axis)
        topk_indices = np.take(index_array, -np.arange(k)-1, axis=axis)
    else:
        index_array = np.argpartition(a, k-1, axis=axis)
        topk_indices = np.take(index_array, np.arange(k), axis=axis)
    topk_values = np.take_along_axis(a, topk_indices, axis=axis)
    if sorted:
        sorted_indices_in_topk = np.argsort(topk_values, axis=axis)
        if largest:
            sorted_indices_in_topk = np.flip(sorted_indices_in_topk, axis=axis)
        sorted_topk_values = np.take_along_axis(
            topk_values, sorted_indices_in_topk, axis=axis)
        sorted_topk_indices = np.take_along_axis(
            topk_indices, sorted_indices_in_topk, axis=axis)
        return sorted_topk_values, sorted_topk_indices
    return topk_values, topk_indices
    

def test_for_float_types():
    # could change its shape
    arr = np.random.rand(100, 34, 43, 54)

    axis = random.choice([*range(arr.ndim), None])
    if axis is not None:
        k = random.choice(range(1, arr.shape[axis]))
    else:
        k = random.choice(range(1, arr.size))
    largest = random.choice([True, False])
    sorted = True
    print('axis={}, k={}, largest={}, sorted={}'.format(axis, k, largest, sorted))

    top_values, top_indices = find_topk(arr, k, axis=axis, largest=largest, sorted=sorted)
    
    # topk(): argument 'dim' must be int, not NoneType, so fix it!
    if axis is None:
        arr = arr.flatten()
        axis = 0
    arr_pt = torch.from_numpy(arr)
    top_values_pt, top_indices_pt = torch.topk(arr_pt, k, dim=axis, largest=largest, sorted=sorted)

    assert np.allclose(top_values, top_values_pt.numpy())
    assert np.allclose(top_indices, top_indices_pt.numpy())


def test_for_signed_int_types():
    # could change its shape
    shape = (100, 34, 43, 54)
    # for the consistency of indices, use unique numbers
    arr = np.arange(np.prod(shape), dtype=np.int32)
    np.random.shuffle(arr)

    axis = random.choice([*range(arr.ndim), None])
    if axis is not None:
        k = random.choice(range(1, arr.shape[axis]))
    else:
        k = random.choice(range(1, arr.size))
    largest = random.choice([True, False])
    sorted = True
    print('axis={}, k={}, largest={}, sorted={}'.format(axis, k, largest, sorted))

    top_values, top_indices = find_topk(arr, k, axis=axis, largest=largest, sorted=sorted)
    # topk(): argument 'dim' must be int, not NoneType, so fix it!
    if axis is None:
        arr = arr.flatten()
        axis = 0
    arr_pt = torch.from_numpy(arr)
    top_values_pt, top_indices_pt = torch.topk(arr_pt, k, dim=axis, largest=largest, sorted=sorted)

    assert np.allclose(top_values, top_values_pt.numpy())
    assert np.allclose(top_indices, top_indices_pt.numpy())


def test_for_unsigned_int_types():
    # could change its shape
    shape = (100, 34, 43, 54)
    # for the consistency of indices, use unique numbers
    arr = np.arange(np.prod(shape), dtype=np.uint32)
    np.random.shuffle(arr)

    axis = random.choice([*range(arr.ndim), None])
    if axis is not None:
        k = random.choice(range(1, arr.shape[axis]))
    else:
        k = random.choice(range(1, arr.size))
    largest = random.choice([True, False])
    sorted = True
    print('axis={}, k={}, largest={}, sorted={}'.format(axis, k, largest, sorted))

    top_values, top_indices = find_topk(arr, k, axis=axis, largest=largest, sorted=sorted)
    # topk(): argument 'dim' must be int, not NoneType, so fix it!
    if axis is None:
        arr = arr.flatten()
        axis = 0
    # torch.from_numpy does not support uint32, so fix it!
    arr_pt = torch.from_numpy(arr.astype(np.float32))
    top_values_pt, top_indices_pt = torch.topk(arr_pt, k, dim=axis, largest=largest, sorted=sorted)

    assert np.allclose(top_values, top_values_pt.numpy())
    assert np.allclose(top_indices, top_indices_pt.numpy())


if __name__ == '__main__':
    num_repeats = 100
    for k in range(num_repeats):
        # test_for_float_types()
        test_for_signed_int_types()
        # test_for_unsigned_int_types()
```

上面将自实现的 `find_topk` 与 `torch.topk` 进行了对比测试, 以验证实现的正确性.


## **代码解析**
设指定维度上的元素数目为 $N$, 先用 `np.argpartition` 返回 topk 元素的索引 (`np.argpartition` 用的是 introselect 算法, 其时间复杂度最坏为 $O(N)$) , 再在这 $k$ 个元素上进行排序 (时间复杂度最坏一般为 $O(k\log{k})$). 而全部元素上排序的时间复杂度最坏一般为 $O(N\log{N})$, 可见在通常情况下 (即 $k$ 远小于 $N$ 时), 前者在性能上有较大的优势. 

另外值得一提的是 `np.take_along_axis` 这个函数, `np.argsort` 配合 `np.take_along_axis` 可以实现 `np.sort` 的功能, `np.argpartition` 配合 `np.take_along_axis` 可以实现 `np.partition` 的功能. 测试代码如下:
```python
import random
import numpy as np


if __name__ == '__main__':
    arr = np.random.rand(100, 34, 43)
    axis = random.choice(range(arr.ndim))
    kth = random.choice(range(1, arr.shape[axis]))

    sorted_arr = np.sort(arr, axis=axis)
    sorted_ind = np.argsort(arr, axis=axis)
    sorted_arr2 = np.take_along_axis(arr, sorted_ind, axis=axis)
    print(np.allclose(sorted_arr, sorted_arr2))

    partitioned_arr = np.partition(arr, kth, axis=axis)
    partitioned_ind = np.argpartition(arr, kth, axis=axis)
    partitioned_arr2 = np.take_along_axis(arr, partitioned_ind, axis=axis)
    print(np.allclose(partitioned_arr, partitioned_arr2))

```

## 相关动态
我把 NumPy 版本的 `find_topk` (被重命名为 `top_k`) 实现也放在我的一个开源项目中了, 在这里: [khandy](https://github.com/quarrying/KHandy). 该项目的定位是: 计算机视觉的例程库, 现在还在很初级的阶段, 后面会慢慢维护改进.

另外我在 NumPy 项目中新建了一个相关的 PR ([EHN: add numpy.topk ](https://github.com/numpy/numpy/pull/19117)), 在 NumPy 的邮件列表中也进行了一些讨论 ([EHN: Discusions about 'add numpy.topk'](http://numpy-discussion.10968.n7.nabble.com/EHN-Discusions-about-add-numpy-topk-td49281.html) ).

## **更新记录**
- 20210521, 发布
- 20210615, 更新一些内容

## **版权声明**
保持署名-非商业用途-非衍生, 知识共享3.0协议.  


