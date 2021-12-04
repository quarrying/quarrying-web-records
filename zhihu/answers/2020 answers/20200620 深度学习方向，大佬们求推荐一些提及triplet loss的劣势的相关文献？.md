#! https://www.zhihu.com/question/402066669/answer/1292854199

[comment]: <> (Answer URL: https://www.zhihu.com/question/402066669/answer/1292854199)
[comment]: <> (Question Title: 深度学习方向，大佬们求推荐一些提及triplet loss的劣势的相关文献？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2020-06-20 11:23:19)

In Defense of the Triplet Loss for Person Re-Identification 中有提到,

1) 三元组挖掘方式复杂. 挖掘困难三元组对于 Triplet loss 至关重要. 首先不能选太过简单的三元组, 因为它们包含的判别信息较少, 其次也不能选太过困难的三元组, 因为它们往往是噪声或称局外点, 所以只能选那些中等 (moderate) 困难的三元组. 虽说复杂, 但不能说是它的劣势.

2) 引入了更多的计算量. 下面是原文的引用: Regardless of which type of mining is being done, it is a separate step from training and adds considerable overhead, as it requires embedding a large fraction of the data with the most recent f θ and computing all pairwise distances between those data points. 这不得不说是 triplet loss 的一个小缺点.

