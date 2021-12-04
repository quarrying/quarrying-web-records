#! https://www.zhihu.com/question/397606122/answer/1249114978

[comment]: <> (Answer URL: https://www.zhihu.com/question/397606122/answer/1249114978)
[comment]: <> (Question Title: grayscale图片对训练参数减少有多大用处？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2020-05-27 16:28:39)

1) 把输入从彩色图像 (三通道图像) 修改为灰度图像 (单通道) 确实不会减少多少参数量, 因为输入图像的通道数只会影响网络第一个卷积层的参数量.

2) 把输入从彩色图像修改为灰度图像可能对网络性能带来不好的影响.

3) 可以尝试一下 "随机灰度化数据增强", 在网络参数量不变的情况下, 提高网络性能.

