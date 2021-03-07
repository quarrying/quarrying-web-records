#! https://zhuanlan.zhihu.com/p/266277852

# TensorFlow 中的 logits 的由来

TensorFlow 和 PyTorch 中与 sigmoid 和 softmax 有关的类或函数中均有 logits 的出现, 下面是一些不完全的列举. 

- TensorFlow 函数名中出现 logits
  - tf.nn.sigmoid_cross_entropy_with_logits
  - tf.nn.softmax_cross_entropy_with_logits
  - tf.nn.softmax_cross_entropy_with_logits_v2
  - tf.nn.sparse_softmax_cross_entropy_with_logits
- TensorFlow 函数参数列表中出现 logits
  - tf.nn.softmax
  - tf.losses.sigmoid_cross_entropy
  - tf.losses.softmax_cross_entropy
  - tf.losses.sparse_softmax_cross_entropy
- PyTorch 类名中出现 logits
  - torch.nn.BCEWithLogitsLoss

大家都知道, logits 常用来表示 softmax 和 sigmoid 相关函数的输入参数之一, 但相信不少人都会有产生疑问: 为什么使用 logits, 这个词有什么由来? 下面是笔者结合搜索和自己理解的一家之见, 供参考.

logistic 函数 (或称 sigmoid 函数. 实际上 S 形曲线的函数都可以称为 sigmoid 函数, 但 sigmoid 函数通常指的是 logistic 函数, 所以未特别说明, 本文不加区分地使用这两个概念) 的定义为:
$$y = \operatorname{sigmoid}(x) = \frac{1}{1 + \exp(-x)}\\$$
其可转化为:
$$x = \log\frac{y}{1 - y}\\$$ 
其中 $y \in \{-1, 1\}$. 其恰为 logit 函数的定义 (logit 函数是 sigmoid 函数的逆函数), 即:
$$x = \operatorname{logit}(y)\\$$
将其代回 $y = \operatorname{sigmoid}(x)$, 可以得到:
$$y = \operatorname{sigmoid}(x) = \operatorname{sigmoid}(\operatorname{logit}(y)) = \frac{1}{1 + \exp(-\operatorname{logit}(y))}\\$$

**注意下面是自己的理解:** 由上式形式可见, 不妨将 sigmoid 函数的自变量称为 logit, 又 softmax 函数是 sigmoid 函数的推广, 其自变量不妨也被称为 logit. 由于各框架中 logit 是以一个 batch 的方式作为输入的, 所以不妨被称为 logits.


## 参考
- https://mathworld.wolfram.com/SigmoidFunction.html
- https://mathworld.wolfram.com/LogitTransformation.html
- https://stackoverflow.com/questions/41455101/what-is-the-meaning-of-the-word-logits-in-tensorflow
- [如何理解深度学习源码里经常出现的logits？](https://www.zhihu.com/question/60751553)

***
### **更新记录**
- 20201016, 发布
### **版权声明**
版权声明: 自由分享, 保持署名-非商业用途-非衍生, 知识共享3.0协议.  
如果你对本文有疑问或建议, 欢迎留言! 转载请保留版权声明!

