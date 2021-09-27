#! https://www.zhihu.com/question/48075261/answer/115387206

[comment]: <> (Answer URL: https://www.zhihu.com/question/48075261/answer/115387206)
[comment]: <> (Question Title: python numpy的样本标准差怎么写?)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2016-08-06 22:18:20)

有时候人容易犯知其一不知其二的错误，`np.std` 也是支持计算无偏样本标准差的（话说无偏样本标准差这么常用，NumPy怎么会不支持呢），见如下代码：  

```python
>>> a = np.arange(10)
>>> a
array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> np.std(a, ddof=1)
3.0276503540974917
>>> np.sqrt(((a - np.mean(a)) ** 2).sum() / (a.size - 1))
3.0276503540974917
>>> np.sqrt(( a.var() * a.size) / (a.size - 1))
3.0276503540974917
```

