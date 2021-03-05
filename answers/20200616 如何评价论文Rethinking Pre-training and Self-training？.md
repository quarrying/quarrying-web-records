#! https://www.zhihu.com/question/401621721/answer/1285924189

[comment]: <> (Answer URL: https://www.zhihu.com/question/401621721/answer/1285924189)
[comment]: <> (Question Title: 如何评价论文Rethinking Pre-training and Self-training？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2020-06-16 13:46:21)

1）验证了在目标检测任务中当训练集增大到一定规模时，（监督训练的）预训练模型不再起正面作用。这也是何文  [1] 中的结论，不过作者进一步实验验证了数据增强方式越激进，预训练模型的价值越小，甚至会有副作用。即增大训练集规模和强化数据增强方式，对于预训练模型有着类似的作用。作者又进一步验证了对于非监督训练的预训练模型也有类似的结论。

2）实验验证了在目标检测和语义分割任务中（分类任务中自训练的工作别人已经做了），不管训练集规模大小和数据增强的激进程度，自训练（一种半监督学习方法，借用论文 [2]  中一句话： Self-training first uses labeled data to train a good teacher model, then use the teacher model to label unlabeled data and finally use the labeled data and unlabeled data to jointly train a student model；这篇论文用的是 self-training with Noisy Student）总能带来性能提升。

3）一点个人感想：数据很重要，不管是数据增强合成的数据，还是teacher model标注的伪标签数据，数据量上来了，模型性能自然会水涨船高。

##  参考

  1. ^  [2018] Rethinking ImageNet Pre-training 
  2. ^  [2019] Self-training with Noisy Student improves ImageNet classification 

