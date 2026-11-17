"""HSV 色帶分割與連通區域篩選。"""
# OpenCV 用於色彩轉換、遮罩、連通區域分析與繪製範例色帶。
import cv2
# NumPy 用於建立範例影像的像素陣列。
import numpy as np


def detect_candidates(image, lower_hsv, upper_hsv, *, min_area, min_aspect):
    """輸入 BGR 影像，回傳依像素面積排序的候選區域。"""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, tuple(lower_hsv), tuple(upper_hsv))
    count, _, stats, centers = cv2.connectedComponentsWithStats(mask)
    candidates = []
    for label in range(1, count):
        x, y, width, height, area = map(int, stats[label])
        aspect = max(width, height) / min(width, height)
        if area >= min_area and aspect >= min_aspect:
            candidates.append({
                "center": tuple(map(float, centers[label])),
                "bounds": (x, y, width, height),
                "area": area,
            })
    return sorted(candidates, key=lambda item: item["area"], reverse=True)


def synthetic_image(x, y):
    """在記憶體中生成含有綠色色帶的虛構影像。"""
    image = np.zeros((80, 120, 3), dtype=np.uint8)
    cv2.rectangle(image, (x, y), (x + 30, y + 5), (0, 255, 0), -1)
    return image


if __name__ == "__main__":
    # 門檻只用於此合成影像。長寬比使用軸對齊外接框。
    print(detect_candidates(synthetic_image(20, 25), (50, 150, 100),
                            (70, 255, 255), min_area=100, min_aspect=3))
