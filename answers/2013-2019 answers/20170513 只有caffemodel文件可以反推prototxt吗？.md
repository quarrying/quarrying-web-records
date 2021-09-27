#! https://www.zhihu.com/question/59597255/answer/168686857

[comment]: <> (Answer URL: https://www.zhihu.com/question/59597255/answer/168686857)
[comment]: <> (Question Title: 只有caffemodel文件可以反推prototxt吗？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2017-05-13 03:17:27)

可以通过caffemodel文件反推prototxt，代码如下：

    
```python
#coding=utf-8
'''
@author: kangkai
'''
from caffe.proto import caffe_pb2

def toPrototxt(modelName, deployName):
    with open(modelName, 'rb') as f:
        caffemodel = caffe_pb2.NetParameter()
        caffemodel.ParseFromString(f.read())

    # 兼容新旧版本
    # LayerParameter 消息中的 blobs 保存着可训练的参数
    for item in caffemodel.layers:
        item.ClearField('blobs')
    for item in caffemodel.layer:
        item.ClearField('blobs')
        
    # print(caffemodel)
    with open(deployName, 'w') as f:
        f.write(str(caffemodel))

if __name__ == '__main__':
    modelName = 'facenet_iter_14000.caffemodel'
    deployName = 'facenet_deploy.prototxt'
    toPrototxt(modelName, deployName)
```

