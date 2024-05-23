import numpy as np
import cv2
import os
import features

SCRIPT_PATH = os.path.dirname(__file__)

def put_sides(card, sides):
    for side, feature in sides.items():
        if side == "DOWN":
            card = cv2.putText(card, text=feature, org=(card.shape[1]//2-20, card.shape[0]-5), color=(0, 0, 0), thickness=1, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4) 
        
        elif side == "UP":
            card = cv2.putText(card, text=feature, org=(card.shape[1]//2-20, 10), color=(0, 0, 0), thickness=1, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4)
        
        elif side == "LEFT":
            card = cv2.rotate(card, cv2.ROTATE_90_CLOCKWISE)
            card = cv2.putText(card, text=feature, org=(card.shape[1]//2-20, 10), color=(0, 0, 0), thickness=1, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4) 
            card = cv2.rotate(card, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        elif side == "RIGHT":
            card = cv2.rotate(card, cv2.ROTATE_90_COUNTERCLOCKWISE)
            card = cv2.putText(card, text=feature, org=(card.shape[1]//2-20, 10), color=(0, 0, 0), thickness=1, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4) 
            card = cv2.rotate(card, cv2.ROTATE_90_CLOCKWISE)

    return card

def main():
    n = 0
    while True:
        image = cv2.imread(os.path.join(SCRIPT_PATH, f"images/cards/card_{str(n).zfill(2)}.png"))

        sides = {
            "UP": "GRASS",
            "RIGHT": "GRASS",
            "DOWN": "GRASS",
            "LEFT": "GRASS"
        }

        sides = features.find_castle(image, sides)
        sides = features.find_road(image, sides)
        out = put_sides(image.copy(), sides)

        cv2.imshow("Out", out)
        cv2.imshow("Original", image)

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