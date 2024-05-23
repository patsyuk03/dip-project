import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import cv2
import os 
import random
from Card import Card
from Map import Map

SCRIPT_PATH = os.path.dirname(__file__)

class GUI:
    def __init__(self, map_size=11) -> None:
        self.map_size = map_size

        self.root = tk.Tk()
        self.game_map = np.zeros((map_size*70, map_size*70, 3), np.uint8)+255
        self.card = cv2.cvtColor(cv2.imread(os.path.join(SCRIPT_PATH, f"images/initial_card.png")), cv2.COLOR_BGR2RGB)
        card_coords = (
            map_size//2*70,
            map_size//2*70
        )
        self.game_map[card_coords[0]:card_coords[0]+70, card_coords[1]:card_coords[1]+70, :] = self.card
        self.game_map_with_options = self.game_map.copy()

        self.map = Map()
        self.map.update_map_dict(self.card, card_coords)

        self.root.title("Carcessonne")
        self.root.geometry(f"{self.map_size*70+200}x{self.map_size*70+20}+100+100")
        self.root.resizable(width=True, height=True)
        
        game_map  =  ImageTk.PhotoImage(image=Image.fromarray(self.game_map))
        card  =  ImageTk.PhotoImage(image=Image.fromarray(self.card))

        tk.Label(self.root, image=game_map).place(x=10, y=10)
        tk.Button(self.root, text="Get Card", command=self.get_card).place(x=self.map_size*70+50, y=30)
        tk.Label(self.root, text="Your Card:").place(x=self.map_size*70+50, y=60)
        tk.Label(self.root, image=card).place(x=self.map_size*70+50, y=80)
        tk.Button(self.root, text="Turn Card", command=self.turn_card).place(x=self.map_size*70+50, y=160)
        tk.Button(self.root, text="Display Options", command=self.display_options).place(x=self.map_size*70+50, y=190)

        self.root.mainloop()

    def get_card(self):
        self.card = cv2.cvtColor(cv2.imread(os.path.join(SCRIPT_PATH, f"images/cards/card_{str(random.randint(0, 24)).zfill(2)}.png")), cv2.COLOR_BGR2RGB).astype('uint8')
        self.update_gui()

    def turn_card(self):
        self.card = cv2.rotate(self.card, cv2.ROTATE_90_CLOCKWISE)
        self.update_gui()

    def display_options(self):
        options = self.map.find_available_option(self.card)
        for number, location in enumerate(options):
            self.game_map_with_options = cv2.putText(self.game_map_with_options, text=str(number+1), org=(location[0]+35, location[1]+35), color=(0, 0, 0), thickness=2, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5)
        self.update_gui()

    def update_gui(self):
        game_map = ImageTk.PhotoImage(image=Image.fromarray(self.game_map_with_options))
        card = ImageTk.PhotoImage(image=Image.fromarray(self.card))

        tk.Label(self.root, image=game_map).place(x=10, y=10)
        tk.Label(self.root, image=card).place(x=self.map_size*70+50, y=80)

        self.game_map_with_options = self.game_map.copy()

        self.root.mainloop()





def main():
    gui = GUI()



if __name__ == "__main__":
    main()
        
