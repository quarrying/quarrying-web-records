#! https://www.zhihu.com/question/48471997/answer/138090073

[comment]: <> (Answer URL: https://www.zhihu.com/question/48471997/answer/138090073)
[comment]: <> (Question Title: caffe中那些层支持in-place计算？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2016-12-28 18:14:36)

### 最新回答 (20211204)
在 Caffe 中, 当一个 Layer 的 top 等于 bottom 时, 其 forward 会改变 bottom 中的数据 (因为 top 和 bottom 共用同一存储空间), 如果接下来的 backward 没有用到被改变前的 bottom 中的数据, 那么这个 Layer 就是支持 in-palce 的. 支持 in-place 的 Layer 需要满足 top 等于 bottom, 这就排除了一些层: 如卷积层和池化层, 因为它们的 top 和 bottom 尺寸一般情况下是不一样的. 

下面是 [Caffe](https://github.com/BVLC/caffe/tree/9b891540183ddc834a02b2bd81b31afae71b2153) 中支持 in-place 运算的层的不完全列举, 并给出了理由 (个人观点, 没有验证, 如有错误, 欢迎指正).

- **BatchNormLayer**: 没有用到 `bottom_data`.
- **BiasLayer**: 没有用到 `bottom_data`.
- **ClipLayer**: 用到 `bottom_data`, 但 `bottom_data[i] >= min && bottom_data[i] <= max` 等价于 `top_data[i] >= min && top_data[i] <= max`.
- **DropoutLayer**: 没有用到 `bottom_data`.
- **ELULayer**: 用到 `bottom_data`, 但 `bottom_data[i] > 0` 等价于 `bottom_data[i] > 0`, 且 `bottom_data[i] <= 0` 等效于 `top_data[i] <= 0`.
- **ExpLayer**: 没有用到 `bottom_data`.
- **PReLULayer**: 用到 `bottom_data`, 但当 in-place 操作时用 `bottom_memory_` 来恢复改变前的 `bottom_data`.
- **ReLULayer**: 用到 `bottom_data`, 但 `(bottom_data[i] > 0) + negative_slope * (bottom_data[i] <= 0)` 等价于 `(top_data[i] > 0) + negative_slope * (top_data[i] <= 0)`.
- **ScaleLayer**: 用到 `bottom_data`, 但当 in-place 操作时用 `temp_` 来恢复改变前的 `bottom_data`.
- **SigmoidLayer**: 没有用到 `bottom_data`.
- **SoftmaxLayer**: 没有用到 `bottom_data`.
- **SwishLayer**: 没有用到 `bottom_data`.
- **TanHLayer**: 没有用到 `bottom_data`.

注意到大部分都是 `NeuronLayer` 的子类.

----
### 第一次回答 (20161228)
不完全列举：ReLU层，Dropout层，BatchNorm层，Scale层
