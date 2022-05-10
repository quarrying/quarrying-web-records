>
>
> On Fri, May 28, 2021 at 4:58 PM <kangkai at mail.ustc.edu.cn 
> <mailto:kangkai at mail.ustc.edu.cn>> wrote:
>
>     Hi all,
>
>     Finding topk elements is widely used in several fields, but missed
>     in NumPy.
>     I implement this functionality named as  numpy.topk using core numpy
>     functions and open a PR:
>
>     https://github.com/numpy/numpy/pull/19117
>     <https://github.com/numpy/numpy/pull/19117>
>
>     Any discussion are welcome.
>
>
> Thanks for the proposal Kang. I think this functionality is indeed a 
> fairly obvious gap in what Numpy offers, and would make sense to add. 
> A detailed comparison with other libraries would be very helpful here. 
> TensorFlow and JAX call this function `top_k`, while PyTorch, Dask and 
> MXNet call it `topk`.
>
> Two things to look at in more detail here are:
> 1. complete signatures of the function in each of those libraries, and 
> what the commonality is there.
> 2. the argument Eric made on your PR about consistency with 
> sort/argsort, and if we want topk/argtopk? Also, do other libraries 
> have `argtopk`?
>
> Cheers,
> Ralf
>
>
>     Best wishes,
>
>     Kang Kai
>

Hi, Thanks for reply, I present some details below: 

## 1. complete signatures of the function in each of those libraries, and what the commonality is there.

| Library     | Name               | arg1  | arg2 | arg3 | arg4      | arg5   |
|-------------|--------------------|-------|------|------|-----------|--------|
| NumPy [1]   | numpy.topk         | a     | k    | axis | largest   | sorted |
| PyTorch [2] | torch.topk         | input | k    | dim  | largest   | sorted |
| R [3]       | topK               | x     | K    | /    | /         | /      |
| MXNet [4]   | mxnet.npx.topk     | data  | k    | axis | is_ascend | /      |
| CNTK [5]    | cntk.ops.top_k     | x     | k    | axis | /         | /      |
| TF [6]      | tf.math.top_k      | input | k    | /    | /         | sorted |
| Dask [7]    | dask.array.topk    | a     | k    | axis | -k        | /      |
| Dask [8]    | dask.array.argtopk | a     | k    | axis | -k        | /      |
| MATLAB [9]  | mink               | A     | k    | dim  | /         | /      |
| MATLAB [10] | maxk               | A     | k    | dim  | /         | /      |


| Library     | Name               | Returns             | 
|-------------|--------------------|---------------------| 
| NumPy [1]   | numpy.topk         | values, indices     | 
| PyTorch [2] | torch.topk         | values, indices     | 
| R [3]       | topK               | indices             | 
| MXNet [4]   | mxnet.npx.topk     | controls by ret_typ | 
| CNTK [5]    | cntk.ops.top_k     | values, indices     | 
| TF [6]      | tf.math.top_k      | values, indices     | 
| Dask [7]    | dask.array.topk    | values              | 
| Dask [8]    | dask.array.argtopk | indices             | 
| MATLAB [9]  | mink               | values, indices     |
| MATLAB [10] | maxk               | values, indices     |

- arg1: Input array.
- arg2: Number of top elements to look for along the given axis.
- arg3: Axis along which to find topk.
    - R only supports vector, TensorFlow only supports axis=-1.
- arg4: Controls whether to return k largest or smallest elements.
    - R, CNTK and TensorFlow only return k largest elements.
    - In Dask, k can be negative, which means to return k smallest elements.
    - In MATLAB, use two distinct functions.
- arg5: If true the resulting k elements will be sorted by the values.
    - R, MXNet, CNTK, Dask and MATLAB only return sorted elements.
    
**Summary**:
- Function Name: could be `topk`, `top_k`, `mink`/`maxk`.
- arg1 (a), arg2 (k), arg3 (axis): should be required.
- arg4 (largest), arg4 (sorted): might be discussed.
- Returns: discussed below.

## 2. the argument Eric made on your PR about consistency with sort/argsort, if we want topk/argtopk? Also, do other libraries have `argtopk`

In most libraries, `topk` or `top_k` returns both values and indices, and 
`argtopk` is not included except for Dask. In addition, there is another 
inconsistency: `sort` returns ascending values, but `topk` returns 
descending values.

## Suggestions
Finally, IMHO, new function signature might be designed as one of:
I) use `topk` / `argtopk` or `top_k` / `argtop_k`
```python
def topk(a, k, axis=-1, sorted=True) -> topk_values
def argtopk(a, k, axis=-1, sorted=True) -> topk_indices
```
or
```python
def top_k(a, k, axis=-1, sorted=True) -> topk_values
def argtop_k(a, k, axis=-1, sorted=True) -> topk_indices
```
where `k` can be negative which means to return k smallest elements.

II) use `maxk` / `argmaxk` or `max_k` / `argmax_k` 
(`mink` / `argmink` or `min_k` / `argmin_k`)
```python
def maxk(a, k, axis=-1, sorted=True) -> values
def argmaxk(a, k, axis=-1, sorted=True) -> indices

def mink(a, k, axis=-1, sorted=True) -> values
def argmink(a, k, axis=-1, sorted=True) -> indices
```
or
```python
def max_k(a, k, axis=-1, sorted=True) -> values
def argmax_k(a, k, axis=-1, sorted=True) -> indices

def min_k(a, k, axis=-1, sorted=True) -> values
def argmin_k(a, k, axis=-1, sorted=True) -> indices
```
where `k` must be positive.


**References**:
- [1] https://github.com/numpy/numpy/pull/19117
- [2] https://pytorch.org/docs/stable/generated/torch.topk.html
- [3] https://www.rdocumentation.org/packages/tensr/versions/1.0.1/topics/topK
- [4] https://mxnet.apache.org/versions/master/api/python/docs/api/npx/generated/mxnet.npx.topk.html
- [5] https://docs.microsoft.com/en-us/python/api/cntk/cntk.ops?view=cntk-py-2.7#top-k-x--k--axis--1--name----
- [6] https://tensorflow.google.cn/api_docs/python/tf/math/top_k?hl=zh-cn
- [7] https://docs.dask.org/en/latest/array-api.html?highlight=topk#dask.array.topk
- [8] https://docs.dask.org/en/latest/array-api.html?highlight=topk#dask.array.argtopk
- [9] https://nl.mathworks.com/help/matlab/ref/maxk.html
- [10] https://nl.mathworks.com/help/matlab/ref/mink.html
- 

