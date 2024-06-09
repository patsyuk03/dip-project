import cv2
import numpy as np
from Card_simulation import Card
import os

SCRIPT_PATH = os.path.dirname(__file__)

class Map:
    def __init__(self, map_size=11) -> None:
        self.map_size = map_size
        self.map = self.create_map()
        self.image = np.zeros((map_size*70, map_size*70, 3), np.uint8)+255
        card = cv2.cvtColor(cv2.imread(os.path.join(SCRIPT_PATH, f"images/initial_card.png")), cv2.COLOR_BGR2RGB)
        card_coords = (
            map_size//2*70,
            map_size//2*70
        )
        self.image[card_coords[0]:card_coords[0]+70, card_coords[1]:card_coords[1]+70, :] = card
        self.update_map(card, card_coords)
        
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
        card.location = location
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
        
        self.image[location[1]:location[1]+70, location[0]:location[0]+70, :] = image

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


