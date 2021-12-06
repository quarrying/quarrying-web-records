# SSE 系列内置函数中的 shuffle 函数

> 首发链接: <https://www.cnblogs.com/quarryman/p/sse_shuffle.html>

这份博文总结了 SSE 系列内置函数中与 shuffle 有关的宏和函数。分析验证了 `_mm_shuffle_epi16` 存在的可能性，并利用 `_mm_shuffle_epi8` 实现了该函数。

下面是 SSE 系列内置函数中与 shuffle 有关的 intrinsic 函数: 
```c++
// Integer shuffle, SSE
extern __m64 _mm_shuffle_pi16(__m64 _A, int _Imm);

// SP FP shuffle, SSE
extern __m128 _mm_shuffle_ps(__m128 _A, __m128 _B, unsigned int _Imm);

// DP FP shuffle, SSE2
extern __m128d _mm_shuffle_pd(__m128d _A, __m128d _B, int _Imm);

// Integer shuffle, SSE2
extern __m128i _mm_shuffle_epi32(__m128i _A, int _Imm);
extern __m128i _mm_shufflehi_epi16(__m128i _A, int _Imm);
extern __m128i _mm_shufflelo_epi16(__m128i _A, int _Imm);

// Integer shuffle, SSSE3
extern __m128i _mm_shuffle_epi8 (__m128i a, __m128i b);
extern __m64 _mm_shuffle_pi8 (__m64 a, __m64 b);
```


## 1. `_mm_shuffle_pd` 和 `_MM_SHUFFLE2`
可以使用 `_MM_SHUFFLE2` 来构造 `_mm_shuffle_pd` 中的参数 `_Imm`, `_MM_SHUFFLE2` 是 `SSE2` 中定义的一个宏, 定义如下
```c++
#define _MM_SHUFFLE2(x,y) (((x)<<1) | (y))
```
因为 `__m128d` 能容纳 2 个 `DP FP` (双精度浮点数) , 所以 `x,y` 的取值集合为 `{0, 1}`, `_MM_SHUFFLE2(x,y)` 的最大值为 
```
(((1)<<1) | (1)) == 3 <= 2^32 - 1
```
显然可以用 `int` 来表示立即数 `_Imm`.

----

## 2. `_mm_shuffle_ps` 和 `_MM_SHUFFLE`
可以使用 `_MM_SHUFFLE` 来构造 `_mm_shuffle_ps` 中的参数 `_Imm`, `_MM_SHUFFLE` 是 `SSE` 中定义的一个宏, 定义如下
```c++
#define _MM_SHUFFLE(fp3, fp2, fp1, fp0) (((fp3) << 6) | ((fp2) << 4) | \
                                        ((fp1) << 2) | ((fp0)))
```
因为 `__m128` 能容纳 4 个 `SP FP` (单精度浮点数) , 所以 `fp3, fp2, fp1, fp0` 的取值集合为 `{0, 1, 2, 3}`,  `_MM_SHUFFLE(fp3, fp2, fp1, fp0)` 的最大值为
```
(((3) << 6) | ((3) << 4) | ((3) << 2) | ((3))) == 255 == 2^8 - 1 <= 2^32 - 1
```
显然可以用 `unsigned int` 来表示立即数 `_Imm`.

注意:  文档和代码注释中只说到使用 `_MM_SHUFFLE` 来构造 `_mm_shuffle_ps` 中的参数 `_Imm`, 实际上除了 `_mm_shuffle_ps`, 上面的 `_mm_shuffle_pi16`, `_mm_shuffle_epi32`, `_mm_shufflehi_epi16`, `_mm_shufflelo_epi16`, 都可以使用 `_MM_SHUFFLE` 来构造 `_Imm`.

----

## 3. `_mm_shuffle_epi16` 和 `_MM_SHUFFLE8`
`SSE` 系列内置函数中并没有定义 `_mm_shuffle_epi16`, 而是定义了 `_mm_shufflehi_epi16`, `_mm_shufflelo_epi16`.

我们不妨定义 `__m128i _mm_shuffle_epi16(__m128i _A, int _Imm);`, 且定义 `_MM_SHUFFLE8` 来构造第二个参数 `_Imm`, 定义如下
```c++
#define _MM_SHUFFLE8(fp7, fp6, fp5, fp4, fp3, fp2, fp1, fp0)\
        (((fp7) << 21) | ((fp6) << 18) | ((fp5) << 15) | ((fp4) << 12)) |\
        (((fp3) << 9) | ((fp2) << 6) | ((fp1) << 3) | ((fp0)))
```
因为 `__m128i` 能容纳 8 个 16 位整型数据, 所以`fp7, fp6, fp5, fp4, fp3, fp2, fp1, fp0` 的取值集合为 `{0, 1, 2, 3, 4, 5, 6, 7}`, 则 `_MM_SHUFFLE8(fp7, fp6, fp5, fp4, fp3, fp2, fp1, fp0)` 的最大值为
```
(((7) << 21) | ((7) << 18) | ((7) << 15) | ((7) << 12)) | 
(((7) << 9) | ((7) << 6) | ((7) << 3) | ((7))) == 16777215 == 2^24 - 1 <= 2^32 - 1
```
所以上面定义的 `_mm_shuffle_epi16` 理论上是可行的, 然而 SSE 系列内置函数中却没有这个函数, 我的猜测是:
`_mm_shufflehi_epi16`, `_mm_shufflelo_epi16` 可以使用 `_MM_SHUFFLE` 构造立即数 `_Imm`, 而要实现 `_mm_shuffle_epi16`, 还要配套实现 `_MM_SHUFFLE8`, 开发人员容易弄混各种 `shuffle` 相关的宏和函数.实际上, 可以利用 `_mm_shufflehi_epi16` 和 `_mm_shufflelo_epi16` 来实现 `_mm_shuffle_epi16`( 可能比较麻烦）, 也可以利用 SSSE3 中的 `_mm_shuffle_epi8` 来实现 `_mm_shuffle_epi16`.

### 3.1 代码一,  利用 `_mm_shuffle_epi8` 实现 `_mm_shuffle_epi16`
```c++
#include <stdio.h>
#include <emmintrin.h>
#include <tmmintrin.h>

#define _MM_SHUFFLE8(fp7, fp6, fp5, fp4, fp3, fp2, fp1, fp0)\
    (((fp7) << 21) | ((fp6) << 18) | ((fp5) << 15) | ((fp4) << 12)) | \
    (((fp3) << 9) | ((fp2) << 6) | ((fp1) << 3) | ((fp0)))

__m128i _mm_shuffle_epi16(__m128i _A, int _Imm)
{
    _Imm &= 0xffffff;
    char m01 = (_Imm >> 0) & 0x7, m03 = (_Imm >> 3) & 0x7;
    char m05 = (_Imm >> 6) & 0x7, m07 = (_Imm >> 9) & 0x7;
    char m09 = (_Imm >> 12) & 0x7, m11 = (_Imm >> 15) & 0x7;
    char m13 = (_Imm >> 18) & 0x7, m15 = (_Imm >> 21) & 0x7;
    m01 <<= 1; m03 <<= 1; m05 <<= 1; m07 <<= 1;
    m09 <<= 1; m11 <<= 1; m13 <<= 1; m15 <<= 1;
    char m00 = m01 + 1, m02 = m03 + 1, m04 = m05 + 1, m06 = m07 + 1;
    char m08 = m09 + 1, m10 = m11 + 1, m12 = m13 + 1, m14 = m15 + 1;
    
    //__m128i vMask = _mm_set_epi8(m00, m01, m02, m03, m04, m05, m06, m07,
    //  m08, m09, m10, m11, m12, m13, m14, m15);
    __m128i vMask = _mm_set_epi8(m14, m15, m12, m13, m10, m11, m08, m09,
        m06, m07, m04, m05, m02, m03, m00, m01);
    return _mm_shuffle_epi8(_A, vMask);
}

void icvPrintM128i_16s(const __m128i& v)
{
    printf("(%d, %d, %d, %d, %d, %d, %d, %d)",
        v.m128i_i16[0], v.m128i_i16[1], v.m128i_i16[2], v.m128i_i16[3],
        v.m128i_i16[4], v.m128i_i16[5], v.m128i_i16[6], v.m128i_i16[7]);
}

int main()
{
    __m128i val = _mm_setr_epi16(0, 1, 2, 3, 4, 5, 6, 7);
    icvPrintM128i_16s(val);
    val = _mm_shuffle_epi16(val, _MM_SHUFFLE8(1, 2, 3, 5, 4, 7, 6, 0));
    icvPrintM128i_16s(val);
    getchar();

    return 0;
}
```

## 4. `_mm_shuffle_epi8`
注意到 `_mm_shuffle_epi8` 的第二个参数使用的是 `__m128i`, 而不是 `int` 或 `unsigned int`. 可以同理得到第二个参数理论上的最大值: 
```
(((15) << 60) | ((15) << 56) | ((15) << 52) | ((15) << 48)) | 
(((15) << 44) | ((15) << 40) | ((15) << 36) | ((15) << 32)) | 
(((15) << 28) | ((15) << 24) | ((15) << 20) | ((15) << 16)) | 
(((15) << 12) | ((15) << 8) | ((15) << 4) | ((15))) == 2**64 - 1
```
所以不能用 32 位整型表示, 却能用 128 位的 `__m128i` 表示.

