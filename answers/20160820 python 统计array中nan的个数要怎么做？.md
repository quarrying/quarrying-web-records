#! https://www.zhihu.com/question/39951948/answer/117896605

[comment]: <> (Answer URL: https://www.zhihu.com/question/39951948/answer/117896605)
[comment]: <> (Question Title: python 统计array中nan的个数要怎么做？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2016-08-20 13:42:33)

利用 `np.nan != np.nan` 为 `True` 的性质  

```python
>>> import numpy as np
>>> a = np.array([1, np.nan, 3, 4, np.nan, 6])
>>> a
array([  1.,  nan,   3.,   4.,  nan,   6.])
>>> np.count_nonzero(a != a)
2
```
