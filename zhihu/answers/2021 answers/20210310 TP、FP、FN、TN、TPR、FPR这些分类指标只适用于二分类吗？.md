#! https://www.zhihu.com/question/448582546/answer/1773168442

[comment]: <> (Answer URL: https://www.zhihu.com/question/448582546/answer/1773168442)
[comment]: <> "Question Title: TP、FP、FN、TN、TPR、FPR这些分类指标只适用于二分类吗？"
[comment]: <> (Author Name: 采石工)

对于多分类问题, 可以计算每一类的 TP, FP, FN 和 TN (当前类样本作为正样本, 其他类样本作为负样本).

得到每一类的 TP, FP, FN 和 TN 之后, 可以 1) 计算每一类的 TPR 和 FPR 等指标, 再计算它们的平均, 这称为 macro-average; 2) 分别计算所有类的 TP, FP, FN 和 TN 之和, 再计算 TPR 和 FPR 等指标, 这称为 micro-average. 

不过在多分类问题中, macro-average/micro-average FPR 并不常用 (至少答主没有见到有人用过), 常用的是 macro-average/micro-average 的 TPR (又称为 recall), precision 和 f-beta score, 当然还有准确率 (实际上准确率与 micro-average recall, micro-average precision 和  micro-average f-beta score 四者是相等的, 这个结论的证明可以参考: [为什么多分类计算出来的精确率 准确率 召回率 f1-score值都一样？](https://www.zhihu.com/question/414824969/answer/1415587771) ).
