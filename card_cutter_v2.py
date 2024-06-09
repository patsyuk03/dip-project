import numpy as np
import cv2
import os

SCRIPT_PATH = os.path.dirname(__file__)
def apply_pincushion_distortion(image, k1):
    h, w = image.shape[:2]

    fx = w
    fy = h
    cx = w / 2
    cy = h / 2
    K = np.array([[fx, 0, cx],
                  [0, fy, cy],
                  [0, 0, 1]], dtype=np.float32)

    D = np.array([k1, 0, 0, 0], dtype=np.float32)
    map1, map2 = cv2.initUndistortRectifyMap(K, D, None, K, (w, h), cv2.CV_32FC1)
    distorted_image = cv2.remap(image, map1, map2, interpolation=cv2.INTER_LINEAR)

    return distorted_image    

def add_grid(frame):
    row, col, c = frame.shape
    for x in range(0, row, 70):
        cv2.line(frame, (0, x), (col, x), (0, 255, 0), thickness=2)

    for y in range(0, col, 70):
        cv2.line(frame, (y, 0), (y, row), (0, 255, 0), thickness=2)

    return frame

def update(new):
    pass

def main():
    global pivot
    camera = cv2.VideoCapture(2)
    ret, image = camera.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    pivot = 0
    cv2.namedWindow("Threshold")
    cv2.createTrackbar("Lower", "Threshold", 0, image.shape[0], update)
    # cv2.createTrackbar("Upper", "Threshold", image.shape[0], image.shape[0], update)
    cv2.createTrackbar("Left", "Threshold", 0, image.shape[1], update)
    # cv2.createTrackbar("Right", "Threshold", image.shape[1], image.shape[1], update)

    n = 16
    while True:
        ret, image = camera.read()
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = apply_pincushion_distortion(image, -0.6)
        image = apply_pincushion_distortion(image, 0.3)

        lower = cv2.getTrackbarPos("Lower", "Threshold")
        # upper = cv2.getTrackbarPos("Upper", "Threshold")
        left = cv2.getTrackbarPos("Left", "Threshold")
        # right = cv2.getTrackbarPos("Right", "Threshold")

        if lower+70 < image.shape[0] and left+70 < image.shape[1]:
            out = image[lower:lower+70, left:left+70, :]
        
        cv2.imshow("In range", out)
        # cv2.imshow("Original", image)

        keycode = cv2.waitKey(1) & 0xFF
        if keycode == ord('q'):
            break
        elif keycode == ord('s'):
            path = os.path.join(SCRIPT_PATH, f"images/cards_2/card_{str(n).zfill(2)}.png")
            n+=1
            print("Saving image to:", path)
            cv2.imwrite(path, out)
    cv2.destroyAllWindows()

    

if __name__ == "__main__":
    main()