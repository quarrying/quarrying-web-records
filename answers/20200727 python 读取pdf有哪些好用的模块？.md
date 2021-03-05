#! https://www.zhihu.com/question/409936926/answer/1364389678

[comment]: <> (Answer URL: https://www.zhihu.com/question/409936926/answer/1364389678)
[comment]: <> (Question Title: python 读取pdf有哪些好用的模块？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2020-07-27 13:00:00)

[ PyMuPDF](https://link.zhihu.com/?target=https%3A//github.com/pymupdf/PyMuPDF) , MuPDF 的 Python 绑定 (binding). 答主曾经用它写过一段例程, 将 PDF 文件转化为图像文件, 如下供参考 (在跑下面代码之前需要先执行, pip install PyMuPDF, 注意大小写不能变):

```python
import os
import fitz


def convert_pdf_to_image(filename, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    doc = fitz.open(filename)
    stem = os.path.splitext(os.path.basename(filename))[0]
    for page_no in range(doc.pageCount):
        transform_matrix = fitz.Matrix(2.0, 2.0).preRotate(0)
        pm = doc[page_no].getPixmap(transform_matrix, alpha=False)
        pm.writePNG(os.path.join(dst_dir, '{}_{}.png'.format(stem, page_no + 1)))
        print('[{}/{}]'.format(page_no + 1, doc.pageCount))
    doc.close()
    
    
if __name__ == '__main__':
    filename = '[2011] Blind_ Referenceless Image Spatial Quality Evaluator.pdf'
    stem = os.path.splitext(os.path.basename(filename))[0]
    convert_pdf_to_image(filename, stem)
```

