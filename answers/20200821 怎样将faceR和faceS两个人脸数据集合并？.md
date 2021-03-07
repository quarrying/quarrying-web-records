#! https://www.zhihu.com/question/407200257/answer/1424887241

[comment]: <> (Answer URL: https://www.zhihu.com/question/407200257/answer/1424887241)
[comment]: <> (Question Title: 怎样将faceR和faceS两个人脸数据集合并？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2020-08-21 22:19:45)

提供一个简单的思路 (假设 faceR 和 faceS 数据集内没有同身份但标签不同的情况):

1. 利用人脸识别模型提取两个数据集每张图像的特征. 特征维度不妨记为  $D$  . 
2. 计算每人所有图像特征的均值并归一化, 作为该人的特征表示. 设 faceR 数据集中有  $M$  人, faceS 数据集中有  $N$  人, 则 faceR 数据集得到一个  $M \times D$  的特征矩阵  $R$  , faceS 数据集得到一个  $N \times D$  的特征矩阵  $S$  . 
3. 计算两个数据集两两人之间的特征相似性, 即计算  $RS^T$  , 其为  $M \times N$  矩阵. 
4. 预先设置一个相似度阈值 (这个阈值是在某个测试集根据 FAR 和 TAR 要求测得的). 对于  $RS^T$  每一行 (即相当于 faceR 数据集的每一人, 不妨记为  $\mathrm{faceR}_i$  ), 找到相似度最大的元素 (即相当于与  $\mathrm{faceR}_i$  最相似的人, 不妨记为  $\mathrm{faceS}_i$  ), 如果其值小于所设相似度阈值, 则认为 faceS 中没有人与  $\mathrm{faceR}_i$  疑似为同一人, 反之则认为  $\mathrm{faceS}_i$  与  $\mathrm{faceR}_i$  疑似为同一人, 并记录下来. 
5. 人工核验上一步记录下来的疑似同一人的列表. 

上面的方法可以很容易推广到: faceR 和 faceS 数据集内存在同身份但标签不同的情况, 在此就不赘述了.

