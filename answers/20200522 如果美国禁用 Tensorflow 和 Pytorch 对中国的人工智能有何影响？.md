#! https://www.zhihu.com/question/325873227/answer/1238379433

[comment]: <> (Answer URL: https://www.zhihu.com/question/325873227/answer/1238379433)
[comment]: <> (Question Title: 如果美国禁用 Tensorflow 和 Pytorch 对中国的人工智能有何影响？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2020-05-22 10:42:03)

想一下: 美国会采用何种方式禁用 TensorFlow 和 PyTorch.

1) 禁止中国下载 TensorFlow 和 PyTorch 的工具包和源码?

禁止方法: 把 pip 和 conda 的源, github 都禁了, 不对中国的 IP 开放.

破解方法: pip 和 conda 源有一些国内镜像, 虽然可能更新不及时, 但短期内至少可用. 既然已经都开源了, 世界上已经有很多源码的副本了,
凭此在国内可以重新维护一个新的版本. 另外国内也有公司推出了自己的深度学习开源框架, 禁止 TensorFlow 和 PyTorch
对这些公司反而是一个不小的机遇.

2) 禁止使用 TensorFlow 和 PyTorch 的中国产品在美国出售?

破解方法: 这类产品几乎都是软件产品, 主要是 APP, 云服务之类的. 包含在这些产品中的 TensorFlow 和 PyTorch
的元素可能是模型权重文件和前向推理引擎. 这个其实很容易被替代, 国内已有不少企业有自己的深度学习推理引擎 (包括开源的和私有的)
及自定义的模型权重文件格式.

3) 禁止使用 TensorFlow 和 PyTorch 的中国学者的论文在美国会议/期刊上发表?

破解方法: 这是一个昏招, 只要发动舆论就好了. 想想刚过去不久的事件: "IEEE 禁止华为员工担任旗下期刊杂志的编辑和审稿人" 的舆论及后续.

如上简单分析了一下, 美国这么做除了恶心人, 得不到一点好处.

