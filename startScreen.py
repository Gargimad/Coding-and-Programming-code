import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from db import Database
import webbrowser
import os

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class StartScreen:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.root.title("PIBBIT")
        self.root.state("zoomed")
        self.root.configure(bg="#DAA520")

        self.nav_bar = tk.Frame(self.root, bg="#DAA520")
        self.nav_bar.pack(side="top", fill="x", padx=20, pady=20)

        # Create the UI elements
        self.createUi() 
        self.createDynamicNav()

        # Results container (below the nav bar)
        self.resultsContainer = tk.Frame(self.root, bg="#DAA520")
        self.resultsContainer.pack(fill="x", expand=True, pady=(20, 20))

    def createDynamicNav(self):
        self.mb = tk.Menubutton(
            self.nav_bar, text="Explore ⏷", 
            bg="#2D5A27", fg="white", 
            font=("Georgia", 12), width=20, 
            direction='below', relief='flat', cursor="hand2")
        self.mb.pack(side="left")

        main_menu = tk.Menu(self.mb, tearoff=0, bg="#2D5A27", fg="white", font=("Georgia", 11), activebackground="#3D7A35")
        self.mb["menu"] = main_menu
        
        categories = self.fetchCategories()      
        for cat_id, cat_name in categories:
            sub_menu = tk.Menu(main_menu, tearoff=0, bg="#2D5A27", fg="white")
            subcategories = self.fetchSubcategories(cat_id)
            for sub_id, sub_name in subcategories:
                sub_menu.add_command(
                    label=sub_name,
                    command=lambda s_id=sub_id, s_name=sub_name: self.displayBusinesses(s_id, s_name) 
                )
            main_menu.add_cascade(label=cat_name, menu=sub_menu)

        self.createButton(self.nav_bar, "Sign Up", "#2D5A27", self.openSignUp)
        self.createButton(self.nav_bar, "Login", "#2D5A27", self.openLogin)

    def createButton(self, parent, text, color, command):
        btn = tk.Button(
            parent, text=text, font=("Georgia", 12, "bold"),
            bg=color, fg="white", width=15, pady=8,
            bd=0, command=command, cursor="hand2"
        )
        btn.pack(side="right", padx=10)

    def fetchCategories(self):
        return self.db.fetchCategories()

    def fetchSubcategories(self, cat_id):
        return self.db.fetchSubcategories(cat_id)

    def fetchBusinessesBySubs(self, sub_id):
        return self.db.fetchBusinessesBySubs(sub_id)

    def displayBusinesses(self, sub_id, sub_name):
        # Clear previous content
        for widget in self.mainPageFrame.winfo_children():
            widget.destroy()
        for widget in self.resultsContainer.winfo_children():
            widget.destroy()

        tk.Label(self.resultsContainer, text=f"Results for {sub_name}:", 
                 font=("Georgia", 20, "bold"), bg="#DAA520", pady=15).pack()
        
        businesses = self.fetchBusinessesBySubs(sub_id) 
        
        if not businesses:
            tk.Label(self.resultsContainer, text="No businesses found in this category.", bg="#DAA520").pack()
        else:
            for biz_id, biz_name, rating, review_count, description, website_link in businesses:
                bizCard = tk.Frame(self.resultsContainer, bg="#DDE0D6", highlightbackground="#6B8E23", 
                                 highlightthickness=2, padx=15, pady=10)
                bizCard.pack(fill="x", pady=5, padx=50)               
                
                tk.Label(bizCard, text=biz_name, font=("Georgia", 18), bg="#DDE0D6").pack(anchor="w")
                
                stars = "★" * int(float(rating)) + "☆" * (5 - int(float(rating)))
                tk.Label(bizCard, text=f"{stars} {rating}", font=("Georgia", 12), 
                         bg="#DDE0D6", fg="#E1AD01").pack(anchor="w")
                
                tk.Label(bizCard, text=f"{description}", font=("Georgia", 10), bg="#DDE0D6").pack(anchor='w')
                
                tk.Button(bizCard, text="Website link", bg="#E4937A", relief="flat", padx=10, 
                          command=lambda link=website_link: self.openWebsite(link)).pack(anchor="e")

    def openWebsite(self, website_link):
        try:
            webbrowser.open(website_link, new=2)
        except Exception as e:
            print(f"Error opening website: {e}")

    def createUi(self):
        # This frame stays centered for the logo/title
        self.mainPageFrame = tk.Frame(self.root, bg="#DAA520")
        self.mainPageFrame.place(relx=0.5, rely=0.5, anchor="center")

        try:
            # RELATIVE PATH: Looks for logo.png in the same folder as this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            imgPath = os.path.join(script_dir, "logo.png")
            
            img = Image.open(imgPath)
            img = img.resize((500, 320))
            photo = ImageTk.PhotoImage(img)
            
            logoLabel = tk.Label(self.mainPageFrame, image=photo, bg="#DAA520", bd=0)
            logoLabel.image = photo 
            logoLabel.grid(row=0, column=0, padx=0)

        except Exception as e:
            print(f"Image load error: {e}")
            tk.Label(self.mainPageFrame, text="[Logo Error]", bg="#DAA520", fg="white").grid(row=0, column=0)

        titleLabel = tk.Label(
            self.mainPageFrame, text="PIBBIT", font=("Georgia", 100, "bold"),
            fg="black", bg="#DAA520"
        )
        titleLabel.grid(row=0, column=1, sticky="w")

        sloganLabel = tk.Label(
            self.mainPageFrame, text="Local Business becomes just a Pibbit Away",
            font=("Georgia", 25), fg="#6E2F20", bg="#DAA520"
        )
        sloganLabel.grid(row=1, column=1, sticky="w")

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