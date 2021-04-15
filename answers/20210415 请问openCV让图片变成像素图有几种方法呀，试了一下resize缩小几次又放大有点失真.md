#! https://www.zhihu.com/answer/1837176680


[comment]: <> (Answer URL: https://www.zhihu.com/question/438927055/answer/1833526706)
[comment]: <> "请问openCV让图片变成像素图有几种方法呀，试了一下resize缩小几次又放大有点失真"
[comment]: <> (Author Name: https://www.zhihu.com/people/quarrying)

参考代码:
```python
"""
作者: 采石工
博客: https://www.zhihu.com/people/quarrying
发布时间: 2021年04月15日
版权声明: 自由分享, 保持署名-非商业用途-非衍生, 知识共享3.0协议.
"""
import cv2


def _two_element_tuple(int_or_tuple):
    if isinstance(int_or_tuple, (list, tuple)):
        if len(int_or_tuple) != 2:
            raise ValueError('Must be a tuple or list with 2 elements: {}'.format(int_or_tuple))
        return int(int_or_tuple[0]), int(int_or_tuple[1])
    if isinstance(int_or_tuple, int):
        return int(int_or_tuple), int(int_or_tuple)
    raise ValueError('Must be an int, a tuple or list with 2 elements')


def pixelate(image, pixel_size=32):
    pixel_width, pixel_height = _two_element_tuple(pixel_size)
    image_height, image_width = image.shape[:2]
    assert image_width >= pixel_width
    assert image_height >= pixel_height

    temp_width = int(round(image_width / pixel_width))
    temp_height = int(round(image_height / pixel_height))
    tmp = cv2.resize(image, (temp_width, temp_height), interpolation=cv2.INTER_LINEAR)
    dst = cv2.resize(tmp, (image_width, image_height), interpolation=cv2.INTER_NEAREST)
    return dst


if __name__ == '__main__':
    src = cv2.imread('lena.jpg')
    dst = pixelate(src)
    # dst = pixelate(src, (32, 64))
    cv2.imshow('src', src)
    cv2.imshow('dst', dst)
    cv2.waitKey()
    cv2.destroyAllWindows()
```
输出结果展示:

![lena_pixelate](https://pic4.zhimg.com/80/v2-58bb17cc33a4eb444677585adb2157ff.png)
