#! https://www.zhihu.com/question/59596195/answer/168684776

[comment]: <> (Answer URL: https://www.zhihu.com/question/59596195/answer/168684776)
[comment]: <> (Question Title: pycaffe中net.blobs[layername].data，这个data是存放什么数据的？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2017-05-13 02:55:15)

`net.blobs` 的类型是 `collections.OrderedDict`（即有序字典），字典的值类型为 `caffe._caffe.Blob`，`caffe._caffe.Blob` 的 `data` 属性类型是 `numpy.ndarray`。

在 Caffe 的 `python/caffe/_caffe.cpp` 文件中：
```c++
.add_property("data",  bp::make_function(&Blob<Dtype>::mutable_cpu_data,
    NdarrayCallPolicies()))
```

在 Caffe 的 `src\caffe\blob.cpp` 文件中
```c++
template <typename Dtype>
Dtype* Blob<Dtype>::mutable_cpu_data() {
    CHECK(data_);
    return static_cast<Dtype*>(data_->mutable_cpu_data());
}
```

继而定位到 `include\caffe\blob.hpp` 文件，其中
```c++
shared_ptr<SyncedMemory> data_;
```

接着在 `src\caffe\syncedmem.cpp` 文件中
```c++
void* SyncedMemory::mutable_cpu_data() {
    to_cpu();
    head_ = HEAD_AT_CPU;
    return cpu_ptr_;
}
```

在 `include\caffe\syncedmem.hpp` 文件中
```c++
void* cpu_ptr_;
```

可见 `caffe._caffe.Blob.data` 保存的数据（一般按照 `(samples, channels, rows, cols)` 的顺序）和 `cpu_ptr_` 指向的数据是一样的，只不过 Python 中把它包装为 `numpy.ndarray` 的形式。

以上。

