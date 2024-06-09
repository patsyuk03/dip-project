import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import cv2
import os 
import random
from Card import Card
from Map import Map
from Camera import Camera
from tkinter import ttk



SCRIPT_PATH = os.path.dirname(__file__)

class GUI:
    def __init__(self, map_size=11) -> None:
        self.map_size = map_size

        self.root = tk.Tk()

        self.camera = Camera()

        self.card = np.zeros((70, 70, 3), np.uint8)

        self.map = Map()
        self.game_map_with_options = self.map.image.copy()
        self.options = list()
        self.show_cam = tk.IntVar()

        self.root.title("Carcessonne")
        self.root.geometry(f"{self.map_size*70+300}x{self.map_size*70+100}+100+100")
        self.root.resizable(width=True, height=True)
        
        game_map = ImageTk.PhotoImage(image=Image.fromarray(self.map.image))
        card = ImageTk.PhotoImage(image=Image.fromarray(self.card))
        frame = ImageTk.PhotoImage(image=Image.fromarray(self.camera.get_frame()))

        tk.Checkbutton(self.root, text="Camera View", variable=self.show_cam, onvalue=1, offvalue=0, command=self.show_camera).place(x=10, y=10)
        tk.Button(self.root, text="Update Map", command=self.map_from_camera).place(x=self.map_size*70-100, y=10)
        if self.show_cam.get() == 0:
            self.map_lable = tk.Label(self.root, image=game_map)
        else: 
            self.map_lable = tk.Label(self.root, image=frame)
        self.map_lable.place(x=10, y=50)
        tk.Button(self.root, text="Get Card", command=self.get_card).place(x=self.map_size*70+50, y=30)
        tk.Label(self.root, text="Your Card:").place(x=self.map_size*70+50, y=60)
        self.card_label = tk.Label(self.root, image=card)
        self.card_label.place(x=self.map_size*70+50, y=80)
        tk.Button(self.root, text="Turn Card", command=self.turn_card).place(x=self.map_size*70+50, y=160)
        tk.Button(self.root, text="Display Options", command=self.display_options).place(x=self.map_size*70+50, y=190)
        tk.Label(self.root, text="Select Card Place").place(x=self.map_size*70+50, y=230)
        self.input_box = tk.Entry(self.root, width=10)
        self.input_box.place(x=self.map_size*70+50, y=250)
        tk.Button(self.root, text="Place Card", command=self.place_card).place(x=self.map_size*70+50, y=280)

        self.combo = ttk.Combobox(
            state="readonly",
            values=["Original", "Thresh Roads", "Thresh Castles"]
        )
        self.combo.place(x=self.map_size*70+50, y=330)

        self.update_gui()
        self.root.mainloop()

    def get_card(self):
        self.card = cv2.cvtColor(cv2.imread(os.path.join(SCRIPT_PATH, f"images/cards_2/card_{str(random.randint(0, 24)).zfill(2)}.png")), cv2.COLOR_BGR2RGB).astype('uint8')
        self.game_map_with_options = self.map.image.copy()

    def turn_card(self):
        self.card = cv2.rotate(self.card, cv2.ROTATE_90_CLOCKWISE)
        self.game_map_with_options = self.map.image.copy()

    def display_options(self):
        self.options = self.map.find_available_option(self.card)
        for number, location in enumerate(self.options):
            self.game_map_with_options = cv2.putText(self.game_map_with_options, text=str(number+1), org=(location[0]+35, location[1]+35), color=(0, 0, 0), thickness=2, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5)
    
    def place_card(self):
        user_input = self.input_box.get()
        if user_input.isdigit() and (self.card != np.zeros((70, 70, 3), np.uint8)).all():
            number = int(user_input)
            if number<=len(self.options) and number>0:
                self.map.update_map(self.card, self.options[number-1])
                self.game_map_with_options = self.map.image.copy()
                self.card = np.zeros((70, 70, 3), np.uint8)

    def show_camera(self):
        self.game_map_with_options = self.map.image.copy()

    def map_from_camera(self):
        self.map.get_map_from_camera(self.camera.get_frame())
        self.game_map_with_options = self.map.image.copy()

    def update_gui(self):
        card = Card(self.card)
        if self.combo.current() == 1:
            game_map = ImageTk.PhotoImage(image=Image.fromarray(self.map.image_roads))
        elif self.combo.current() == 2:
            game_map = ImageTk.PhotoImage(image=Image.fromarray(self.map.image_castles))
        else:
            game_map = ImageTk.PhotoImage(image=Image.fromarray(self.game_map_with_options))
        card = ImageTk.PhotoImage(image=Image.fromarray(card.image_with_features))
        frame = ImageTk.PhotoImage(image=Image.fromarray(self.camera.get_frame()))

        if self.show_cam.get() == 0:
            self.map_lable.config(image=game_map)
            self.map_lable.game_map = game_map
        else: 
            self.map_lable.config(image=frame)
            self.map_lable.frame = frame

        self.card_label.config(image=card)
        self.card_label.card = card

        self.root.after(100, self.update_gui)
            





def main():
    gui = GUI()



if __name__ == "__main__":
    main()
        
