#! https://www.zhihu.com/question/53182986/answer/135792209

[comment]: <> (Answer URL: https://www.zhihu.com/question/53182986/answer/135792209)
[comment]: <> (Question Title: 如何theano程序调试，查看数据shape?)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2016-12-14 13:33:55)

```python
>>> import theano.tensor as T
>>> x = T.ones((3, 4))
>>> x.shape.eval()
array([3, 4], dtype=int64)
>>> x.eval().shape
(3L, 4L)
```

