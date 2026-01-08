import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from db import Database
from login import Login
import webbrowser

class StartScreen:
    def __init__(self, root): #Initialization function
        self.root = root
        self.db = Database() #Connecting to the database
        self.root.title("PIBBIT") #Top title in the tkinter application
        self.root.state("zoomed")
        self.root.configure(bg="#DAA520") #Background of the whole application
        self.createUi() #Goes to the createUi function below
        self.createDynamicNav() #Goes to the createDynamicNav function that creates the navigation bar
        self.resultsContainer = tk.Frame(self.root, bg="#DAA520") #This tk frame creates the container that's below the navigation bar
        self.resultsContainer.pack(fill="y", expand=True, pady=(100, 20))
        #self.createNav()
    
    def createDynamicNav(self): #Dynamically creates the navigation bar by connecting to the pibbit.sqlite database
        self.mb = tk.Menubutton(
            self.root, text="Explore ⏷", #Explore menu bar at the top left
            bg="#2D5A27", fg="white", #Styles the explore bar ------>
            font=("Georgia", 12), width=20, 
            direction='below', relief='flat', cursor="hand2")
        self.mb.place(x=20, y=20) #Location of the menu bar
        
        main_menu = tk.Menu(self.mb, tearoff=0, bg="#2D5A27", fg="white", font=("Georgia", 11), activebackground="#3D7A35") #Styles the menu bar
        self.mb["menu"] = main_menu
        categories = self.fetchCategories() #Calls the method which calls the db      
        for cat_id, cat_name in categories: #Iterating and displaying/looping the categories
            sub_menu = tk.Menu(main_menu, tearoff=0, bg="#2D5A27", fg="white") #Creating the sub menu- the menu that branches out from the main menu
            subcategories = self.fetchSubcategories(cat_id) #Fetches the subcategories using the cat_id from the sqlite database
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
        for widget in self.mainPageFrame.winfo_children():
            widget.destroy()
        for widget in self.resultsContainer.winfo_children():
            widget.destroy()
        # 2. Add a Header
        tk.Label(self.resultsContainer, text=f"Results for {sub_name}:", font=("Georgia", 20, "bold"), bg = "#DAA520", pady= 15).pack()
            # 3. Fetch data from SQLite
        businesses = self.fetchBusinessesBySubs(sub_id) 
        
        # 4. Loop through results and create "Cards"
        if not businesses:
            tk.Label(self.resultsContainer, text="No businesses found in this category.").pack()
        else:
            for biz_id, biz_name, rating, review_count, description, website_link in businesses:
                bizCard = tk.Frame(self.resultsContainer, bg="#DDE0D6", highlightbackground="#6B8E23", 
                                highlightthickness=2, padx=15, pady=10)
                bizCard.pack(fill="x", pady=5, padx=50)
                
                tk.Label(bizCard, text=biz_name, font=("Georgia", 18), bg="#DDE0D6").pack(anchor="w")
                stars = "★" * int(float(rating)) + "☆" * (5 - int(float(rating)))
                tk.Label(bizCard, text=f"{stars} {rating}", font=("Georgia", 12), 
                         bg="#DDE0D6", fg="#E1AD01").pack(anchor="w")
                tk.Label(bizCard, text=f"{description}", font = ("Georgia", 10), bg= "#DDE0D6").pack(anchor ='w')
                print(website_link)
                tk.Button(bizCard, text="Website link", bg="#E4937A", relief="flat", padx=10, command= lambda: self.openWebsite(website_link)).pack(anchor="e") #Button that allows users to click on website link
                
    def openWebsite(self, website_link):
        url= f"{website_link}" #Creates the gateway to the website link in the database
        print("url", url)
        print("website_link", website_link)
        try:
            webbrowser.open(url, new=2) #this opens the link from the click of the button
        except Exception as e:
            print(f"Error opening website.Try copying and pasting this link to your webbrowser: {e}") #Backup if the link doesn't work for some reason

    def createUi(self):
        self.mainPageFrame = tk.Frame(self.root, bg="#DAA520") #Creating the mainPage frame that will hold the logo and the main title
        self.mainPageFrame.place(relx=0.5, rely=0.5, anchor="center") #Positioning the mainPageFrame


        try:  #Will try to use canvas for the image when I reach home----------------------------------------------------------->
            imgPath = r"C:\Gargi Madala\python\github c&p\Coding-and-Programming-code\logo.png" #Used raw link because logo.png wasn't working? --------------------------------------------Inv further
            img = Image.open(imgPath)
            img = img.resize((500, 320))
            photo = ImageTk.PhotoImage(img)
            logoLabel = tk.Label(
                self.mainPageFrame,
                image=photo,
                bg="#DAA520",
                bd=0,
                highlightthickness=0
            )
            logoLabel.image = photo #References the image to have a backup when python begins to garbage it
            logoLabel.grid(row=0, column=0, padx=0)

        except Exception as e:
            print(f"Error: {e}")
            tk.Label(self.mainPageFrame, text="[Logo Error]", bg="#DAA520", fg="white").grid(row=0, column=0)

        titleLabel = tk.Label( #Styling the main title that appears on startscreen
            self.mainPageFrame,
            text="PIBBIT",
            font=("Georgia", 100, "bold"), #Made the font bigger and bolder than the normal texts because of a higher position in heirarchy
            fg="black", #Applying contrast against the golden background below this
            bg="#DAA520"
        )
        titleLabel.grid(row=0, column=1, sticky="w")

        sloganLabel = tk.Label( #Styling the slogan that's under the title
            self.mainPageFrame, #Frame that its in
            text = "Local Business becomes just a Pibbit Away", #The main content
            font=("Georgia", 25), #style from here-->
            fg = "#6E2F20", #Differentiated this with the title color to differentiate the purposes of the texts.
            bg="#DAA520" #Made the fg dark also to contrast with this bg
        )
        sloganLabel.grid(row = 1, column=1, sticky = "w")

    def createButton(self, parent, text, color, command, x_pos, y_pos): #Creates the typical button for users to click on.
        tk.Button( #Styling the button--->
            parent,
            text=text,
            font=("Georgia", 12, "bold"),
            bg=color, fg="white",
            width=15, pady=8,
            bd=0, command=command, 
            cursor = "hand2",
        ).place(x=x_pos, y=y_pos) #Placement of the button is now more controlled.

    def openSignUp(self): #Opens the Sign up page after user clicks 'Sign up' button
        self.root.destroy() #Destroys the current display for users to see the Sign up page
        from signup import SignUp #Imports the Sign up class from signup.py to carry out necessary tasks
        root = tk.Tk() #Opens up another root or page
        SignUp(root) #Connects to the root page of the Sign up class and grabs its elements
        root.mainloop() #Runs the page here automatically

    def openLogin(self): #Opens the login page after user clicks 'Login' button
        self.root.destroy() #Destroys the current display for users to see the Login page
        from login import Login #Imports the login class from login.py to carry out necessary tasks
        root = tk.Tk() #Opens up another root or page
        Login(root) #Connects to the root page of the Login class and grabs its elements
        root.mainloop() #Runs the page here automatically
