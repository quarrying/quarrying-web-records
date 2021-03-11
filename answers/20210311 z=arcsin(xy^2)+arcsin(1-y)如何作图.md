#! https://www.zhihu.com/answer/1774815866


[comment]: <> (Answer URL: https://www.zhihu.com/question/396132009/answer/1261546116)
[comment]: <> "Question Title: z=arcsin(x/y^2)+arcsin(1-y)如何作图？"
[comment]: <> (Author Name: 采石工)

参考代码如下:

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

if __name__ == '__main__':
    x = np.linspace(-4, 4, 100)
    y = np.linspace(0.001, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.arcsin(X / (Y**2)) + np.arcsin(1 - Y)
    # plot_surface 不支持过滤 NaN 值, 所以不妨将 NaN 值转化为 0
    Z[np.isnan(Z)] = 0

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)
    plt.show()
```
函数图形如下:
![函数图形](https://pic4.zhimg.com/80/v2-33b058d776919ec9611037972457816c.png)

