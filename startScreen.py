import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
#from login import Login

class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("PIBBIT")
        self.root.state("zoomed")
        self.root.configure(bg="#DAA520")
        self.createUi()
        self.createNav()
        '''
    def on_select(self, choice):
        self.clicked.set(self.fixedOption)   
        '''  
    def createNav(self):
        self.mb = tk.Menubutton(
            self.root, text="Explore ⏷", 
            bg="#2D5A27", fg="white", 
            font=("Georgia", 12), width=20, 
            direction='below', relief='flat', cursor="hand2")
        self.mb.place(x=20, y=20)

        # Main Menu setup
        main_menu = tk.Menu(self.mb, tearoff=0, bg="#2D5A27", fg="white", font=("Georgia", 11), activebackground="#3D7A35")
        self.mb["menu"] = main_menu

        # --- Category Submenus ---
        beauty_menu = tk.Menu(main_menu, tearoff=0, bg="#2D5A27", fg="white")
        beauty_menu.add_command(label="Salons", command=lambda: print("Salons"))
        beauty_menu.add_command(label="Spas", command=lambda: print("Spas"))
        beauty_menu.add_command(label="Therapy", command=lambda: print("Therapy"))
        beauty_menu.add_command(label="Messages", command=lambda: print("Messages"))
        beauty_menu.add_command(label="Other", command=lambda: print("Other"))
        
        rest_menu = tk.Menu(main_menu, tearoff=0, bg="#2D5A27", fg="white")
        rest_menu.add_command(label="Cafes", command=lambda: print("Cafes"))
        rest_menu.add_command(label="Breakfast/Brunch", command=lambda: print("Breakfast/Brunch"))
        rest_menu.add_command(label="Lunch/Dinner", command=lambda: print("Lunch/Dinner"))
        rest_menu.add_command(label="Bars & Pubs", command=lambda: print("Food Trucks"))
        rest_menu.add_command(label="Other", command=lambda: print("Bars & Pubs"))
        
        travel_menu = tk.Menu(main_menu, tearoff=0, bg="#2D5A27", fg="white")
        travel_menu.add_command(label = "banana")

        # Add cascades to main menu
        main_menu.add_cascade(label="Beauty & Well-Being", menu=beauty_menu)
        main_menu.add_cascade(label="Restaurants", menu=rest_menu)
        main_menu.add_cascade(label="Travel & Activities", menu=travel_menu)

        self.createButton(self.root, "Sign Up", "#2D5A27", self.openSignUp, x_pos= 1300.5, y_pos=20)
        self.createButton(self.root, "Login", "#2D5A27", self.openLogin, x_pos = 1100.5, y_pos=20)
        
        
    
    def createUi(self):
        # Container frame
        self.cardFrame = tk.Frame(self.root, bg="#DAA520")
        self.cardFrame.place(relx=0.5, rely=0.5, anchor="center")

        try:
            # Use raw string for the path
            img_path = r"C:\Gargi Madala\python\github c&p\Coding-and-Programming-code\logo.png"
            
            # Open and convert to RGBA
            img = Image.open(img_path).convert("RGBA")
            img = img.resize((500, 320), Image.Resampling.LANCZOS)
            
            # Create the PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Create label
            logoLabel = tk.Label(
                self.cardFrame, 
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
            tk.Label(self.cardFrame, text="[Logo Error]", bg="#DAA520", fg="white").grid(row=0, column=0)

        # Title Label
        titleLabel = tk.Label(
            self.cardFrame,
            text="PIBBIT",
            font=("Georgia", 100, "bold"),
            fg="black",
            bg="#DAA520"
        )
        titleLabel.grid(row=0, column=1, sticky="w")
        sloganLabel = tk.Label(
            self.cardFrame,
            text = "Local Business, Just a PIBBIT Away",
            font=("Georgia", 25),
            fg = "#6E2F20",
            bg="#DAA520"
        )
        sloganLabel.grid(row = 1, column=1, sticky = "w")
        
    def createButton(self, parent, text, color, command, x_pos, y_pos):
        tk.Button(
            parent, 
            text=text,
            font=("Georgia", 12, "bold"),
            bg=color, fg="white",
            width=15, pady=8,
            bd=0, command=command,
            cursor = "hand2",
        ).place(x=x_pos, y=y_pos)
        
    def openSignUp(self):
        self.root.destroy()
        from signup import SignUp
        root = tk.Tk()
        SignUp(root)
        root.mainloop()

    def openLogin(self):
        self.root.destroy()
        from login import Login
        root = tk.Tk()
        Login(root)
        root.mainloop()