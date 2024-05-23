import cv2
import numpy as np
from Card import Card

class Map:
    def __init__(self) -> None:
        self.map = self.create_map()
        
    def create_map(self, map_size=11):
        map_list = list()
        for x in range(map_size):
            for y in range(map_size):
                card = Card()
                card.location = (x*70, y*70)
                map_list.append(card)
        return  map_list

    def update_map_dict(self, image, location):
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


