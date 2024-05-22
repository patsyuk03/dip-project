#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import cv2
import os

SCRIPT_PATH = os.path.dirname(__file__)

def update(new):
    pass
 
def main():
    colors = ['lR', 'lG', 'lB', 'uR', 'uG', 'uB']
    value = [0, 0, 0, 255, 50, 255]
    bounds = {}
    for idx, color in enumerate(colors):
        bounds[color] = value[idx]

    cv2.namedWindow("Threshold")
    for color in colors:
        cv2.createTrackbar(color, "Threshold", bounds[color], 255, update)

    n = 0
    while True:
        # image_rgb = cv2.imread(os.path.join(SCRIPT_PATH, f"images/cards/card_{str(n).zfill(2)}.png"))
        image_rgb = cv2.imread(os.path.join(SCRIPT_PATH, f"images/carcassonne_cards.png"))


        image = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2HSV)

        # kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        # image_grey = cv2.filter2D(image_grey, -1, kernel)

        for key, val in bounds.items():
            bounds[key] = cv2.getTrackbarPos(key, "Threshold")
        
        lowerBounds = np.array([bounds['lR'],bounds['lG'],bounds['lB']])
        upperBounds = np.array([bounds['uR'],bounds['uG'],bounds['uB']])

        out = cv2.inRange(image, lowerBounds, upperBounds)

        kernel = np.array([[0,1,0], [1,1,1], [0,1,0]], np.uint8)
        # out = cv2.erode(out, kernel, iterations=1) 
        # out = cv2.morphologyEx(out, cv2.MORPH_CLOSE, kernel)
        out = cv2.morphologyEx(out, cv2.MORPH_OPEN, kernel)
        # out = cv2.dilate(out, kernel, iterations=2) 

        cv2.imshow("Out", out)
        cv2.imshow("Original", image_rgb)

        keycode = cv2.waitKey(1) & 0xFF
        if keycode == ord('q'):
            break
        elif keycode == ord('a'):
            if n > 0:
                n-=1
        elif keycode == ord('d'):
            if n < 24:
                n+=1
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()