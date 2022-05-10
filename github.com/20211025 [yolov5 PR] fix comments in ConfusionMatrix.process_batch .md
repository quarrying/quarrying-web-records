## [fix comments in ConfusionMatrix.process_batch](https://github.com/ultralytics/yolov5/pull/5333)

https://github.com/ultralytics/yolov5/blob/a4fece8c1480aed46a38a6344b403d79c81bd751/utils/metrics.py#L148-L160
```python
n = matches.shape[0] > 0
m0, m1, _ = matches.transpose().astype(np.int16)
for i, gc in enumerate(gt_classes):
    j = m0 == i
    if n and sum(j) == 1:
        self.matrix[detection_classes[m1[j]], gc] += 1  # correct
    else:
        self.matrix[self.nc, gc] += 1  # background FP

if n:
    for i, dc in enumerate(detection_classes):
        if not any(m1 == i):
            self.matrix[dc, self.nc] += 1  # background FN
```
According to the above codes and comments, we can formulate confusion matrix as:

/                    | actual foreground | actual background
---------------------|-------------------|-------------------
predicted foreground | /                 | background FN
predicted background | background FP     | /

But it is inconsistent with the following codes in `ConfusionMatrix.plot`.
https://github.com/ultralytics/yolov5/blob/a4fece8c1480aed46a38a6344b403d79c81bd751/utils/metrics.py#L177-L181

```python
warnings.simplefilter('ignore')  # suppress empty matrix RuntimeWarning: All-NaN slice encountered
sn.heatmap(array, annot=self.nc < 30, annot_kws={"size": 8}, cmap='Blues', fmt='.2f', square=True,
           xticklabels=names + ['background FP'] if labels else "auto",
           yticklabels=names + ['background FN'] if labels else "auto").set_facecolor((1, 1, 1))
```
According to confusion matrix, `xticklabels` should be with `background FP`, and `yticklabels` should be with `background FN`.

So there may be at least one mistake. I think the mistake occurs in the comments of `ConfusionMatrix.process_batch`: If one gt (actual foreground) does not have any det (predicted foreground) matched with it, it should be considered as FN; If one det does not have any gt matched with it, it should be considered as FP. And now, confusion matrix changes into:

/                    | actual foreground | actual background
---------------------|-------------------|-------------------
predicted foreground | /                 | FP
predicted background | FN                | /

The original may be misleading, so change it accordingly.

```python
n = matches.shape[0] > 0
m0, m1, _ = matches.transpose().astype(np.int16)
for i, gc in enumerate(gt_classes):
    j = m0 == i
    if n and sum(j) == 1:
        self.matrix[detection_classes[m1[j]], gc] += 1  # correct
    else:
        self.matrix[self.nc, gc] += 1  # background FN

if n:
    for i, dc in enumerate(detection_classes):
        if not any(m1 == i):
            self.matrix[dc, self.nc] += 1  # background FP
```
