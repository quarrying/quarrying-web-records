#! https://www.zhihu.com/question/406496267/answer/1352491537

[comment]: <> (Answer URL: https://www.zhihu.com/question/406496267/answer/1352491537)
[comment]: <> (Question Title: 哪位大佬能解释一下，为什么Python会定义取模运算，就是a%b=a-n*b，n为向负无穷方向取整?)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2020-07-21 20:33:26)

确实有差异, 其实不同版本的 C++ 中取余的定义也是有差异的:

Python 中:  $a \% b = a - \lfloor a/b \rfloor \times b$  ,  $\lfloor \cdot \rfloor$  表示向下取整.

C++ 11 及之后版本中:  $a \% b = a - \left[ a/b \right] \times b$  ,  $\left[ \cdot \right]$  表示向零取整.

C++ 11 之前的版本中:  $a \% b = a - \mathrm{round}( a/b ) \times b$  , 其中取整函数 $\mathrm{round}(\cdot)$  是由实现定义的 (implementation-defined).

此外还有一个差异之处, Python 中 % 支持整型和浮点型, C++ 中 % 只支持整型.

至于它们为什么有这样的差异, 猜测可能是由于历史原因吧?

参考:
- https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations
- https://stackoverflow.com/questions/11630321/why-does-c-output-negative-numbers-when-using-modulo
- 