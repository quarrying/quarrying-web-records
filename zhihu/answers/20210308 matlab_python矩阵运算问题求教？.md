#! https://www.zhihu.com/question/446961393/answer/1769283470

[comment]: <> (Answer URL: https://www.zhihu.com/question/446961393/answer/1769283470)
[comment]: <> "Question Title: matlab/python矩阵运算问题求教？"
[comment]: <> (Author Name: 采石工)

答主实现了四个等效的版本, 其中 `to_diagonal_v3` (参考自其他答主的回答) 和 `to_diagonal_v4` 都没有显式地用到循环语句. 经简单测试, `to_diagonal_v2` 速度较慢, 其他几个速度上没有明显差异 (其中 `to_diagonal_v4` 的 `return_dense` 参数设置为 `True`). `to_diagonal_v4` 还有一个好处, 可以返回稀疏矩阵, 这时的内存占用较少, 而且速度更快.

```python
import time
import numpy as np
import scipy.sparse


def to_diagonal_v1(x):
    num_rows, num_cols = x.shape
    y = np.zeros((num_rows, num_rows - 1 + num_cols), dtype=x.dtype)
    for k in range(num_cols):
        y.flat[k::y.shape[1] + 1] = x[:,k]
    return y


def to_diagonal_v2(x):
    num_rows, num_cols = x.shape
    y = np.zeros((num_rows, num_rows - 1 + num_cols), dtype=x.dtype)
    for k in range(num_rows):
        y[k, k: k + num_cols] = x[k]
    return y


def to_diagonal_v3(x):
    num_rows, num_cols = x.shape
    y = np.zeros((num_rows, num_rows - 1 + num_cols), dtype=x.dtype)
    row_idx, col_idx = np.indices((num_rows, num_cols))
    col_idx += np.arange(num_rows).reshape(-1, 1)
    y[row_idx, col_idx] = x
    return y


def to_diagonal_v4(x, return_dense=True):
    num_rows, num_cols = x.shape
    diags = -np.arange(num_cols)
    y = scipy.sparse.spdiags(x.T, diags, num_rows - 1 + num_cols, num_rows).T
    if return_dense:
        return y.toarray()
    return y
    

if __name__ == '__main__':
    num_rows, num_cols = 10, 5
    x = np.arange(1, num_rows * num_cols + 1).reshape(num_rows, num_cols)
    
    y1 = to_diagonal_v1(x)
    y2 = to_diagonal_v2(x)
    y3 = to_diagonal_v3(x)
    y4 = to_diagonal_v4(x)
    # print(x)
    # print(y1)
    print(np.allclose(y1, y2))
    print(np.allclose(y1, y3))
    print(np.allclose(y1, y4))
```

