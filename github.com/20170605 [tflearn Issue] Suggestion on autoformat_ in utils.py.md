## [Suggestion on autoformat_* in utils.py](https://github.com/tflearn/tflearn/issues/781)

In file `utils.py`:
```python
# Auto format kernel for 3d convolution
def autoformat_kernel_3d(kernel):
```
Actually, `autoformat_kernel_3d` was used in `avg_pool_3d` and `max_pool_3d`, not in `conv_3d`.
So comment for `autoformat_kernel_3d` may be misleading. 

The following is the code in order to improve the readablity on `autoformat_*`.

```python  
# Auto format strides parameter for 2d convolution and 2d pooling
def autoformat_strides_2d(strides):
    if isinstance(strides, int):
        return [1, strides, strides, 1]
    elif isinstance(strides, (tuple, list)):
        if len(strides) == 2:
            return [1, strides[0], strides[1], 1]
        elif len(strides) == 4:
            assert strides[0] == strides[3] == 1, "Must have strides[0] = strides[3] = 1"
            return [strides[0], strides[1], strides[2], strides[3]]
        else:
            raise Exception("strides length error: " + str(len(strides))
                            + ", only a length of 2 or 4 is supported.")
    else:
        raise Exception("strides format error: " + str(type(strides)))
        
# Auto format ksize parameter for 2d pooling
def autoformat_pool_ksize_2d(ksize):
    if isinstance(ksize, int):
        return [1, ksize, ksize, 1]
    elif isinstance(ksize, (tuple, list)):
        if len(ksize) == 2:
            return [1, ksize[0], ksize[1], 1]
        elif len(ksize) == 4:
            assert ksize[0] == ksize[3] == 1, "Must have ksize[0] = ksize[3] = 1"
            return [ksize[0], ksize[1], ksize[2], ksize[3]]
        else:
            raise Exception("ksize length error: " + str(len(ksize))
                            + ", only a length of 2 or 4 is supported.")
    else:
        raise Exception("ksize format error: " + str(type(ksize)))
        
# Auto format filter parameter for 2d convolution
# Output shape: (rows, cols, input_channels, output_channels)
def autoformat_conv_filter_2d(fsize, in_channels, out_channels):
    if isinstance(fsize, int):
        return [fsize, fsize, in_channels, out_channels]
    elif isinstance(fsize, (tuple, list)):
        if len(fsize) == 2:
            return [fsize[0], fsize[1], in_channels, out_channels]
        else:
            raise Exception("filter length error: " + str(len(fsize))
                            + ", only a length of 2 is supported.")
    else:
        raise Exception("filter format error: " + str(type(fsize)))
    
```

Thanks!
