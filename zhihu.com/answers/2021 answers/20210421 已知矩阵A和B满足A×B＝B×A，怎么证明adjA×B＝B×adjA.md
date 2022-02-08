#! https://www.zhihu.com/question/455470405/answer/1847738372


[comment]: <> (Answer URL: https://www.zhihu.com/question/455470405/answer/1847738372)
[comment]: <> "已知矩阵A和B满足A×B＝B×A，怎么证明adjA×B＝B×adjA？其中adjA是矩阵A的伴随矩阵？"
[comment]: <> (Author Name: https://www.zhihu.com/people/quarrying)


根据题设, 已知 $A\operatorname{adj}(A) = \operatorname{adj}(A)A = \det(A) I$ (这是伴随矩阵的性质, 其中 $I$ 是恒等矩阵) 和 $AB = BA$.

因为: 
$$
A\operatorname{adj}(A) B\operatorname{adj}(A) = \det(A) B\operatorname{adj}(A) \\
A\operatorname{adj}(A)B\operatorname{adj}(A) = \operatorname{adj}(A) AB\operatorname{adj}(A) = \operatorname{adj}(A) BA\operatorname{adj}(A) = \operatorname{adj}(A) B \det(A)
$$
所以 $\operatorname{adj}(A) B = B \operatorname{adj}(A)$, 得证.

## 参考:
- https://encyclopediaofmath.org/wiki/Adjugate_matrix

