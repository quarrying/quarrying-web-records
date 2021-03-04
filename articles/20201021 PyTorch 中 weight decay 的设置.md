#! https://zhuanlan.zhihu.com/p/267535838
# PyTorch 中 weight decay 的设置
先介绍一下 Caffe 和 TensorFlow 中 weight decay 的设置:
- 在 **Caffe** 中, `SolverParameter.weight_decay` 可以作用于所有的可训练参数, 不妨称为 global weight decay, 另外还可以为各层中的每个可训练参数设置独立的 `decay_mult`, global weight decay 和当前可训练参数的 `decay_mult` 共同决定了当前可训练参数的 weight decay. 
- 在 **TensorFlow** 中, 某些接口可以为其下创建的可训练参数设置独立的 weight decay (如 `slim.conv2d` 可通过 `weights_regularizer`, `bias_regularizer` 分别为其下定义的 weight 和 bias 设置不同的 regularizer).

在 PyTorch 中, 模块 (`nn.Module`) 和参数 (`nn.Parameter`) 的定义没有暴露与 weight decay 设置相关的 argument, 它把 weight decay 的设置放到了 `torch.optim.Optimizer` (严格地说, 是 `torch.optim.Optimizer` 的子类, 下同) 中. 

在 `torch.optim.Optimizer` 中直接设置 `weight_decay`, 其将作用于该 optimizer 负责优化的所有可训练参数 (和 Caffe 中 `SolverParameter.weight_decay` 的作用类似), 这往往不是所期望的: BatchNorm 层的 $\gamma$ 和 $\beta$ 就不应该添加正则化项, 卷积层和全连接层的 bias 也往往不用加正则化项. 幸运地是, `torch.optim.Optimizer` 支持为不同的可训练参数设置不同的 weight_decay (`params` 支持 dict 类型), 于是问题转化为如何将不期望添加正则化项的可训练参数 (如 BN 层的可训练参数及卷积层和全连接层的 bias) 从可训练参数列表中分离出来. 笔者借鉴网上的一些方法, 写了一个满足该功能的函数, 没有经过严格测试, 仅供参考.

```python
"""
作者: 采石工
博客: http://www.cnblogs.com/quarryman/
发布时间: 2020年10月21日
版权声明: 自由分享, 保持署名-非商业用途-非衍生, 知识共享3.0协议.
"""
import torch
from torchvision import models


def split_parameters(module):
    params_decay = []
    params_no_decay = []
    for m in module.modules():
        if isinstance(m, torch.nn.Linear):
            params_decay.append(m.weight)
            if m.bias is not None:
                params_no_decay.append(m.bias)
        elif isinstance(m, torch.nn.modules.conv._ConvNd):
            params_decay.append(m.weight)
            if m.bias is not None:
                params_no_decay.append(m.bias)
        elif isinstance(m, torch.nn.modules.batchnorm._BatchNorm):
            params_no_decay.extend([*m.parameters()])
        elif len(list(m.children())) == 0:
            params_decay.extend([*m.parameters()])
    assert len(list(module.parameters())) == len(params_decay) + len(params_no_decay)
    return params_decay, params_no_decay


def print_parameters_info(parameters):
    for k, param in enumerate(parameters):
        print('[{}/{}] {}'.format(k+1, len(parameters), param.shape))
        
        
if __name__ == '__main__':
    model = models.resnet18(pretrained=False)
    params_decay, params_no_decay = split_parameters(model)
    print_parameters_info(params_decay)
    print_parameters_info(params_no_decay)
```

## 参考
- https://discuss.pytorch.org/t/weight-decay-in-the-optimizers-is-a-bad-idea-especially-with-batchnorm/16994
- https://discuss.pytorch.org/t/changing-the-weight-decay-on-bias-using-named-parameters/19132/4
- https://discuss.pytorch.org/t/how-to-set-different-learning-rate-for-weight-and-bias-in-one-layer/13450
- [Allow to set 0 weight decay for biases and params in batch norm #1402](https://github.com/pytorch/pytorch/issues/1402)


## 版权声明
版权声明: 自由分享, 保持署名-非商业用途-非衍生, 知识共享3.0协议.

如果你对本文有疑问或建议, 欢迎留言! 转载请保留版权声明! 

