import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import cv2
import os 
import random
from Card_simulation import Card
from Map_simulation import Map

SCRIPT_PATH = os.path.dirname(__file__)

class GUI:
    def __init__(self, map_size=11) -> None:
        self.map_size = map_size

        self.root = tk.Tk()

        self.card = np.zeros((70, 70, 3), np.uint8)

        self.map = Map()
        self.game_map_with_options = self.map.image.copy()
        self.options = list()

        self.root.title("Carcessonne")
        self.root.geometry(f"{self.map_size*70+200}x{self.map_size*70+20}+100+100")
        self.root.resizable(width=True, height=True)
        
        game_map = ImageTk.PhotoImage(image=Image.fromarray(self.map.image))
        card = ImageTk.PhotoImage(image=Image.fromarray(self.card))

        tk.Label(self.root, image=game_map).place(x=10, y=10)
        tk.Button(self.root, text="Get Card", command=self.get_card).place(x=self.map_size*70+50, y=30)
        tk.Label(self.root, text="Your Card:").place(x=self.map_size*70+50, y=60)
        tk.Label(self.root, image=card).place(x=self.map_size*70+50, y=80)
        tk.Button(self.root, text="Turn Card", command=self.turn_card).place(x=self.map_size*70+50, y=160)
        tk.Button(self.root, text="Display Options", command=self.display_options).place(x=self.map_size*70+50, y=190)
        tk.Label(self.root, text="Select Card Place").place(x=self.map_size*70+50, y=230)
        self.input_box = tk.Entry(self.root, width=10)
        self.input_box.place(x=self.map_size*70+50, y=250)
        tk.Button(self.root, text="Place Card", command=self.place_card).place(x=self.map_size*70+50, y=280)

        self.root.mainloop()

    def get_card(self):
        self.card = cv2.cvtColor(cv2.imread(os.path.join(SCRIPT_PATH, f"images/cards/card_{str(random.randint(0, 24)).zfill(2)}.png")), cv2.COLOR_BGR2RGB).astype('uint8')
        self.update_gui()

    def turn_card(self):
        self.card = cv2.rotate(self.card, cv2.ROTATE_90_CLOCKWISE)
        self.update_gui()

    def display_options(self):
        self.options = self.map.find_available_option(self.card)
        for number, location in enumerate(self.options):
            self.game_map_with_options = cv2.putText(self.game_map_with_options, text=str(number+1), org=(location[0]+35, location[1]+35), color=(0, 0, 0), thickness=2, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5)
        self.update_gui()
    
    def place_card(self):
        user_input = self.input_box.get()
        if user_input.isdigit() and (self.card != np.zeros((70, 70, 3), np.uint8)).all():
            number = int(user_input)
            if number<=len(self.options) and number>0:
                self.map.update_map(self.card, self.options[number-1])
                self.game_map_with_options = self.map.image.copy()
                self.card = np.zeros((70, 70, 3), np.uint8)
        self.update_gui()

    def update_gui(self):
        game_map = ImageTk.PhotoImage(image=Image.fromarray(self.game_map_with_options))
        card = ImageTk.PhotoImage(image=Image.fromarray(self.card))

        tk.Label(self.root, image=game_map).place(x=10, y=10)
        tk.Label(self.root, image=card).place(x=self.map_size*70+50, y=80)

        self.game_map_with_options = self.map.image.copy()

        self.root.mainloop()





def main():
    gui = GUI()



if __name__ == "__main__":
    main()
        
