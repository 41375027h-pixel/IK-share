"""以齊次矩陣串接平面二連桿的正向運動學。"""
# math 提供旋轉矩陣所需的三角函式與圓周率。
from math import cos, pi, sin


def link_transform(angle, length):
    """先在父座標系旋轉，再沿旋轉後的 x 軸平移。"""
    c, s = cos(angle), sin(angle)
    return ((c, -s, length * c), (s, c, length * s), (0, 0, 1))


def forward_kinematics(shoulder, elbow, L1, L2):
    """回傳末端在基座座標中的 (x, y)，角度以弧度輸入。"""
    first = link_transform(shoulder, L1)
    second = link_transform(elbow, L2)
    # 末端在基座中的位置是 (first × second) 的平移欄。
    return tuple(
        sum(first[row][k] * second[k][2] for k in range(3))
        for row in range(2)
    )


if __name__ == "__main__":
    # 虛構連桿。
    print(forward_kinematics(0, pi / 2, 3, 2))
