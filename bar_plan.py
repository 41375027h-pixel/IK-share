"""平面二連桿逆運動學與座標轉換。角度一律使用弧度。"""
# math 提供三角函式、角度換算與距離計算。
from math import acos, atan2, cos, degrees, hypot, pi, sin


def wrap(angle):
    return (angle + pi) % (2 * pi) - pi


def world_to_base(point, origin, heading):
    """heading 為基座 x 軸在世界平面上的方向。"""
    dx, dy = point[0] - origin[0], point[1] - origin[1]
    c, s = cos(heading), sin(heading)
    return c * dx + s * dy, -s * dx + c * dy


def solve_ik(target, L1, L2, *, tolerance=1e-12):
    """回傳候選 (肩角, 肘角)。空清單表示不可達。"""
    if L1 <= 0 or L2 <= 0:
        raise ValueError("連桿長度必須為正")
    x, y = target
    radius = hypot(x, y)
    if radius == 0 and L1 == L2:
        # 肩角任意，回傳一組代表解。
        return [(0.0, -pi)]
    if radius < abs(L1 - L2) or radius > L1 + L2:
        return []
    c2 = (radius**2 - L1**2 - L2**2) / (2 * L1 * L2)
    bend = acos(max(-1.0, min(1.0, c2)))
    elbows = (bend,) if min(bend, pi - bend) <= tolerance else (bend, -bend)
    solutions = []
    for elbow in elbows:
        shoulder = atan2(y, x) - atan2(L2 * sin(elbow), L1 + L2 * cos(elbow))
        solutions.append((wrap(shoulder), wrap(elbow)))
    return solutions


if __name__ == "__main__":
    # 匯入正向運動學函式，用於驗證範例的 IK 解。
    from model_v3 import forward_kinematics

    # 虛構尺寸與座標，長度採用任意一致單位。
    L1, L2 = 3.0, 2.0
    target = world_to_base((13, 7), (10, 5), 0.0)
    for angles in solve_ik(target, L1, L2):
        endpoint = forward_kinematics(*angles, L1, L2)
        error = hypot(endpoint[0] - target[0], endpoint[1] - target[1])
        print(tuple(round(degrees(a), 4) for a in angles), "FK 誤差", error)
