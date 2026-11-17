"""將無畸變像素反投影到指定平面。"""
# NumPy 用於求解相機射線、矩陣轉換與向量運算。
import numpy as np


def pixel_to_plane(pixel, K, R, t, normal, offset, *, tolerance=1e-12):
    """R、t 將相機座標轉成世界座標。平面定義為 normal·p + offset = 0。"""
    origin = np.asarray(t, dtype=float)
    normal = np.asarray(normal, dtype=float)
    norm = np.linalg.norm(normal)
    if norm == 0:
        raise ValueError("平面法向量必須非零")
    normal = normal / norm
    offset = offset / norm

    direction = np.asarray(R) @ np.linalg.solve(K, [*pixel, 1.0])
    direction = direction / np.linalg.norm(direction)
    denominator = normal @ direction
    if abs(denominator) <= tolerance:
        return None

    distance = -(normal @ origin + offset) / denominator
    if distance < 0:
        return None
    return origin + distance * direction


if __name__ == "__main__":
    # 虛構針孔相機與平面，世界座標方向與相機方向相同。
    K = np.array([[100, 0, 50], [0, 100, 40], [0, 0, 1]])
    print(pixel_to_plane((70, 40), K, np.eye(3), (0, 0, 0), (0, 0, 1), -5))
