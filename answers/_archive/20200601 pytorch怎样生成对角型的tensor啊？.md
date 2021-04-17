#! https://www.zhihu.com/question/398662333/answer/1258053822

[comment]: <> (Answer URL: https://www.zhihu.com/question/398662333/answer/1258053822)
[comment]: <> (Question Title: pytorch怎样生成对角型的tensor啊？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2020-06-01 11:46:12)

可以使用 `torch.diag_embed`, 测试代码如下

```python
import torch
b, n = 3, 5
x = torch.randn(b, n)
y = torch.diag_embed(x)
print(y.shape)
print(y[0])
```
