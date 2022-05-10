## [optimize `mmcv.image.geometric.bbox_scaling`](https://github.com/open-mmlab/mmcv/pull/754)
Hi, this PR updates `mmcv.image.geometric.bbox_scaling` to make it faster. The following is the test code, FYI.

Note: `bbox_scaling` is adapted from `mmcv.image.geometric.bbox_scaling`, `bbox_scaling_v2` is the updated implementation. For simplicity, two functions don't include `clip_shape` argument here. 

```python
import time
import numpy as np


def bbox_scaling(bboxes, scale):
    """Scaling bboxes w.r.t the box center.

    Args:
        bboxes (ndarray): Shape(..., 4).
        scale (float): Scaling factor.

    Returns:
        ndarray: Scaled bboxes.
    """
    if float(scale) == 1.0:
        scaled_bboxes = bboxes.copy()
    else:
        w = bboxes[..., 2] - bboxes[..., 0] + 1
        h = bboxes[..., 3] - bboxes[..., 1] + 1
        dw = (w * (scale - 1)) * 0.5
        dh = (h * (scale - 1)) * 0.5
        scaled_bboxes = bboxes + np.stack((-dw, -dh, dw, dh), axis=-1)
    return scaled_bboxes


def bbox_scaling_v2(bboxes, scale):
    """Scaling bboxes w.r.t the box center.

    Args:
        bboxes (ndarray): Shape(..., 4).
        scale (float): Scaling factor.

    Returns:
        ndarray: Scaled bboxes.
    """
    scaled_bboxes = bboxes.copy()
    if float(scale) != 1.0:
        factor = (scale - 1) * 0.5

        x_deltas = bboxes[..., 2] - bboxes[..., 0]
        y_deltas = bboxes[..., 3] - bboxes[..., 1]
        x_deltas += 1
        y_deltas += 1
        x_deltas *= factor
        y_deltas *= factor
        
        scaled_bboxes[..., 0] -= x_deltas
        scaled_bboxes[..., 1] -= y_deltas
        scaled_bboxes[..., 2] += x_deltas
        scaled_bboxes[..., 3] += y_deltas

    return scaled_bboxes


def benchmark(func, num_repeats=100, num_repeats_burn_in=0, display_interval=None):
    assert isinstance(num_repeats, int) and (num_repeats > 0)
    assert isinstance(num_repeats_burn_in, int) and (num_repeats_burn_in >= 0)
    assert isinstance(display_interval, int) or (display_interval is None)
    # assert num_repeats > num_repeats_burn_in
    
    duration_list = []
    for i in range(num_repeats + num_repeats_burn_in):
        start_time = time.time()
        output = func()
        duration = time.time() - start_time
        if i >= num_repeats_burn_in:
            duration_list.append(duration)
            actual_repeat = i - num_repeats_burn_in + 1
            if (display_interval is not None) and (actual_repeat % display_interval == 0):
                print('repeat {}, duration = {:.3f}s'.format(actual_repeat, duration))
    time_summary = {
        'total': np.sum(duration_list),
        'mean': np.mean(duration_list),
        'stddev': np.std(duration_list),
        'max': np.max(duration_list),
        'min': np.min(duration_list),
    }
    return output, time_summary


if __name__ == '__main__':
    num_repeats = 1000
    bboxes = np.random.randn(200000, 4).astype(np.float32)
    ret_bboxes1, tm1 = benchmark(lambda: bbox_scaling(bboxes.copy(), 2.5), num_repeats=num_repeats)
    ret_bboxes2, tm2 = benchmark(lambda: bbox_scaling_v2(bboxes.copy(), 2.5), num_repeats=num_repeats)
    print(np.allclose(ret_bboxes1, ret_bboxes2))
    print(tm1)
    print(tm2)

```

## 遇到问题
```
Thank you for your submission! We really appreciate it. Like many open source projects, we ask that you sign our Contributor License Agreement before we can accept your contribution.
You have signed the CLA already but the status is still pending? Let us recheck it.
```
同样需要签署 CLA.


## OpenMMLab Contributor License Agreement
```
OpenMMLab Contributor License Agreement
In order to clarify the intellectual property license granted with Contributions from any person or entity, the open source project OpenMMLab ("OpenMMLab") must have a Contributor License Agreement (CLA) on file that has been signed by each Contributor, indicating agreement to the license terms below. This license is for your protection as a Contributor as well as the protection of OpenMMLab and its users; it does not change your rights to use your own Contributions for any other purpose.

You accept and agree to the following terms and conditions for Your present and future Contributions submitted to OpenMMLab. Except for the license granted herein to OpenMMLab and recipients of software distributed by OpenMMLab, You reserve all right, title, and interest in and to Your Contributions.

Definitions.

"You" (or "Your") shall mean the copyright owner or legal entity authorized by the copyright owner that is making this Agreement with OpenMMLab. For legal entities, the entity making a Contribution and all other entities that control, are controlled by, or are under common control with that entity are considered to be a single Contributor. For the purposes of this definition, "control" means (i) the power, direct or indirect, to cause the direction or management of such entity, whether by contract or otherwise, or (ii) ownership of fifty percent (50%) or more of the outstanding shares, or (iii) beneficial ownership of such entity.

"Contribution" shall mean any original work of authorship, including any modifications or additions to an existing work, that is intentionally submitted by You to OpenMMLab for inclusion in, or documentation of, any of the products owned or managed by OpenMMLab (the "Work"). For the purposes of this definition, "submitted" means any form of electronic, verbal, or written communication sent to OpenMMLab or its representatives, including but not limited to communication on electronic mailing lists, source code control systems, and issue tracking systems that are managed by, or on behalf of, OpenMMLab for the purpose of discussing and improving the Work, but excluding communication that is conspicuously marked or otherwise designated in writing by You as "Not a Contribution."

Grant of Copyright License. Subject to the terms and conditions of this Agreement, You hereby grant to OpenMMLab and to recipients of software distributed by OpenMMLab a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare derivative works of, publicly display, publicly perform, sublicense, and distribute Your Contributions and such derivative works.

Grant of Patent License. Subject to the terms and conditions of this Agreement, You hereby grant to OpenMMLab and to recipients of software distributed by OpenMMLab a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable (except as stated in this section) patent license to make, have made, use, offer to sell, sell, import, and otherwise transfer the Work, where such license applies only to those patent claims licensable by You that are necessarily infringed by Your Contribution(s) alone or by combination of Your Contribution(s) with the Work to which such Contribution(s) was submitted. If any entity institutes patent litigation against You or any other entity (including a cross-claim or counterclaim in a lawsuit) alleging that your Contribution, or the Work to which you have contributed, constitutes direct or contributory patent infringement, then any patent licenses granted to that entity under this Agreement for that Contribution or Work shall terminate as of the date such litigation is filed.

You represent that you are legally entitled to grant the above license. If your employer(s) has rights to intellectual property that you create that includes your Contributions, you represent that you have received permission to make Contributions on behalf of that employer, that your employer has waived such rights for your Contributions to OpenMMLab, or that your employer has executed a separate Corporate CLA with OpenMMLab.

You represent that each of Your Contributions is Your original creation (see section 7 for submissions on behalf of others). You represent that Your Contribution submissions include complete details of any third-party license or other restriction (including, but not limited to, related patents and trademarks) of which you are personally aware and which are associated with any part of Your Contributions.

You are not expected to provide support for Your Contributions, except to the extent You desire to provide support. You may provide support for free, for a fee, or not at all. Unless required by applicable law or agreed to in writing, You provide Your Contributions on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON- INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE.

Should You wish to submit work that is not Your original creation, You may submit it to OpenMMLab separately from any Contribution, identifying the complete details of its source and of any license or other restriction (including, but not limited to, related patents, trademarks, and license agreements) of which you are personally aware, and conspicuously marking the work as "Submitted on behalf of a third-party: [named here]".

You agree to notify OpenMMLab of any facts or circumstances of which you become aware that would make these representations inaccurate in any respect.
```


