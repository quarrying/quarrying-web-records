#! https://www.zhihu.com/question/405249134/answer/1352344808

[comment]: <> (Answer URL: https://www.zhihu.com/question/405249134/answer/1352344808)
[comment]: <> (Question Title: 在Python中，plt.imshow为啥对于np.zeros和np.ones矩阵都显示为黑色图像?)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2020-07-21 19:03:05)

利用 plt.imshow 显示图像, 不同的数值类型显示效果是不一样的, 另外对于单通道图像, 设置不同的 cmap, 显示效果也不一样 (具体说明见 `plt.imshow` 的 help 文档). 测试代码如下:

    
```python
import numpy as np
import matplotlib.pyplot as plt

image_height, image_width = 224, 224
plt.subplot(231)
plt.imshow(np.ones((image_height, image_width), dtype=np.int8))
plt.subplot(232)
plt.imshow(np.ones((image_height, image_width), dtype=np.int8), cmap='gray')
plt.subplot(233)
plt.imshow(np.ones((image_height, image_width, 3), dtype=np.int8))

plt.subplot(234)
plt.imshow(np.ones((image_height, image_width), dtype=np.float32))
plt.subplot(235)
plt.imshow(np.ones((image_height, image_width), dtype=np.float32), cmap='gray')
plt.subplot(236)
plt.imshow(np.ones((image_height, image_width, 3), dtype=np.float32))
```
显示图为:

![](https://pic4.zhimg.com/50/v2-2fb9272549db2fd45685d5ac23fea8aa_hd.jpg?source=1940ef5c)

