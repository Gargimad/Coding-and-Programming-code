import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from db import Database
import webbrowser
import os
from qna import QnaPage

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class StartScreen:
    def __init__(self, root, userEmail):
        self.root = root
        self.db = Database()
        self.root.title("PIBBIT")
        self.root.state("zoomed")
        self.root.configure(bg="#DAA520")
        self.userEmail = userEmail

        self.nav_bar = tk.Frame(self.root, bg="#DAA520")
        self.nav_bar.pack(side="top", fill="x", padx=20, pady=20)
        self.resultsContainer = tk.Frame(self.root, bg="#DAA520")
        self.createUi() 
        self.createDynamicNav()

        # The container for dynamic content (Results or Q&A)
        

    def createDynamicNav(self):
        self.mb = tk.Menubutton(
            self.nav_bar, text="Explore ⏷", 
            bg="#2D5A27", fg="white", 
            font=("Georgia", 12), width=20, 
            direction='below', relief='flat', cursor="hand2")
        #self.mb.pack(side="left", padx = (0,10), command = self.displayBusinesses(1, 'Explore'))
        self.mb.pack(side="left", padx = (0,10))
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

        if not self.userEmail:
            self.createButton(self.nav_bar, "Sign Up", "#2D5A27", self.openSignUp)
            self.createButton(self.nav_bar, "Login", "#2D5A27", self.openLogin)
        else:
            self.coupsNDeals = tk.Button(self.nav_bar, text="Coupons and Deals", 
                                        bg="#2D5A27", fg="white", font=("Georgia", 12), 
                                        width=20, relief='flat', cursor="hand2")
            self.coupsNDeals.pack(side="left", padx=(0,10))
            
            # FIXED Q&A BUTTON
            self.qna_btn = tk.Button(self.nav_bar, text="Q&A",
                                     bg="#2D5A27", fg="white", font=("Georgia", 12), 
                                     width=20, relief='flat', cursor="hand2", 
                                     command=self.showQna)
            self.qna_btn.pack(side="left", padx=(0,10))
            
            self.bookmarks = tk.Button(self.nav_bar, text="Bookmarks",
                                      bg="#2D5A27", fg="white", font=("Georgia", 12), 
                                      width=20, relief='flat', cursor="hand2")
            self.bookmarks.pack(side="left", padx=(0,10))
            
            self.profile_btn = tk.Menubutton(self.nav_bar, text="👤 Profile ✎", font=("Arial", 11),
                                            bg="#DAA520", relief="flat", cursor="hand2", width=20)
            self.profile_btn.pack(side="right")

            profile_menu = tk.Menu(self.profile_btn, tearoff=0, bg="white", fg="black")
            profile_menu.add_command(label="Edit Profile")
            profile_menu.add_command(label="Settings")
            profile_menu.add_separator()
            profile_menu.add_command(label="Logout")
            self.profile_btn["menu"] = profile_menu

    def showQna(self):
        """Clears the screen and initializes the Q&A page."""
        # Hide home screen elements
        self.mainPageFrame.place_forget()
        
        # Clear any existing content in resultsContainer
    
        for widget in self.resultsContainer.winfo_children():
            widget.destroy()
            
        self.resultsContainer.pack(fill="both", expand=True)

        # Colors expected by the QnaPage class
        colors = {
            'bg': "#DAA520",
            'darkText': "black",
            'navBg': "#2D5A27"
        }

        # Initialize and draw the Q&A content inside the results container
        qna_view = QnaPage(self.resultsContainer, colors)
        qna_view.draw()

    def createButton(self, parent, text, color, command):
        btn = tk.Button(parent, text=text, font=("Georgia", 12, "bold"),
                        bg=color, fg="white", width=15, pady=8,
                        bd=0, command=command, cursor="hand2")
        btn.pack(side="right", padx=10)

    def fetchCategories(self):
        return self.db.fetchCategories()

    def fetchSubcategories(self, cat_id):
        return self.db.fetchSubcategories(cat_id)

    def fetchBusinessesBySubs(self, sub_id):
        return self.db.fetchBusinessesBySubs(sub_id)
    def fetchAllBusinesses(self):
        return self.db.fetchAllBusinesses()
    
    def displayBusinesses(self, sub_id, sub_name):
        self.mainPageFrame.place_forget()
        for widget in self.resultsContainer.winfo_children():
            widget.destroy()

        self.resultsContainer.pack(fill="both", expand=True)
        canvas = tk.Canvas(self.resultsContainer, bg="#DAA520", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.resultsContainer, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#DAA520")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', configure_canvas)

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        if sub_id == 1:
            businesses = self.fetchAllBusinesses()
        else:
            tk.Label(scrollable_frame, text=f"Results for {sub_name}:", 
                 font=("Georgia", 20, "bold"), bg="#DAA520", pady=15).pack()
            businesses = self.fetchBusinessesBySubs(sub_id) 
        if not businesses:
            tk.Label(scrollable_frame, text="No businesses found.", bg="#DAA520").pack()
        else:
            for biz_id, biz_name, rating, review_count, description, website_link in businesses:
                bizCard = tk.Frame(scrollable_frame, bg="#DDE0D6", highlightbackground="#6B8E23", 
                                   highlightthickness=2, padx=15, pady=10)
                bizCard.pack(fill="x", pady=10, padx=50)               
                tk.Label(bizCard, text=biz_name, font=("Georgia", 18), bg="#DDE0D6").pack(anchor="w")
                stars = "★" * int(float(rating)) + "☆" * (5 - int(float(rating)))
                tk.Label(bizCard, text=f"{stars} {rating}", font=("Georgia", 12), 
                         bg="#DDE0D6", fg="#E1AD01").pack(anchor="w")
                tk.Label(bizCard, text=f"{description}", font=("Georgia", 10), bg="#DDE0D6").pack(anchor='w')
                tk.Button(
                    bizCard,
                    text="Website Link",
                    bg="#E4937A",
                    relief="flat",
                    padx=10,
                    cursor="hand2",
                    command=lambda link=website_link: self.openWebsite(link)
                ).pack(side="right", padx=(10, 0))

                # ✅ Only show these buttons AFTER login
                if self.userEmail:
                    tk.Button(
                        bizCard,
                        text="Rate Business",
                        bg="#A2D98E",
                        relief="flat",
                        padx=10,
                        cursor="hand2"
                    ).pack(side="right", padx=(10, 0))

                    tk.Button(
                        bizCard,
                        text="Write a Review",
                        bg="#A2D98E",
                        relief="flat",
                        padx=10,
                        cursor="hand2"
                    ).pack(side="right", padx=(10, 0))

                
                

    def openWebsite(self, website_link):
        try:
            webbrowser.open(website_link, new=2)
        except Exception as e:
            print(f"Error: {e}")

    def createUi(self):
        self.mainPageFrame = tk.Frame(self.root, bg="#DAA520")
        self.mainPageFrame.place(relx=0.5, rely=0.5, anchor="center")
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            imgPath = os.path.join(script_dir, "logo.png")
            img = Image.open(imgPath).resize((500, 320))
            photo = ImageTk.PhotoImage(img)
            logoLabel = tk.Label(self.mainPageFrame, image=photo, bg="#DAA520", bd=0)
            logoLabel.image = photo 
            logoLabel.grid(row=0, column=0, padx=0)
        except:
            tk.Label(self.mainPageFrame, text="[Logo Error]", bg="#DAA520", fg="white").grid(row=0, column=0)

        tk.Label(self.mainPageFrame, text="PIBBIT", font=("Georgia", 100, "bold"),
                 fg="black", bg="#DAA520").grid(row=0, column=1, sticky="w")
        tk.Label(self.mainPageFrame, text="Local Business becomes just a Pibbit Away",
                 font=("Georgia", 25), fg="#6E2F20", bg="#DAA520").grid(row=1, column=1, sticky="w")

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