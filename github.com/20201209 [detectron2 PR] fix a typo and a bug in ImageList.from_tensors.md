## [fix a typo and a bug in ImageList.from_tensors](https://github.com/facebookresearch/detectron2/pull/2358)

In `ImageList.from_tensors`, shape of each item in `tensors` is (Hi, Wi) or (C_1, ..., C_K, Hi, Wi) where K >= 1 according to the docstring, and from the following code, we can conclude that each item in `tensors` must have the same shape besides width and height (i.e. the last two dimension).

https://github.com/facebookresearch/detectron2/blob/f7b394e059702341c5eb8db2b9a0534779826b4c/detectron2/structures/image_list.py#L117-L121
```python
# max_size can be a tensor in tracing mode, therefore convert to list
batch_shape = [len(tensors)] + list(tensors[0].shape[:-2]) + list(max_size)
batched_imgs = tensors[0].new_full(batch_shape, pad_value)
for img, pad_img in zip(tensors, batched_imgs):
    pad_img[..., : img.shape[-2], : img.shape[-1]].copy_(img)
```
Accordingly, 
https://github.com/facebookresearch/detectron2/blob/f7b394e059702341c5eb8db2b9a0534779826b4c/detectron2/structures/image_list.py#L89-L91
```python
for t in tensors:
    assert isinstance(t, torch.Tensor), type(t)
    assert t.shape[1:-2] == tensors[0].shape[1:-2], t.shape
```
should be 
```python
for t in tensors:
    assert isinstance(t, torch.Tensor), type(t)
    assert t.shape[:-2] == tensors[0].shape[:-2], t.shape
```
In addition, there is a typo in docstring in `ImageList.from_tensors`, and this PR fix it.

For your information.


## 遇到问题
```facebook-github-bot commented 19 minutes ago
Hi @quarrying!

Thank you for your pull request and welcome to our community. We require contributors to sign our Contributor License Agreement, and we don't seem to have you on file.

In order for us to review and merge your code, please sign at https://code.facebook.com/cla. If you are contributing on behalf of someone else (eg your employer), the individual CLA may not be sufficient and your employer may need to sign the corporate CLA.

If you have received this in error or have any questions, please contact us at cla@fb.com. Thanks!
```
需要翻墙签一个 Contributor License Agreement, 于是找到了 <https://github.com/getlantern/download>.


## detectron2 的 PR template
`.github/pull_request_template.md` 文件中

```
Thanks for your contribution!

If you're sending a large PR (e.g., >50 lines),
please open an issue first about the feature / bug, and indicate how you want to contribute.

We do not always accept features.
See https://detectron2.readthedocs.io/notes/contributing.html#pull-requests about how we handle PRs.

Before submitting a PR, please run `dev/linter.sh` to lint the code.
```

## Facebook, Inc. Individual Contributor License Agreement
```
Facebook, Inc. Individual Contributor License Agreement ("Agreement"), v1.0

You accept and agree to the following terms and conditions for Your present and future Contributions submitted to Facebook, Inc. ("Facebook"). Except for the license granted herein to Facebook and recipients of software distributed by Facebook, You reserve all right, title, and interest in and to Your Contributions.

1. Definitions.

"You" (or "Your") shall mean the copyright owner or legal entity authorized by the copyright owner that is making this Agreement with Facebook. For legal entities, the entity making a Contribution and all other entities that control, are controlled by, or are under common control with that entity are considered to be a single Contributor. For the purposes of this definition, "control" means (i) the power, direct or indirect, to cause the direction or management of such entity, whether by contract or otherwise, or (ii) ownership of fifty percent (50%) or more of the outstanding shares, or (iii) beneficial ownership of such entity.

"Contribution" shall mean any original work of authorship, including any modifications or additions to an existing work, that is intentionally submitted by You to Facebook for inclusion in, or documentation of, any of the products owned or managed by Facebook (the "Work"). For the purposes of this definition, "submitted" means any form of electronic, verbal, or written communication sent to Facebook or its representatives, including but not limited to communication on electronic mailing lists, source code control systems, and issue tracking systems that are managed by, or on behalf of, Facebook for the purpose of discussing and improving the Work, but excluding communication that is conspicuously marked or otherwise designated in writing by You as "Not a Contribution."

2. Grant of Copyright License. Subject to the terms and conditions of this Agreement, You hereby grant to Facebook and to recipients of software distributed by Facebook a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare derivative works of, publicly display, publicly perform, sublicense, and distribute Your Contributions and such derivative works.

3. Grant of Patent License. Subject to the terms and conditions of this Agreement, You hereby grant to Facebook and to recipients of software distributed by Facebook a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable (except as stated in this section) patent license to make, have made, use, offer to sell, sell, import, and otherwise transfer the Work, where such license applies only to those patent claims licensable by You that are necessarily infringed by Your Contribution(s) alone or by combination of Your Contribution(s) with the Work to which such Contribution(s) was submitted. If any entity institutes patent litigation against You or any other entity (including a cross-claim or counterclaim in a lawsuit) alleging that your Contribution, or the Work to which you have contributed, constitutes direct or contributory patent infringement, then any patent licenses granted to that entity under this Agreement for that Contribution or Work shall terminate as of the date such litigation is filed.

4. You represent that you are legally entitled to grant the above license. If your employer(s) has rights to intellectual property that you create that includes your Contributions, you represent that you have received permission to make Contributions on behalf of that employer, that your employer has waived such rights for your Contributions to Facebook, or that your employer has executed a separate Corporate CLA with Facebook.

5. You represent that each of Your Contributions is Your original creation (see section 7 for submissions on behalf of others). You represent that Your Contribution submissions include complete details of any third-party license or other restriction (including, but not limited to, related patents and trademarks) of which you are personally aware and which are associated with any part of Your Contributions.

6. You are not expected to provide support for Your Contributions, except to the extent You desire to provide support. You may provide support for free, for a fee, or not at all. Unless required by applicable law or agreed to in writing, You provide Your Contributions on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON- INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE.

7. Should You wish to submit work that is not Your original creation, You may submit it to Facebook separately from any Contribution, identifying the complete details of its source and of any license or other restriction (including, but not limited to, related patents, trademarks, and license agreements) of which you are personally aware, and conspicuously marking the work as "Submitted on behalf of a third-party: [named here]".

8. You agree to notify Facebook of any facts or circumstances of which you become aware that would make these representations inaccurate in any respect.
```


