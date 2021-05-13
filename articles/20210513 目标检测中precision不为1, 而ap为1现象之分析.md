#! https://zhuanlan.zhihu.com/p/372128335
# 目标检测中precision不为1, 而ap为1现象之分析
最近在用 mmdet 评测某目标检测模型时遇到了一个现象 (算法大佬指出): precision 不为 1, 而 average precision (ap) 为 1. 按照之前的理解, ap 是 PR 曲线的曲线下面积, 如果某个 precision 不为 1, 则 ap 肯定不为 1. 起初怀疑是 ap 显示的有效数字太少, 引入了舍入误差, 但多次调整显示位数后输出的还是 1 (准确说是 1.00, 1.000 等). 于是查阅了 mmdet 的代码, 最终解决了这个困惑, 具体分析如下. 其实这种计算 ap 的方式不是 mmdet 所独有的, 在其他检测框架中也常见到, 不知道这种情况 (precision 不为 1, 而 ap 为 1) 算不算这种计算方式的一种缺陷? 

## 具体分析
mmdet 计算 ap 用到了 `average_precision` 函数, 其实现大致如下 (经过简化):
```python
def average_precision(recalls, precisions):
    mrec = np.concatenate(([0], recalls, [1]))
    mpre = np.concatenate(([0], precisions, [0]))
    for i in range(mpre.size - 1, 0, -1):
        mpre[i - 1] = max(mpre[i - 1], mpre[i])
    ind = np.where(mrec[1:] != mrec[:-1])[0] 
    ap = np.sum((mrec[ind + 1] - mrec[ind]) * mpre[ind + 1])
    return ap
```

来看一个下面的 recalls 和 precisions (简单起见, 不妨分别视作 mrec 和 mprec) : 
```
recalls = [0.03846154, 0.07692308, 0.11538462, 0.15384615, 0.19230769, 0.23076923,
           0.26923077, 0.30769231, 0.34615385, 0.38461538, 0.42307692, 0.46153846,
           0.5,        0.53846154, 0.57692308, 0.61538462, 0.65384615, 0.69230769,
           0.73076923, 0.76923077, 0.80769231, 0.84615385, 0.88461538, 0.92307692,
           0.96153846, 1.,         1.,         1.,         1.,         1.,        ]
precisions = [1.,        1.,        1.,        1.,        1.,        1.,
              1.,        1.,        1.,        1.,        1.,        1.,
              1.,        1.,        1.,        1.,        1.,        1.,
              1.,        1.,        1.,        1.,        1.,        1.,
              1. ,       1.,        0.962963,  0.9285714, 0.8965517, 0.8666667]
```
由于 recalls 后面几项均为 1, `ind = np.where(mrec[1:] != mrec[:-1])[0] ` 执行后,  `ind` 不会包含后面几项的索引.

接下来的 `ap = np.sum((mrec[ind + 1] - mrec[ind]) * mpre[ind + 1])`, precisions 的后面几项将不参与计算, 剩下参与计算的 precisions 项均为 1, 所以最终计算得到的 ap 存在为 1 的可能.


## 完整测试代码
```python
import numpy as np
from sklearn.metrics import auc


def average_precision(recalls, precisions):
    mrec = np.concatenate(([0], recalls, [1]))
    mpre = np.concatenate(([0], precisions, [0]))
    for i in range(mpre.size - 1, 0, -1):
        mpre[i - 1] = max(mpre[i - 1], mpre[i])
    ind = np.where(mrec[1:] != mrec[:-1])[0] 
    # print(ind)
    ap = np.sum((mrec[ind + 1] - mrec[ind]) * mpre[ind + 1])
    return ap


if __name__ == '__main__':
    recalls = [0.03846154, 0.07692308, 0.11538462, 0.15384615, 0.19230769, 0.23076923,
               0.26923077, 0.30769231, 0.34615385, 0.38461538, 0.42307692, 0.46153846,
               0.5,        0.53846154, 0.57692308, 0.61538462, 0.65384615, 0.69230769,
               0.73076923, 0.76923077, 0.80769231, 0.84615385, 0.88461538, 0.92307692,
               0.96153846, 1.,         1.,         1.,         1.,         1.,        ]
    precisions = [1.,        1.,        1.,        1.,        1.,        1.,
                  1.,        1.,        1.,        1.,        1.,        1., 
                  1.,        1.,        1.,        1.,        1.,        1.,
                  1.,        1.,        1.,        1.,        1.,        1., 
                  1. ,       1.,        0.962963,  0.9285714, 0.8965517, 0.8666667]
    print(average_precision(recalls, precisions))
    print(auc(recalls, precisions))
    
```

## **更新记录**
- 20210513, 发布

## **版权声明**
保持署名-非商业用途-非衍生, 知识共享3.0协议.  

