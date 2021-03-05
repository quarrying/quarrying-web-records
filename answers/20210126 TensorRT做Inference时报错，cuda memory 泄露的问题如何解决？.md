#! https://www.zhihu.com/question/410656967/answer/1699366831

[comment]: <> (Answer URL: https://www.zhihu.com/question/410656967/answer/1699366831)
[comment]: <> (Question Title: TensorRT做Inference时报错，cuda memory 泄露的问题如何解决？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2021-01-26 21:17:35)

同遇到这个问题 (TensorRT 版本是7.0), 通过搜索  [1]  [2]  [3]  猜测原因可能是, IExecutionContext::setBindingDimensions 内部存在显存泄露, 一些链接中提到升级 TensorRT 版本可以解决这个问题. 于是将 TensorRT 升级到 7.2, 问题解决.

##  参考

  1. ^  [ https://forums.developer.nvidia.com/t/context-setbindingdimensions-casing-gpu-memory-leak/83423/7 ](https://forums.developer.nvidia.com/t/context-setbindingdimensions-casing-gpu-memory-leak/83423/7)
  2. ^  [ https://forums.developer.nvidia.com/t/tensorrt-6-iexecutioncontext-execute-cause-gpu-memory-leak/83680/5 ](https://forums.developer.nvidia.com/t/tensorrt-6-iexecutioncontext-execute-cause-gpu-memory-leak/83680/5)
  3. ^  [Memory leak when creating and deleting a new IExecutionContext at each iteration #582](https://github.com/NVIDIA/TensorRT/issues/582)

