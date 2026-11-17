"""整合多張影像的偵測結果，估計色帶中心。"""
# NumPy 用於計算中心點的中位數與距離。
import numpy as np

# 匯入色帶偵測函式與範例影像產生函式。
from detect_bar import detect_candidates, synthetic_image


def estimate_center(frames, detector, *, max_distance, min_inliers):
    """以座標中位數排除離群中心。距離單位為像素。"""
    if max_distance < 0 or min_inliers < 1:
        raise ValueError("距離須非負，最少一致幀數須為正")

    centers = []
    for frame in frames:
        candidates = detector(frame)
        if candidates:
            centers.append(candidates[0]["center"])

    if len(centers) < min_inliers:
        return None

    points = np.asarray(centers, dtype=float)
    median = np.median(points, axis=0)
    distances = np.linalg.norm(points - median, axis=1)
    inliers = points[distances <= max_distance]
    if len(inliers) < min_inliers:
        return None
    return tuple(map(float, np.median(inliers, axis=0)))


if __name__ == "__main__":
    def detect(image):
        return detect_candidates(image, (50, 150, 100), (70, 255, 255),
                                 min_area=100, min_aspect=3)

    # 四張合成影像，最後一張的色帶故意偏離。
    frames = [synthetic_image(x, 25) for x in (20, 21, 19, 75)]
    print(estimate_center(frames, detect, max_distance=3, min_inliers=3))
