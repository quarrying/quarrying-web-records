#! https://www.zhihu.com/question/407177119/answer/1341761547

[comment]: <> (Answer URL: https://www.zhihu.com/question/407177119/answer/1341761547)
[comment]: <> (Question Title: 机器学习clean dataset是指怎样的数据集？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2020-07-16 13:08:55)

就分类数据集而言, 一个干净的数据集, 可能指的是:

1) 某类的数据中没有混入其他类别的数据, 且没有混入与该分类任务不相关的数据.

2) 不存在同一类别的数据, 有多个类别标签 (例如有的明星有艺名, 本名和曾用名, 不能认为这些名字是不同的人).

3) 不存在不满足质量要求的数据 (例如人脸识别数据集会要求人头姿态不能太大).

