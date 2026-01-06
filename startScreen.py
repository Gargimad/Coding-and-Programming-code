import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from db import Database
#from login import Login

class StartScreen:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.root.title("PIBBIT")
        self.root.state("zoomed")
        self.root.configure(bg="#DAA520")
        self.createUi()
        self.createDynamicNav()
        self.resultsContainer = tk.Frame(self.root, bg="#DAA520")
        self.resultsContainer.pack(fill="y", expand=True, pady=(100, 20))
        #self.createNav()
    
    def createDynamicNav(self):
        self.mb = tk.Menubutton(
            self.root, text="Explore ⏷", 
            bg="#2D5A27", fg="white", 
            font=("Georgia", 12), width=20, 
            direction='below', relief='flat', cursor="hand2")
        self.mb.place(x=20, y=20)
        main_menu = tk.Menu(self.mb, tearoff=0, bg="#2D5A27", fg="white", font=("Georgia", 11), activebackground="#3D7A35")
        self.mb["menu"] = main_menu
        
        categories = self.fetchCategories() #Calls the method which calls the db
        for cat_id, cat_name in categories: #Iterating and displaying/looping the categories
            sub_menu = tk.Menu(main_menu, tearoff=0, bg="#2D5A27", fg="white")
            subcategories = self.fetchSubcategories(cat_id)
            for sub_id,sub_name in subcategories:
                sub_menu.add_command(
                    label = sub_name,
                    command=lambda s_id=sub_id, s_name=sub_name: self.displayBusinesses(s_id, s_name) 
                )
            main_menu.add_cascade(label=cat_name, menu= sub_menu)
            
        #Login and Sign Up buttons separately but along the same line    
        self.createButton(self.root, "Sign Up", "#2D5A27", self.openSignUp, x_pos= 1300.5, y_pos=20)
        self.createButton(self.root, "Login", "#2D5A27", self.openLogin, x_pos = 1100.5, y_pos=20)
        
    def fetchCategories(self): #Connects to the same def from db
        categories = self.db.fetchCategories()
        return categories
    def fetchSubcategories(self, cat_id):
        subcategories = self.db.fetchSubcategories(cat_id)
        return subcategories
    def fetchBusinessesBySubs(self, sub_id):
        businesses = self.db.fetchBusinessesBySubs(sub_id)
        return businesses
    def displayBusinesses(self, sub_id, sub_name):
    # 1. Clear previous results from your display area
        for widget in self.cardFrame.winfo_children():
            widget.destroy()
        for widget in self.resultsContainer.winfo_children():
            widget.destroy()
        # 2. Add a Header
        tk.Label(self.resultsContainer, text=f"Results for {sub_name}:", font=("Georgia", 14, "bold")).pack()
            # 3. Fetch data from SQLite
        businesses = self.fetchBusinessesBySubs(sub_id) 
        
        # 4. Loop through results and create "Cards"
        if not businesses:
            tk.Label(self.resultsContainer, text="No businesses found in this category.").pack()
        else:
            for biz_id, biz_name, rating, review_count, description in businesses:
                # MATCHING YOUR IMAGE DESIGN:
                card = tk.Frame(self.resultsContainer, bg="#DDE0D6", highlightbackground="#6B8E23", 
                                highlightthickness=2, padx=15, pady=10)
                card.pack(fill="x", pady=5, padx=50)
                
                tk.Label(card, text=biz_name, font=("Georgia", 18), bg="#DDE0D6").pack(anchor="w")
                
                # Stars Row
                stars = "★" * int(float(rating)) + "☆" * (5 - int(float(rating)))
                tk.Label(card, text=f"{stars})", font=("Arial", 12), 
                         bg="#DDE0D6", fg="#E1AD01").pack(anchor="w")
                
                # Button
                tk.Button(card, text="Website link", bg="#E4937A", relief="flat", padx=10).pack(anchor="e")
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