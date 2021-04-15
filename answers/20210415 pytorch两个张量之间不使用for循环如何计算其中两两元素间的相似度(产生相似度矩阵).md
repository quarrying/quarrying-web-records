#! https://www.zhihu.com/question/454233624/answer/1835919262

[comment]: <> (Answer URL: https://www.zhihu.com/question/454233624/answer/1835919262)
[comment]: <> "pytorch两个张量之间不使用for循环如何计算其中两两元素间的相似度(产生相似度矩阵)？"
[comment]: <> (Author Name: https://www.zhihu.com/people/quarrying)


可以使用 `torch.nn.functional.cosine_similarity`, 参考代码:

```python
import torch
import torch.nn.functional as F

features_a = torch.rand((4, 64))
features_b = torch.rand((5, 64))
similarity_matrix = F.cosine_similarity(features_a.unsqueeze(1), 
                                        features_b.unsqueeze(0), dim=2)
print(similarity_matrix.shape)
print(similarity_matrix)
```