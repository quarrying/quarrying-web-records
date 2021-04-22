#! https://www.zhihu.com/question/454936025/answer/1849513369


[comment]: <> (Answer URL: https://www.zhihu.com/question/454936025/answer/1849513369)
[comment]: <> "torvision中的nms是如何实现的？"
[comment]: <> (Author Name: https://www.zhihu.com/people/quarrying)


不是大佬, 强答一下:

`nms` 函数具体实现在 `$TORCHVISION$/torchvision/csrc/ops/nms.cpp` 文件中, 如下:
```
at::Tensor nms(
    const at::Tensor& dets,
    const at::Tensor& scores,
    double iou_threshold) {
  static auto op = c10::Dispatcher::singleton()
                       .findSchemaOrThrow("torchvision::nms", "")
                       .typed<decltype(nms)>();
  return op.call(dets, scores, iou_threshold);
}
```
其内部通过 `Dispatcher` 来确定具体的 nms 实现. 

在 TorchVision 中共有四种 nms 的实现.

- CPU 版本: `$TORCHVISION$/torchvision/csrc/ops/cpu/nms_kernel.cpp`.
- GPU 版本: `$TORCHVISION$/torchvision/csrc/ops/cuda/nms_kernel.cpp`.
- 量化的  CPU 版本: `$TORCHVISION$/torchvision/csrc/ops/quantized/cpu/qnms_kernel.cpp`.
- Autocast 版本: `$TORCHVISION$/torchvision/csrc/ops/autocast/qnms_kernel.cpp`.

不妨看一下 `$TORCHVISION$/torchvision/csrc/ops/cpu/nms_kernel.cpp` 这个文件, 其中包含了 nms 的实现函数 `nms_kernel`, 同时还有一段代码:
```c++
TORCH_LIBRARY_IMPL(torchvision, CPU, m) {
  m.impl(TORCH_SELECTIVE_NAME("torchvision::nms"), TORCH_FN(nms_kernel));
}
```
其作用是将 `nms_kernel` 函数注册为 `torchvision::nms` 的 CPU 版本实现.


## 参考:
- https://pytorch.org/tutorials/advanced/dispatcher.html

