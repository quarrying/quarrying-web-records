#! https://www.zhihu.com/question/24058898/answer/117620288

[comment]: <> (Answer URL: https://www.zhihu.com/question/24058898/answer/117620288)
[comment]: <> (Question Title: matplotlib.pyplot.imshow如何显示灰度图？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2016-08-18 22:55:46)

我写了一个例程，可以跑起来对比一下：  

    
```python
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

img = Image.open('lena.jpg')
img = np.array(img)
if img.ndim == 3:
    img = img[:,:,0]
plt.subplot(221); plt.imshow(img)
plt.subplot(222); plt.imshow(img, cmap='gray')
plt.subplot(223); plt.imshow(img, cmap=plt.cm.gray)
plt.subplot(224); plt.imshow(img, cmap=plt.cm.gray_r)
plt.show()
```

