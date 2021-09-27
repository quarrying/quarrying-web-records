#! https://www.zhihu.com/question/61717516/answer/197493705

[comment]: <> (Answer URL: https://www.zhihu.com/question/61717516/answer/197493705)
[comment]: <> (Question Title: Python的Numpy操作：如何实现逐个元素取最大值，组成新array？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2017-07-13 01:49:36)

np.where 是一种方法，其实最简单的还是使用 np.maximum，如下：

```python
>>> a = np.array([[3, 5, 7], [1, 9, 5]])
>>> b = np.array([[2, 9, 8], [3, 6, 2]])
>>> np.maximum(a, b)
array([[3, 9, 8],
       [3, 9, 5]])
>>> np.where(a > b, a, b)
array([[3, 9, 8],
       [3, 9, 5]])
```
