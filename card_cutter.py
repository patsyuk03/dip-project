import numpy as np
import cv2
import os

SCRIPT_PATH = os.path.dirname(__file__)

def update(new):
    pass

def main():
    global pivot
    image = cv2.imread(os.path.join(SCRIPT_PATH, "images/carcassonne_cards.png"))

    pivot = 0
    cv2.namedWindow("Threshold")
    cv2.createTrackbar("Lower", "Threshold", 0, image.shape[0], update)
    # cv2.createTrackbar("Upper", "Threshold", image.shape[0], image.shape[0], update)
    cv2.createTrackbar("Left", "Threshold", 0, image.shape[1], update)
    # cv2.createTrackbar("Right", "Threshold", image.shape[1], image.shape[1], update)

    n = 4
    while True:
        image = cv2.imread(os.path.join(SCRIPT_PATH, "images/carcassonne_cards.png"))

        lower = cv2.getTrackbarPos("Lower", "Threshold")
        # upper = cv2.getTrackbarPos("Upper", "Threshold")
        left = cv2.getTrackbarPos("Left", "Threshold")
        # right = cv2.getTrackbarPos("Right", "Threshold")

        if lower+70 < image.shape[0] and left+70 < image.shape[1]:
            out = image[lower:lower+70, left:left+70, :]
        
        cv2.imshow("In range", out)
        # cv2.imshow("Original", image)

        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break
        elif (cv2.waitKey(1) & 0xFF) == ord("s"):
            path = os.path.join(SCRIPT_PATH, f"images/cards/card_{str(n).zfill(2)}.png")
            # n+=1
            print("Saving image to:", path)
            cv2.imwrite(path, out)
    cv2.destroyAllWindows()

    

if __name__ == "__main__":
    main()