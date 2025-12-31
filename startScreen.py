import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("PIBBIT")
        self.root.state("zoomed")
        self.root.configure(bg="#DAA520")
        self.createUi()
        self.createExplore()
        
    def createExplore(self):
        clicked = StringVar()
        clicked.set("Explore ⏷")
        drop = OptionMenu(self.root, clicked, "Beauty & Well-Being", "Restaurants", "Travel & Activities")
        drop.config(
            bg = "#cf7b63",
            font=("Georgia", 12),
            width=20,
            highlightthickness=0,
            indicatoron=False,
            cursor="hand2"
        )
        drop.place(x=20, y=20)
        
        
    def createUi(self):
        # Container frame
        cardFrame = tk.Frame(self.root, bg="#DAA520")
        cardFrame.place(relx=0.5, rely=0.5, anchor="center")

        try:
            # Use raw string for the path
            img_path = r"C:\Gargi Madala\python\github c&p\Coding-and-Programming-code\logo.png"
            
            # Open and convert to RGBA
            img = Image.open(img_path).convert("RGBA")
            img = img.resize((400, 240), Image.Resampling.LANCZOS)
            
            # Create the PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Create label
            logoLabel = tk.Label(
                cardFrame, 
                image=photo, 
                bg="#DAA520", 
                bd=0, 
                highlightthickness=0
            )
            
            # IMPORTANT: This line prevents Python from deleting the image from memory
            logoLabel.image = photo 
            
            logoLabel.grid(row=0, column=0, padx=0)
            
        except Exception as e:
            print(f"Error: {e}")
            tk.Label(cardFrame, text="[Logo Error]", bg="#DAA520", fg="white").grid(row=0, column=0)

        # Title Label
        titleLabel = tk.Label(
            cardFrame,
            text="PIBBIT",
            font=("Georgia", 100, "bold"),
            fg="black",
            bg="#DAA520"
        )
        titleLabel.grid(row=0, column=1, sticky="w")
        sloganLabel = tk.Label(
            cardFrame,
            text = "Local Business, Just a PIBBIT Away",
            font=("Georgia", 25),
            fg = "#6E2F20",
            bg="#DAA520"
        )
        sloganLabel.grid(row = 1, column=1, sticky = "w")