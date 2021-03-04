#! https://zhuanlan.zhihu.com/p/354129213
# 三维空间下的 Rodrigues 旋转公式
$\vec v$ 按照右手法则绕单位向量 $\vec k$ 旋转 $\theta$ 后的向量记为 $\vec v_{\text{rot}}$, 有: 
$$\begin{aligned}
\vec v_{\text{rot}}
&= \vec v\cos \theta + (\vec k \times \vec v)\sin \theta  + (\vec k \cdot \vec v)\vec k(1 - \cos \theta)\\
&= \vec v + (\vec k \times \vec v)\sin \theta  + \left( \vec k \times (\vec k \times \vec v) \right)(1 - \cos \theta ) \\ 
\end{aligned}$$

其称为 Rodrigues 旋转公式 (罗德里格斯旋转公式). 其中 $\vec k$ 称为旋转轴, $\theta$ 称为旋转角.

## 公式推导
令 $\vec v = \vec v_\parallel + \vec v_\bot$. 其中 $\vec v_\parallel$ 与 $\vec k$ 平行, $\vec v_\bot$ 与 $\vec k$ 垂直. 即 $\vec v_\parallel$ 为 $\vec v$ 在 $\vec k$ 上的射影 (vector projection), $\vec v_\bot$ 为 the vector rejection of $\vec v$ from $\vec k$ ( 暂时没有找到 vector rejection 的贴切翻译).

根据向量到非零向量的投影公式可得, $\vec v_\parallel = \left\langle {\vec v,\vec k} \right\rangle \vec k = (\vec k \cdot \vec v)\vec k$ (注意 $\vec k$ 是单位向量), 
所以 $\vec v_\bot = \vec v - \vec v_\parallel = \vec v - (\vec k \cdot \vec v)\vec k$. 利用拉格朗日公式可以得到  $\vec v_\bot = -\vec k \times (\vec k \times \vec v)$ (根据拉格朗日公式 $\vec a \times \left( {\vec b \times \vec c} \right) = \vec b\left( {\vec a \cdot \vec c} \right) - \vec c\left( {\vec a \cdot \vec b} \right)$, 可以得到 $(\vec k \cdot \vec v)\vec k - \vec v = (\vec k \cdot \vec v)\vec k - \vec v(\vec k \cdot \vec k) = \vec k \times (\vec k \times \vec v)$). 所以

$$\vec v_\parallel = (\vec k \cdot \vec v)\vec k = \vec v + \vec k \times (\vec k \times \vec v)$$
$$\vec v_\bot = \vec v - (\vec k \cdot \vec v)\vec k=-\vec k \times (\vec k \times \vec v)$$

令 $\vec w = \vec k \times \vec v$, 所以 $\vec w = \vec k \times \vec v = \vec k \times (\vec v_\parallel + \vec v_\bot) = \vec k \times \vec v_\bot$, 可见 $\left\| \vec w \right\| = \left\| \vec k \right\| \left\| \vec v_\bot \right\| \sin \left\langle {\vec k,\vec v_\bot} \right\rangle= \left\| \vec v_\bot \right\|$ (因为 $\vec k$ 是单位向量且 $\vec v_\bot$ 与 $\vec k$ 垂直). 

$\vec v_\bot$ 按照右手法则绕单位向量 $\vec k$ (大拇指指的是 $\vec k$ 的方向) 旋转 $\theta$ 后的向量记为 $\vec v_{ \bot \text{rot}}$, 显然有 $\left\| \vec v_{ \bot \text{rot}} \right\| = \left\| \vec v_\bot \right\|$ (旋转是正交变换, 不会改变向量的范数), 所以: 

$$\begin{aligned}
  {\vec v}_{ \bot {\text{rot}}} 
   &= \left\| {\vec v}_{ \bot {\text{rot}}} \right\|\cos \theta {{\vec e}_{{\vec v}_ \bot }} + \left\| {\vec v}_{\bot \text{rot}} \right\|\sin \theta \vec e_{\vec w} \\ 
   &= \left\| \vec v_\bot  \right\| \cos \theta \vec e_{\vec v_\bot } + \left\| {\vec w} \right\|\sin \theta \vec e_{\vec w} \\ 
   &= \vec v_\bot \cos \theta  + \vec w\sin \theta  \\ 
   &= \vec v_\bot \cos \theta  + (\vec k \times \vec v)\sin \theta  \\ 
\end{aligned}$$

上式中 $\vec e_{\vec v_\bot }$ 和 $\vec e_{\vec w}$ 分别表示 $\vec v_\bot$ 和 $\vec w$ 的单位向量.

$\vec v_\parallel$ 不受旋转的影响, 所以 ${\vec v_{\parallel {\text{rot}}}} = \vec v_\parallel$. 于是

$$\begin{aligned}
  {\vec v}_\text{rot} &= {\vec v}_{ \bot {\text{rot}}} + {\vec v}_{\parallel {\text{rot}}} \\&= {\vec v}_{ \bot {\text{rot}}} + {\vec v}_\parallel \\ 
   &= {{\vec v}_ \bot }\cos \theta  + (\vec k \times \vec v)\sin \theta  + {{\vec v}_\parallel } \\ 
   &= \vec v\cos \theta  + (\vec k \times \vec v)\sin \theta  + (\vec k \cdot \vec v)\vec k(1 - \cos \theta ) \\ 
   &= \vec v + (\vec k \times \vec v)\sin \theta  + \left( \vec k \times (\vec k \times \vec v) \right)(1 - \cos \theta ) \\ 
\end{aligned}$$

叉积可以表示为一个反对称矩阵与一个列向量矩阵乘的形式, 例如:

$$\vec k \times \vec v = [\vec k]_\times \vec v = \left[ \begin{matrix}
     0 & -k_z &  k_y \\ 
   k_z &    0 & -k_x \\ 
  -k_y &  k_x &    0 
\end{matrix} \right] \left[ \begin{matrix}
 v_x \\ v_y \\ v_z 
\end{matrix} \right]$$


于是 $\vec v_\text{rot}$ 用矩阵运算则可以表示为: 

$$\begin{aligned}
  {\vec v}_{\text{rot}} 
   &= \vec v\cos \theta  + ({[\vec k]_ \times }\vec v)\sin \theta  + \vec k{{\vec k}^T}\vec v(1 - \cos \theta ) \\ 
   &= \left( {I\cos \theta  + {{[\vec k]}_\times }\sin \theta  + \vec k{{\vec k}^T}(1 - \cos \theta )} \right)\vec v \\ 
\end{aligned}$$

或

$$\begin{aligned}
  {\vec v}_{\text{rot}} 
   &= \vec v + (\vec k \times \vec v)\sin \theta  + \left( \vec k \times (\vec k \times \vec v) \right)(1 - \cos \theta ) \\ 
   &= \left( {I + {{[\vec k]}_ \times }\sin \theta  + {{[\vec k]}_\times^2}(1 - \cos \theta )} \right)\vec v \\ 
\end{aligned}$$

所以旋转轴为 $\vec k$, 旋转角为 $\theta$ 的旋转变换矩阵为: 
$$I\cos \theta  + {[\vec k]_ \times }\sin \theta  + \vec k{\vec k^T}(1 - \cos \theta )$$
或 
$$I + {[\vec k]_ \times }\sin \theta  + {[\vec k]_ \times^2 }(1 - \cos \theta )$$

下面将该旋转变换矩阵记为 $R\left( \vec k, \theta \right)$. 

## 逆公式推导

下面进行逆公式推导, 即由旋转变换矩阵 $R\left( \vec k, \theta \right)$ 到 axis-angle 表示 ($\vec k$ 和 $\theta$) 的推导:

因为 $R\left( \vec k, \theta \right)=I\cos \theta  + {[\vec k]_ \times }\sin \theta  + \vec k{\vec k^T}(1 - \cos \theta )$  且 ${[\vec k]_ \times }$ 是反对称矩阵, 所以
$\begin{aligned}
  \operatorname{tr} \left( R\left( \vec k, \theta \right) \right) 
  &= \operatorname{tr} \left( I \right)\cos \theta  + \operatorname{tr} \left( [\vec k]_\times \right)\sin \theta  + \operatorname{tr} \left( {\vec k{{\vec k}^T}} \right)(1 - \cos \theta ) \\ 
  &= 3\cos \theta  + 1 - \cos \theta  = 2\cos \theta  + 1 \\ 
\end{aligned}$

于是 $\theta  = \arccos \frac{1}{2} \left( {\operatorname{tr} \left( {R\left( {\vec k,\theta } \right)} \right) - 1} \right)$.

又 ${R^T}\left( \vec k,\theta \right) = I \cos \theta  - {[\vec k]_ \times }\sin \theta  + \vec k{\vec k^T}(1 - \cos \theta )$, 于是 $\frac{R - R^T}{2} = [\vec k]_\times\sin \theta$. 再利用上面得到的 $\theta$ 可求得 $[\vec k]_ \times$ 或 $\vec k$.


## 测试代码
```python
"""
作者: 采石工
博客: https://www.zhihu.com/people/quarrying
发布时间: 2021年03月02日
版权声明: 自由分享, 保持署名-非商业用途-非衍生, 知识共享3.0协议.
"""
import cv2
import numpy as np


def Rodrigues(rotation_vector):
    """对应于 OpenCV 中的 Rodrigues
    
    Notes:
        这里仿照 OpenCV 使用旋转向量的范数来表示旋转角度, 而不是用单独的参数来表示旋转角度.
    """
    rotation_vector = rotation_vector.reshape(-1)
    ex, ey, ez = rotation_vector
    norm = np.sqrt(ex ** 2 + ey ** 2 + ez ** 2) + 1e-7
    ex, ey, ez = [x / norm for x in rotation_vector]
    s, c = np.sin(norm), np.cos(norm)
    m1 = np.array([[ex * ex, ex * ey, ex * ez], 
                   [ey * ex, ey * ey, ey * ez],
                   [ex * ez, ey * ez, ez * ez]]);
    m2 = np.array([[c, -ez * s, ey * s], 
                   [ez * s, c, -ex * s],
                   [-ey * s, ex * s, c]]);
    rotation_matrix = (1 - c) * m1 + m2
    return rotation_matrix
    
    
def Rodrigues_inv(rotation_matrix):
    z = (rotation_matrix - rotation_matrix.T) / 2
    rx = z[2, 1]
    ry = -z[2, 0]
    rz = z[1, 0]
    theta = np.arccos((np.sum(np.diag(rotation_matrix)) - 1 ) * 0.5)
    # 注意必须乘以 theta!
    rotation_vector = np.array([rx, ry, rz]) / np.sin(theta) * theta
    return rotation_vector


if __name__ == '__main__':
    # np.random.seed(0)
    rotation_vector = np.random.randn(1, 3)
    print(rotation_vector)
    print('==================================================')
    rotation_matrix_cv, _ = cv2.Rodrigues(rotation_vector)
    print(rotation_matrix_cv)
    rotation_matrix_np = Rodrigues(rotation_vector)
    print(rotation_matrix_np)
    print(np.allclose(rotation_matrix_cv, rotation_matrix_np))
    print('==================================================')
    rotation_vector_cv, _ = cv2.Rodrigues(rotation_matrix_cv)
    print(rotation_vector_cv)
    rotation_vector_np = Rodrigues_inv(rotation_matrix_np)
    print(rotation_vector_np)
    print(np.allclose(rotation_vector.flat, rotation_vector_cv.flat))
    print(np.allclose(rotation_vector.flat, rotation_vector_np.flat))
    print('==================================================')
    
```


## 更新记录
- 20210302, 发布
- 20210304, 简单更新


## 版权声明
版权声明: 自由分享, 保持署名-非商业用途-非衍生, 知识共享3.0协议.

如果你对本文有疑问或建议, 欢迎留言! 转载请保留版权声明! 


