import cv2
import numpy as np

class Card:
    def __init__(self, image=np.zeros((70, 70, 3), np.uint8)) -> None:
        self.image = image
        self.image_with_features = image.copy()
        self.location = None
        self.features = {
            "UP": "",
            "RIGHT": "",
            "DOWN": "",
            "LEFT": ""
        }
        self.empty = not self.image.any()

        if not self.empty:
            self.find_castle()
            self.find_road()
            self.find_grass()
            self.put_sides()

    def put_sides(self):
        for side, feature in self.features.items():
            if side == "DOWN":
                self.image_with_features = cv2.putText(self.image_with_features, text=feature, org=(self.image_with_features.shape[1]//2-20, self.image_with_features.shape[0]-5), color=(0, 0, 0), thickness=1, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4) 
            
            elif side == "UP":
                self.image_with_features = cv2.putText(self.image_with_features, text=feature, org=(self.image_with_features.shape[1]//2-20, 10), color=(0, 0, 0), thickness=1, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4)
            
            elif side == "LEFT":
                self.image_with_features = cv2.rotate(self.image_with_features, cv2.ROTATE_90_CLOCKWISE)
                self.image_with_features = cv2.putText(self.image_with_features, text=feature, org=(self.image_with_features.shape[1]//2-20, 10), color=(0, 0, 0), thickness=1, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4) 
                self.image_with_features = cv2.rotate(self.image_with_features, cv2.ROTATE_90_COUNTERCLOCKWISE)
            
            elif side == "RIGHT":
                self.image_with_features = cv2.rotate(self.image_with_features, cv2.ROTATE_90_COUNTERCLOCKWISE)
                self.image_with_features = cv2.putText(self.image_with_features, text=feature, org=(self.image_with_features.shape[1]//2-20, 10), color=(0, 0, 0), thickness=1, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4) 
                self.image_with_features = cv2.rotate(self.image_with_features, cv2.ROTATE_90_CLOCKWISE)

    def get_border(self, card, n = 5):
        border = {
            "UP": card[:n, :],
            "RIGHT": card[:, -n:],
            "DOWN": card[-n:, :],
            "LEFT": card[:, :n]
        }
        return border

    def find_castle(self):
        out = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
        out = cv2.inRange(out, np.array([0, 50, 0]), np.array([30, 255, 255]))

        kernel = np.array([[0,1,0], [1,1,1], [0,1,0]], np.uint8)
        out = cv2.morphologyEx(out, cv2.MORPH_OPEN, kernel)
        out = cv2.morphologyEx(out, cv2.MORPH_CLOSE, kernel)
        out = cv2.erode(out, kernel, iterations=2) 

        border = self.get_border(out)
        for side_name, side_array in border.items():
            nonzero = np.count_nonzero(side_array)*100/max(side_array.shape)
            if nonzero > 80:
                self.features[side_name] = "CASTLE"

    def find_road(self):
        out = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
        out = cv2.inRange(out, np.array([0, 0, 0]), np.array([255, 50, 255]))

        kernel = np.array([[0,1,0], [1,1,1], [0,1,0]], np.uint8)
        out = cv2.morphologyEx(out, cv2.MORPH_OPEN, kernel)

        border = self.get_border(out)
        for side_name, side_array in border.items():
            nonzero = np.count_nonzero(side_array)*100/max(side_array.shape)
            if nonzero > 20:
                self.features[side_name] = "ROAD"

    
    def find_grass(self):
        for side, feature in self.features.items():
            if feature == "":
                self.features[side] = "GRASS"
