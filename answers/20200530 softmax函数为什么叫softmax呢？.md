#! https://www.zhihu.com/question/269806612/answer/1254773576

[comment]: <> (Answer URL: https://www.zhihu.com/question/269806612/answer/1254773576)
[comment]: <> (Question Title: softmax函数为什么叫softmax呢？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2020-05-30 14:17:22)

softmax 函数更接近于 argmax 函数而不是 max 函数. soft 这个前缀源于 softmax 函数是连续可微的. argmax 函数的结果可以表示为一个 one-hot 向量, 它不是连续和可微的 (注: argmax 的一般实现是返回最大值所在的索引, 但这个索引可以转化为 one-hot 向量). softmax 函数提供了 argmax 的软化版本. max 函数相应的软化版本可以记为  ${\mathrm{softmax} ^T}\left( {\vec x} \right)\vec x$  (注: max 函数还可以表示为 $\mathrm{argmax} ^{T}\left( {\vec x} \right)\vec x$, 如果 argmax 函数返回的是 one-hot 向量的话). 最好是把 softmax 函数称为 softargmax, 但当前名称已经是一个根深蒂固的习惯了.

摘自 Ian Goodfellow 等人的《深度学习》, 括号内的内容是答主自己加的.

