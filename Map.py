import cv2
import numpy as np
from Card import Card
import os

SCRIPT_PATH = os.path.dirname(__file__)

class Map:
    def __init__(self, map_size=11) -> None:
        self.map_size = map_size
        self.map = self.create_map()
        self.image = np.zeros((map_size*70, map_size*70, 3), np.uint8)+255
        self.image_castles = np.zeros((map_size*70, map_size*70, 2), np.uint8)+255
        self.image_roads = np.zeros((map_size*70, map_size*70, 2), np.uint8)+255
        # card = cv2.cvtColor(cv2.imread(os.path.join(SCRIPT_PATH, f"images/initial_card_2.png")), cv2.COLOR_BGR2RGB)
        # card_coords = (
        #     map_size//2*70,
        #     map_size//2*70
        # )
        # self.image[card_coords[0]:card_coords[0]+70, card_coords[1]:card_coords[1]+70, :] = card
        # self.update_map(card, card_coords)
        
    def create_map(self):
        map_list = list()
        for x in range(self.map_size):
            for y in range(self.map_size):
                card = Card()
                card.location = (x*70, y*70)
                map_list.append(card)
        return map_list

    def update_map(self, image, location):
        card = Card(image)
        # cv2.imshow("test", card.image_with_features)
        card.location = location
        feature_list = [card.features["UP"], card.features["DOWN"], card.features["LEFT"], card.features["RIGHT"]]
        if feature_list != ["", "", "", ""]:
            for place_number, place in enumerate(self.map):
                if place.location == card.location:
                    self.map[place_number] = card
                elif place.location == (location[0], location[1]+70):
                    self.map[place_number].features["UP"] = card.features["DOWN"]
                elif place.location == (location[0], location[1]-70):
                    self.map[place_number].features["DOWN"] = card.features["UP"]
                elif place.location == (location[0]+70, location[1]):
                    self.map[place_number].features["LEFT"] = card.features["RIGHT"]
                elif place.location == (location[0]-70, location[1]):
                    self.map[place_number].features["RIGHT"] = card.features["LEFT"]
            
            self.image[location[1]:location[1]+70, location[0]:location[0]+70, :] = card.image_with_features
            self.get_thresh_castles()
            self.get_thresh_roads()
            

    def find_available_option(self, image):
        card = Card(image)
        options = list()
        for place_number, place in enumerate(self.map):
            feature_list = [place.features["UP"], place.features["DOWN"], place.features["LEFT"], place.features["RIGHT"]]
            if place.empty and feature_list != ["", "", "", ""]:
                if ((place.features["UP"] == card.features["UP"] or place.features["UP"] == "") and
                    (place.features["DOWN"] == card.features["DOWN"] or place.features["DOWN"] == "") and
                    (place.features["LEFT"] == card.features["LEFT"] or place.features["LEFT"] == "") and
                    (place.features["RIGHT"] == card.features["RIGHT"] or place.features["RIGHT"] == "")):

                    options.append(place.location)
        return options
    
    def get_map_from_camera(self, image):
        row, col, c = image.shape

        for x in range(0, row-70, 70):
            for y in range(0, col-70, 70):
                card = image[x:x+70, y:y+70, :]
                card_coords = (y ,x)
                self.update_map(card, card_coords)

    def get_thresh_roads(self):
        out = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
        out = cv2.inRange(out, np.array([17, 18, 142]), np.array([38, 41, 175]))

        kernel = np.array([[0,1,0], [1,1,1], [0,1,0]], np.uint8)
        out = cv2.morphologyEx(out, cv2.MORPH_CLOSE, kernel)
        out = cv2.morphologyEx(out, cv2.MORPH_OPEN, kernel)
        out = cv2.dilate(out, kernel, iterations=2)
        self.image_roads = out 

    def get_thresh_castles(self):
        out = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
        out = cv2.inRange(out, np.array([0, 0, 0]), np.array([20, 255, 255]))

        kernel = np.array([[0,1,0], [1,1,1], [0,1,0]], np.uint8)
        out = cv2.erode(out, kernel, iterations=2) 
        self.image_castles = out 





