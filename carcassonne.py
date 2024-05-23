import numpy as np
import cv2
import os
from Card import Card
from Map import Map
import tkinter as tk
from PIL import ImageTk, Image
from GUI import GUI


SCRIPT_PATH = os.path.dirname(__file__)

map_size = 11

root = tk.Tk()
root.resizable(width=True, height=True)


def display_options(game_map, options):
    for number, location in enumerate(options):
        game_map = cv2.putText(game_map, text=str(number), org=location, color=(0, 0, 0), thickness=2, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5)
    return game_map


def main():


    gui = GUI()


if __name__ == "__main__":
    main()