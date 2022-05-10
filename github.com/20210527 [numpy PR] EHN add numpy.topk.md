## [EHN: add numpy.topk](https://github.com/numpy/numpy/pull/19117)

Hi, find topk elements is widely used in machine learning and elsewhere, and some python frameworks have implemented it, e.g. TensorFlow (`tf.math.top_k`), PyTorch (`torch.topk`). 

I try to implement topk using core numpy functions, and have checked its correctness using `torch.topk`. The following is the test code snippet:

```python
import random

import torch
import numpy as np


def topk_np(a, k, axis=-1, largest=True, sorted=True):
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

    top_values, top_indices = topk_np(arr, k, axis=axis, largest=largest, sorted=sorted)
    
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

    top_values, top_indices = topk_np(arr, k, axis=axis, largest=largest, sorted=sorted)
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

    top_values, top_indices = topk_np(arr, k, axis=axis, largest=largest, sorted=sorted)
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


## NumPy PR 的注意事项
```
<!--         ----------------------------------------------------------------
                MAKE SURE YOUR PR GETS THE ATTENTION IT DESERVES!
                ----------------------------------------------------------------

*  FORMAT IT RIGHT:
      http://www.numpy.org/devdocs/dev/development_workflow.html#writing-the-commit-message

*  IF IT'S A NEW FEATURE OR API CHANGE, TEST THE WATERS:
      http://www.numpy.org/devdocs/dev/development_workflow.html#get-the-mailing-list-s-opinion

*  HIT ALL THE GUIDELINES:
      https://numpy.org/devdocs/dev/index.html#guidelines

*  WHAT TO DO IF WE HAVEN'T GOTTEN BACK TO YOU:
      http://www.numpy.org/devdocs/dev/development_workflow.html#getting-your-pr-reviewed
-->
```

## PR 时遇到的问题
```
  File "/home/vsts/work/1/s/build/testenv/lib/python3.8/site-packages/numpy/core/fromnumeric.py", line 1284, in <module>
    def topk(a, k, axis=-1, largest=True, sorted=True):
  File "/home/vsts/work/1/s/build/testenv/lib/python3.8/site-packages/numpy/core/overrides.py", line 189, in decorator
    verify_matching_signatures(implementation, dispatcher)
  File "/home/vsts/work/1/s/build/testenv/lib/python3.8/site-packages/numpy/core/overrides.py", line 111, in verify_matching_signatures
    raise RuntimeError('dispatcher functions can only use None for '
RuntimeError: dispatcher functions can only use None for default argument values
```

## PR 问题回复
- https://github.com/numpy/numpy/pull/19117


## 发送邮件到 numpy-discussion@python.org
QQ 邮箱发送不了, 所以改用科大邮箱.
```
标题: Discusions about 'add numpy.topk'

Hi, all.

Finding topk elements is widely used in several fields, but missed in NumPy.
I implement this functionality named as numpy.topk using core numpy 
functions and open a PR: 

https://github.com/numpy/numpy/pull/19117

Any discussion are welcome.

Best wishes,

Kang Kai
```


