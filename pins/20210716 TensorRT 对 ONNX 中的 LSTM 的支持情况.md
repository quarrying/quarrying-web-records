公司同事发布了一版 OCR 模型 (ONNX 格式), 在部署的时候遇到了问题, 反馈的原因是 TensorRT 6.0 不支持 LSTM. 但从 TensorRT 6.0 的文档 [1] 来看 `nvinfer1::IRNNv2Layer` 是可以实现 LSTM (bidirectional) 的. 所以严格地说: 不是 TensorRT 6.0 不支持 LSTM, 而是 TensorRT 6.0 不支持 ONNX 中的 LSTM. 遂又搜索了 TensorRT 对 ONNX 的支持情况, 验证了这一说法:  由 [2] 可见, TensorRT 6.0 确实不支持 ONNX 中 LSTM, 由 [3] 可见, TensorRT 7.0 (应该还包括以后的版本) 支持 ONNX 中 LSTM. 

- [1] https://docs.nvidia.com/deeplearning/tensorrt/archives/tensorrt-601/tensorrt-api/c_api/classnvinfer1_1_1_i_r_n_nv2_layer.html
- [2] https://github.com/onnx/onnx-tensorrt/blob/6.0/operators.md
- [3] https://github.com/onnx/onnx-tensorrt/blob/7.0/operators.md
