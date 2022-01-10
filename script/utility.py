import math
import numpy as np


def calc_angle(pos_1: np.ndarray, pos_2: np.ndarray, pos_3: np.ndarray) -> float:
    vec_12: np.ndarray = pos_2 - pos_1
    vec_13: np.ndarray = pos_3 - pos_1

    return math.degrees(math.acos(np.dot(vec_12, vec_13) / (np.linalg.norm(vec_12) * np.linalg.norm(vec_13))))

# convert angle into (0, 90)
def conv_to_acute_angle(angle: float) -> float:
    if 0 <= angle <= 90:
        return angle
    elif 90 < angle <= 180:
        return 180 - angle
    elif 180 < angle <= 270:
        return angle - 180
    else:
        return 360 - angle
