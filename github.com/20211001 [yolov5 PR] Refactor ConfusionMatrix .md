## [Refactor ConfusionMatrix](https://github.com/ultralytics/yolov5/pull/5016)

Hi, I refactor `ConfusionMatrix` to make it more efficient and readable. The following codes could be used for understanding and testing about new `ConfusionMatrix`. Any discussion are welcome.
```python
import time
import numpy as np
from scipy.sparse import csr_matrix


def get_matches(overlaps, thresh):
    """Adapted from current implementation of `ConfusionMatrix`
    """
    num_gts, num_dets = overlaps.shape
    indices = np.where(overlaps > thresh)
    if num_gts:
        matches = np.concatenate((np.stack(indices, 1), overlaps[indices[0], indices[1]][:, None]), 1)
        if num_gts > 1:
            matches = matches[matches[:, 2].argsort()[::-1]]
            matches = matches[np.unique(matches[:, 1], return_index=True)[1]]
            matches = matches[matches[:, 2].argsort()[::-1]]
            matches = matches[np.unique(matches[:, 0], return_index=True)[1]]
    else:
        matches = np.zeros((0, 3))
    return matches


def get_det_matched_gt_inds(overlaps, thresh):
    num_gts, num_dets = overlaps.shape
    det_matched_gt_inds = np.full((num_dets, ), -1, dtype=np.long)
    if num_gts == 0 or num_dets == 0:
        return det_matched_gt_inds

    # for each det, which gt best overlaps with it and the max overlap ratio of all gts
    argmax_overlaps_foreach_det = np.argmax(overlaps, axis=0)
    max_overlaps_foreach_det = overlaps[argmax_overlaps_foreach_det, np.arange(num_dets)]
    foreground_indices = max_overlaps_foreach_det >= thresh
    det_matched_gt_inds[foreground_indices] = argmax_overlaps_foreach_det[foreground_indices]

    overlaps_new = csr_matrix((max_overlaps_foreach_det[foreground_indices], 
                               (argmax_overlaps_foreach_det[foreground_indices], np.nonzero(foreground_indices)[0])), 
                               (num_gts, num_dets))
    argmax_overlaps_foreach_gt = np.argmax(overlaps_new, axis=1)

    gt_matched_det_inds = np.full((num_gts, ), -1, dtype=np.long)
    for det_ind, gt_ind in enumerate(det_matched_gt_inds):
        if gt_ind != -1 and argmax_overlaps_foreach_gt[gt_ind] == det_ind:
            gt_matched_det_inds[gt_ind] = det_ind
    det_matched_gt_inds[:] = -1
    for gt_ind, det_ind in enumerate(gt_matched_det_inds):
        if det_ind != -1 :
            det_matched_gt_inds[det_ind] = gt_ind

    return det_matched_gt_inds


def get_confusion_matrix_by_matches(matches, gt_labels, det_labels, num_classes):
    """Adapted from current implementation of `ConfusionMatrix`
    """
    matrix = np.zeros((num_classes + 1, num_classes + 1), dtype=np.long)
    num_matches = matches.shape[0]
    gt_indices, det_indices, _ = matches.transpose().astype(np.int16)
    for i, gt_label in enumerate(gt_labels):
        j = (i == gt_indices)
        if (num_matches > 0) and (sum(j) == 1):
            matrix[det_labels[det_indices[j]], gt_label] += 1
        else:
            matrix[num_classes, gt_label] += 1  # background FP

    # if num_matches > 0:
    for i, det_label in enumerate(det_labels):
        if not any(det_indices == i):
            matrix[det_label, num_classes] += 1  # background FN
    return matrix


def get_confusion_matrix_by_inds(det_matched_gt_inds, gt_labels, det_labels, num_classes):
    matrix = np.zeros((num_classes + 1, num_classes + 1), dtype=np.long)
    for det_ind, gt_ind in enumerate(det_matched_gt_inds):
        if gt_ind != -1:
            matrix[det_labels[det_ind], gt_labels[gt_ind]] += 1
        else:
            matrix[ det_labels[det_ind], num_classes] += 1

    gt_matched_det_inds = np.full((len(gt_labels), ), -1, dtype=np.long)
    for det_ind, gt_ind in enumerate(det_matched_gt_inds):
        if gt_ind != -1:
            gt_matched_det_inds[gt_ind] = det_ind
        
    for gt_ind, det_ind in enumerate(gt_matched_det_inds):
        if det_ind == -1:
            matrix[num_classes, gt_labels[gt_ind]] += 1
    return matrix


def convert_to_det_matched_gt_inds(matches, num_dets):
    det_matched_gt_inds = np.full((num_dets, ), -1, dtype=np.long)
    for k in range(len(matches)):
        det_matched_gt_inds[int(matches[k, 1])] = int(matches[k, 0])
    return det_matched_gt_inds


if __name__ == '__main__':
    num_classes = 5
    num_gts, num_dets = 1000, 1000

    overlaps = np.random.randn(num_gts, num_dets)
    start_time = time.time()
    matches1 = get_matches(overlaps, 0)
    print(time.time() - start_time)
    matched_inds1 = convert_to_det_matched_gt_inds(matches1, num_dets)
    start_time = time.time()
    matched_inds2 = get_det_matched_gt_inds(overlaps, 0)
    print(time.time() - start_time)
    print(np.allclose(matched_inds1, matched_inds2))
    print('======================')

    gt_labels = np.random.randint(num_classes, size=num_gts)
    det_labels = np.random.randint(num_classes, size=num_dets)
    start_time = time.time()
    confmat1 = get_confusion_matrix_by_matches(matches1, gt_labels, det_labels, num_classes)
    print(time.time() - start_time)
    start_time = time.time()
    confmat2 = get_confusion_matrix_by_inds(matched_inds2, gt_labels, det_labels, num_classes)
    print(time.time() - start_time)
    print(np.allclose(confmat1, confmat2))
    print('======================')
```

