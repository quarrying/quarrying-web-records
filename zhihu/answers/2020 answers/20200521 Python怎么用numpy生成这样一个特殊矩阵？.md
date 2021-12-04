#! https://www.zhihu.com/question/389310583/answer/1236650915

[comment]: <> (Answer URL: https://www.zhihu.com/question/389310583/answer/1236650915)
[comment]: <> (Question Title: Python怎么用numpy生成这样一个特殊矩阵？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2020-05-21 13:44:26)

用 NumPy 比较容易实现, 如下:

```python
import numpy as np


def get_matrix(rows, cols, index_from_zero=True):
    xx, yy = np.meshgrid(np.arange(cols), np.arange(rows))
    if index_from_zero:
        return np.dstack((yy, xx))
    else:
        return np.dstack((yy, xx)) + 1
    
    
if __name__ == '__main__':
    x = get_matrix(3, 4)
    print(x[1, 2])
    x = get_matrix(3, 4, False)
    print(x[1, 2])
```
