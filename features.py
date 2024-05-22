import numpy as np
import cv2

def get_border(card, n = 5):
    border = {
        "UP": card[:n, :],
        "RIGHT": card[:, -n:],
        "DOWN": card[-n:, :],
        "LEFT": card[:, :n]
    }
    return border

def find_castle(card, sides):
    out = cv2.cvtColor(card, cv2.COLOR_BGR2HSV)
    out = cv2.inRange(out, np.array([0, 50, 0]), np.array([30, 255, 255]))

    kernel = np.array([[0,1,0], [1,1,1], [0,1,0]], np.uint8)
    out = cv2.morphologyEx(out, cv2.MORPH_OPEN, kernel)
    out = cv2.morphologyEx(out, cv2.MORPH_CLOSE, kernel)
    out = cv2.erode(out, kernel, iterations=2) 

    border = get_border(out)
    for side_name, side_array in border.items():
        nonzero = np.count_nonzero(side_array)*100/max(side_array.shape)
        if nonzero > 80:
            sides[side_name] = "CASTLE"
    
    return sides

def find_road(card, sides):
    out = cv2.cvtColor(card, cv2.COLOR_BGR2HSV)
    out = cv2.inRange(out, np.array([0, 0, 0]), np.array([255, 50, 255]))

    kernel = np.array([[0,1,0], [1,1,1], [0,1,0]], np.uint8)
    out = cv2.morphologyEx(out, cv2.MORPH_OPEN, kernel)

    border = get_border(out)
    for side_name, side_array in border.items():
        nonzero = np.count_nonzero(side_array)*100/max(side_array.shape)
        if nonzero > 20:
            sides[side_name] = "ROAD"

    return sides