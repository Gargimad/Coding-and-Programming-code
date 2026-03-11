'''
Gargi Madala, Grace Wu, Dhanvi Ramkumar
Pibbit Start Screen
FBLA- Coding and Programming
26 January 2026
'''
#Imports------------------------------------------------------------------------------------------------------------------------------------
#Imports from libraries:
import os
import sys

#Tkinter imports
import tkinter as tk
#from tkinter import *
from tkinter import messagebox

#Pillow imports
from PIL import Image, ImageTk

#Webbrowser import for opening external links
import webbrowser

#library imports for generating reports
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import tempfile

#Imports from other pages (Modular code): 
from popUpControl import RatingPopup, ReviewPopup
from db import Database
from qna import QnaPage



#Try/Except to help features fit into computers with different sizes
try: 
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

#Class of StartScreen (In Pascal Case)-----------------------------------------------------------------------------------------------------------------------
class StartScreen:
    #Innitializing the class
    def __init__(self, root, userEmail):
        #Connecting to database page and controlling tkinter application framework
        self.root = root
        self.db = Database()
        self.root.title("PIBBIT")
        self.root.state("zoomed")
        self.root.configure(bg="#DAA520")        
        self.userEmail = userEmail #User email that user inputs in sign up/login
        self.navBar = tk.Frame(self.root, bg= "#DAA520")
        self.navBar.pack(side="top", fill="x", padx=20, pady=20)
        self.resultsContainer = tk.Frame(self.root, bg="#DAA520") #Creating frame for the results container which will hold a lot of pages
        
        self.darkMode = False
        self.current_view = None  # Track current view for theme refresh
        self.current_sub_id = None
        self.current_sub_name = None
        self.current_city_id = None

        #Theme Colors-----------------------------------------------------------------------------------------

        #shared colors between the two
        baseColors = {
            "gold": "#DAA520",
            "green": "#2D5A27",
            "lightCard": "#DDE0D6",
            "olive": "#6B8E23",
            "bookmarkGold": "#E1AD01",
        }

        # Light Theme
        self.lightColors = {
            "bg": baseColors["gold"],
            "nav": baseColors["gold"],
            "card": baseColors["lightCard"],
            "cardText": "black",
            "accent": baseColors["green"],
            "accentText": "white",
            "text": "black",
            "footer": baseColors["green"],
            "button": baseColors["green"],
            "buttonText": "white",
            "highlight": baseColors["olive"],
            "bookmarkAdded": baseColors["bookmarkGold"],
            "bookmarkRemove": "#1D2E28",
            "ratingStars": baseColors["bookmarkGold"]
        }

        # Dark Theme
        self.darkColors = {
            "bg": "#1E1E1E",
            "nav": "#2B2B2B",
            "card": "#333333",
            "cardText": "white",
            "accent": "#3D7A35",
            "accentText": "white",
            "text": "white",
            "footer": "#111111",
            "button": "#3D7A35",
            "buttonText": "white",
            "highlight": "#4A7023",
            "bookmarkAdded": "#B8860B",
            "bookmarkRemove": baseColors["green"],
            "ratingStars": "#FFD700"
        }

#Instructions------------------------------------------------------------------------------------------------------------------------------------------
        #This StringVar allows us to update the text at the bottom of the screen dynamically
        self.instructionVar = tk.StringVar(value="Welcome to PIBBIT! Use 'Explore' to find local businesses.")
        self.footer = tk.Label(
            self.root,
            textvariable=self.instructionVar,
            bg=self.lightColors["footer"],
            fg=self.lightColors["accentText"],
            font=("Georgia", 11, "italic"),
            pady=8,
            bd=1,
            relief="sunken"
        )
        self.footer.pack(side="bottom", fill="x")

        self.homeUi() #Creates the front Pibbit Page
        self.createDynamicNav() #Creates the navigation bar at the top
        
    # Function to update the footer text easily
    def updateInstructions(self, text):
        self.instructionVar.set(text)
        
    # Helper method to get current theme colors
    def getColors(self):
        return self.darkColors if self.darkMode else self.lightColors
        
#Dynamic navigation bar using sqlite database values for easy navigation--------------------------------------------------------------------------------------
    def createDynamicNav(self):
        colors = self.getColors()
        #Creating the dynamic navigation bar
        try: 
            #Creating the home logo next to the explore page for easy navigation
            homeLogo = Image.open(os.path.join(os.path.dirname(__file__), "homeLogo.png")).resize((50, 50)) #Sizing home page
            self.homeLogo = ImageTk.PhotoImage(homeLogo) #Using Tkinter image
            homeButton = tk.Button(self.navBar, image=self.homeLogo, bg=colors["nav"], bd=0, cursor="hand2", 
                              command=lambda: [self.updateInstructions("Welcome Home! Select a category to start."), self.resultsContainer.pack_forget(), self.mainPageFrame.place(relx=0.5, rely=0.5, anchor="center")]
                              )
            homeButton.pack(side="left", padx=(0, 10)) #Home button to direct user back to home page when necessary
            #Adding hover instruction for home
            homeButton.bind("<Enter>", lambda e: self.updateInstructions("Click to return to the main dashboard."))
            self.home_button = homeButton  #Storing reference for theme updates
        except:
            messagebox.showwarning("Error", f"Could not load home logo")
        #Creating dynamic menubar dropdowns that sorts businesses by category name
        self.mb = tk.Menubutton( #Creating the menubutton for the Explore
            self.navBar, text="Explore ⏷", 
            bg=colors["button"],fg=colors["buttonText"], 
            font=("Georgia", 12), width=20, 
            direction='below', relief='flat', cursor="hand2")
        self.mb.pack(side="left", padx=(0,10))
#Sorting businesses by category------------------------------------------------------------------------------------------------------------------------
        #On click of explore, the button calls the function displayBusinesses and shows all businesses
        self.mb.bind("<Button-1>", lambda e: self.displayBusinesses(1, 'Explore',0))
        # Add hover instruction for Explore
        self.mb.bind("<Enter>", lambda e: self.updateInstructions("Browse businesses by category or location."))

        mainMenu = tk.Menu(
            self.mb,
            bg=colors["button"],
            fg=colors["buttonText"],
            activebackground=colors["accent"]
        )
        self.mb["menu"] = mainMenu
        #Calling the categories from database
        categories = self.fetchCategories()  
        #Iterating the categories and subcategories and displaying business on click of each subcategory      
        for cat_id, cat_name in categories:
            subCatMenu = tk.Menu(mainMenu, tearoff=0, bg=colors["button"], fg=colors["buttonText"])
            subcategories = self.fetchSubcategories(cat_id)
            for sub_id, sub_name in subcategories:
                subCatMenu.add_command(
                    label=sub_name,
                    command=lambda sId=sub_id, sName=sub_name: self.displayBusinesses(sId, sName,0) 
                )
            mainMenu.add_cascade(label=cat_name, menu=subCatMenu)
        #Displaying sign up and login button when user has not signed in
        if not self.userEmail:
            #Guest exit Page Buttons
            self.guestExPgButtons(self.navBar, "Sign Up", colors["button"], command = self.openSignUp)
            self.guestExPgButtons(self.navBar, "Login", colors["button"], command = self.openLogin)
        
        else:
            #Creating buttons in the top navigation bar that are available only when user signs in
            #Coupons and deals
            self.coupsNDeals = tk.Button(self.navBar, text="Coupons and Deals", 
                                        bg=colors["button"], fg=colors["buttonText"], font=("Georgia", 12), 
                                        width=20, relief='flat', cursor="hand2")
            self.coupsNDeals.config(command=self.showAllCouponsPage) #Shows all coupons
            self.coupsNDeals.pack(side="left", padx=(0,10))
            self.coupsNDeals.bind("<Enter>", lambda e: self.updateInstructions("View exclusive local discounts and promo codes."))
                        
            #Handling bookmarks with the buttons
            self.bookmarks = tk.Button(self.navBar, text="Bookmarks",
                                      bg=colors["button"], fg=colors["buttonText"], font=("Georgia", 12), 
                                      width=20, relief='flat', cursor="hand2",
                                      command=lambda: self.displayBusinesses(-1, "Bookmarks",0))
            self.bookmarks.pack(side="left", padx=(0,10))
            self.bookmarks.bind("<Enter>", lambda e: self.updateInstructions("View businesses you have saved to your favorites."))
            
            #Interactive Q&A Button
            self.helpBtn = tk.Button(self.navBar, text="Help",
                                     bg=colors["button"], fg=colors["buttonText"], font=("Georgia", 12), 
                                     width=20, relief='flat', cursor="hand2", 
                                     command=self.showQA) # Pointing to new function
            self.helpBtn.pack(side="left", padx=(0,10))
            self.helpBtn.bind("<Enter>", lambda e: self.updateInstructions("Have a question? Visit our interactive Q&A support."))

            
            #Dark mode toggle button
            self.darkBtn = tk.Button(
                self.navBar,
                text="🌙 Dark Mode",
                bg=colors["button"],
                fg=colors["buttonText"],
                font=("Georgia", 12),
                width=15,
                relief="flat",
                cursor="hand2",
                command=self.toggleDarkMode
            )
            self.darkBtn.pack(side="right", padx=10)
            
            #Profile settings for logged in user
            self.profileBtn = tk.Menubutton(self.navBar, text="👤 Profile ✎", font=("Arial", 11),
                                            bg=colors["nav"], relief="flat", cursor="hand2", width=20)
            self.profileBtn.pack(side="right")
            self.profileBtn.bind("<Enter>", lambda e: self.updateInstructions("Manage your account settings and profile details."))

            pfpMenuOpts = tk.Menu(self.profileBtn, tearoff=0, bg=colors["card"], fg=colors["cardText"])
            pfpMenuOpts.add_command(label="Edit Profile")
            pfpMenuOpts.add_command(label="Settings")
            pfpMenuOpts.add_separator()
            pfpMenuOpts.add_command(label="Logout")
            self.profileBtn["menu"] = pfpMenuOpts
            
#Intelligent Q&A -------------------------------------------------------------------------------------------------------------------------------------

    #Showing an interactive Q&A with data in another file - Modular code because the data is in another file- keeps things clean
    def showQA(self):
        colors = self.getColors()
        self.updateInstructions("Interactive Support: Browse common questions or search for help.")
        #Hides the main frame
        self.mainPageFrame.place_forget()
        #Clears the result container to display this page
        for widget in self.resultsContainer.winfo_children():
            widget.destroy()  
        #Packs the container
        self.resultsContainer.pack(fill="both", expand=True)
        #Apply theme to results container
        self.resultsContainer.configure(bg=colors["bg"])
        #Showing the qna page
        qnaPageShow = QnaPage(self.resultsContainer, self.root)
        qnaPageShow.show()

    #Defining guestExPgButtons which makes the login and Signup buttons at the top when user is not logged in
    def guestExPgButtons(self, parent, text, color, command):
        colors = self.getColors()
        btn = tk.Button(parent, text=text, font=("Georgia", 12, "bold"),
                        bg=color, fg=colors["buttonText"], width=15, pady=8,
                        bd=0, command=command, cursor="hand2")
        btn.pack(side="right", padx=10)
        #Storing reference for theme updates
        if (text == "Sign Up"):
            self.signup_btn = btn
        else:
            self.login_btn = btn
        #Updating instructions on hover for guest buttons
        if (text == "Sign Up"):
            btn.bind("<Enter>", lambda e: self.updateInstructions("Join PIBBIT to bookmark businesses and get coupons!"))
        else:
            btn.bind("<Enter>", lambda e: self.updateInstructions("Log in to access your saved businesses and deals."))

#Rating and Reviews------------------------------------------------------------------------------------------------------------------------------
    def openRatingPopup(self, biz_id, biz_name):
        RatingPopup(self.root, self.db, biz_id, biz_name, self.displayBusinesses)
    def openReviewPopup(self, root, db, biz_id, biz_name):
        ReviewPopup(self.root, self.db, biz_id, biz_name, self.userEmail)
    def fetchCategories(self):
        return self.db.fetchCategories()

    #Fetches subcategories based on category id from subcategory table in pibbit database
    def fetchSubcategories(self, cat_id):
        return self.db.fetchSubcategories(cat_id)

    #Fetches businesses based on sub id from businesses table in pibbit database     
    def fetchBusinessesBySubs(self, sub_id):
        return self.db.fetchBusinessesBySubs(sub_id)

    #Fetches ALL businesses from businesses table from pibbit database when explore button is clicked
    def fetchAllBusinesses(self):
        return self.db.fetchAllBusinesses()

#Sorting ratings and reviews---------------------------------------------------------------------------------------------------------------------
    def sortByRatings(self, businesses):
        self.updateInstructions("Sorting by user ratings: Showing top-rated businesses first.")
        #Sorting ratings by order- highest rating first and lowest rating last
        if not businesses: return
        sortingBizes = sorted(
            businesses,
            key=lambda b: (float(b[2]) if b[2] not in (None, "", "N/A") else 0.0), #Sorts list by using lambda- rating is 2nd index
            reverse=True
        )
        self.renderBusinessCards(sortingBizes)

    def sortByReviews(self, businesses):
        self.updateInstructions("Sorting by review count: Showing the most discussed businesses.")
        #Sorts businesses by review count- highest first to lowest last
        if not businesses: return
        sortingBizes = sorted(
            businesses,
            key=lambda b: (int(b[3]) if b[3] else 0), #Using b(3) as review is 3rd index of the list in the query of the db
            reverse=True #Using reverse to counter the default lowest to highest order- reverse helps to make it highest to lowest
        )
        self.renderBusinessCards(sortingBizes)

#Bookmarks-----------------------------------------------------------------------------------------------------------------------------------------
    
    def onBookmarkToggle(self, biz_id, button):
        colors = self.getColors()
        res = self.db.toggleBookmark(self.userEmail, biz_id)
        if res == "added":
            button.config(text="🔖 Bookmarked", bg=colors["bookmarkAdded"])
            self.updateInstructions("Business saved to your bookmarks!")
        else:
            button.config(text="☆ Bookmark", bg=colors["bookmarkRemove"])
            self.updateInstructions("Business removed from bookmarks.")

    #Displays businesses on the resultsContainer frame with scrollbar frame
    def displayBusinesses(self, sub_id, sub_name, city_id):
        #Storing current view parameters for theme refresh
        self.current_sub_id = sub_id
        self.current_sub_name = sub_name
        self.current_city_id = city_id
        self.current_view = 'businesses'
        
        colors = self.getColors()
        self.updateInstructions(f"Viewing {sub_name if sub_name != 0 else 'Selected City'}. Click 'Website Link' to visit them.")
        self.mainPageFrame.place_forget()
        #Destroys container before displaying new information
        for widget in self.resultsContainer.winfo_children():
            widget.destroy()
            
        self.resultsContainer.pack(fill="both", expand=True)
        #Apply theme to results container
        self.resultsContainer.configure(bg=colors["bg"])
        
        #Creates the canvas that holds scrolling bar
        resultsContCanvas = tk.Canvas(self.resultsContainer, bg=colors["bg"], highlightthickness=0) #Results Containter Canvas
        scrollbar = tk.Scrollbar(self.resultsContainer, orient="vertical", command=resultsContCanvas.yview)
        self.scrollingFrame = tk.Frame(resultsContCanvas, bg=colors["bg"])
        self.scrollingFrame.bind("<Configure>", lambda e: resultsContCanvas.configure(scrollregion=resultsContCanvas.bbox("all")))
        scrollBarCanvasCreate = resultsContCanvas.create_window((0, 0), window=self.scrollingFrame, anchor="nw")
        
        #Calls the function that configures the canvas created before
        def configure_canvas(event):
            resultsContCanvas.itemconfig(scrollBarCanvasCreate, width=event.width)
        resultsContCanvas.bind('<Configure>', configure_canvas)

        resultsContCanvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        resultsContCanvas.pack(side="left", fill="both", expand=True)

        # Container for sorting buttons and title
        top_bar = tk.Frame(self.scrollingFrame, bg=colors["bg"])
        top_bar.pack(fill="x", pady=10, padx=50)

        #If explore is clicked, it displays all the businesses
        if sub_id == 1:
            tk.Label(top_bar, text="All Businesses:", 
                  font=("Georgia", 20, "bold"), bg=colors["bg"], fg=colors["text"]).pack(side="left")
            businesses = self.fetchAllBusinesses()
        elif sub_id == -1:
            # Displays businesses that the user has saved
            tk.Label(top_bar, text="Your Bookmarked Businesses:", 
                  font=("Georgia", 20, "bold"), bg=colors["bg"], fg=colors["text"]).pack(side="left")
            businesses = self.db.fetchBookmarkedBusinesses(self.userEmail)
        elif sub_id == 0 and city_id != 0:
            tk.Label(top_bar, text=f"Businesses in Selected City:", 
                  font=("Georgia", 20, "bold"), bg=colors["bg"], fg=colors["text"]).pack(side="left")
            businesses = self.db.fetchBusinessByCity(city_id)
        else:
            tk.Label(top_bar, text=f"Results for {sub_name}:", 
                  font=("Georgia", 20, "bold"), bg=colors["bg"], fg=colors["text"]).pack(side="left")
            businesses = self.fetchBusinessesBySubs(sub_id) 

        #Sorting Buttons
        sortingBtnFrame = tk.Frame(top_bar, bg=colors["bg"])
        sortingBtnFrame.pack(side="right")
        
        self.city_mb = tk.Menubutton(sortingBtnFrame, text="Select GA City ⏷", 
                               bg=colors["button"], fg=colors["buttonText"], font=("Georgia", 10), 
                               width=15, relief="flat")
        self.city_mb.pack(side="left", padx=5)
        self.city_mb.bind("<Enter>", lambda e: self.updateInstructions("Filter results by specific Georgia communities."))

        #Creating the empty Menu object
        self.citySelectDrpMenu = tk.Menu(self.city_mb, tearoff=0, bg=colors["button"], fg=colors["buttonText"])
        self.city_mb["menu"] = self.citySelectDrpMenu

        #Binding the click event to trigger the dynamic update
        self.city_mb.bind("<Button-1>", lambda e: self.displayCities())
        
        tk.Button(sortingBtnFrame, text="Highest Ratings", bg=colors["button"], fg=colors["buttonText"], 
                  font=("Georgia", 10), width=15, relief="flat", cursor="hand2",
                  command=lambda: self.sortByRatings(businesses)).pack(side="left", padx=5)
        
        tk.Button(sortingBtnFrame, text="Most Reviewed", bg=colors["button"], fg=colors["buttonText"], 
                  font=("Georgia", 10), width=15, relief="flat", cursor="hand2",
                  command=lambda: self.sortByReviews(businesses)).pack(side="left", padx=5)
        
        print_btn = tk.Button(sortingBtnFrame, text="🖨️", bg=colors["bg"], fg=colors["text"], 
                  font=("Georgia", 15), width=4, relief="flat", cursor="hand2",
                  command= lambda: self.printBusinesses(businesses, sub_name))
        print_btn.pack(side="left", padx = 2)
        print_btn.bind("<Enter>", lambda e: self.updateInstructions("Generate and export a professional PDF report of these businesses."))

        #Container where cards will actually be drawn
        self.cardsFrame = tk.Frame(self.scrollingFrame, bg=colors["bg"])
        self.cardsFrame.pack(fill="both", expand=True)
        self.renderBusinessCards(businesses)
        
#Selection of communities-------------------------------------------------------------------------------------------------------------------------------------
    def displayCities(self):
        colors = self.getColors()
        self.citySelectDrpMenu.delete(0, 'end')
        self.citySelectDrpMenu.configure(bg=colors["button"], fg=colors["buttonText"])
        cities = self.db.fetchCities()
        if not cities:
            self.citySelectDrpMenu.add_command(label="No cities found", state="disabled")
            return
        #Al all cities option
        self.citySelectDrpMenu.add_command(label="All Cities", command=lambda: self.displayBusinesses(1, "Explore", 0))
        self.citySelectDrpMenu.add_separator()
        for city_id, city_name in cities:
            self.citySelectDrpMenu.add_command(
            label=city_name,
            #Using default arguments in lambda (c_id=city_id) to avoid the "closure" bug
            command=lambda c_id=city_id, c_name=city_name: self.displayBusinesses(0,0, c_id)
        )
            
    def renderBusinessCards(self, businesses):
        colors = self.getColors()
        
        #Clearing existing cards first
        for widget in self.cardsFrame.winfo_children():
            widget.destroy()
        if not businesses:
            tk.Label(self.cardsFrame, text="No businesses found.", bg=colors["bg"], fg=colors["text"], font=("Georgia", 12)).pack(pady=20)
            return
        for biz_id, biz_name, rating, review_count, description, website_link in businesses:
            if any(field is None for field in [biz_name, description, website_link]):
                continue

            bizCard = tk.Frame(
                self.cardsFrame,
                bg=colors["card"],
                highlightbackground=colors["highlight"],
                highlightthickness=2,
                padx=15,
                pady=10
            )
            bizCard.pack(fill="x", pady=10, padx=50)  
                     
            tk.Label(bizCard, text=biz_name,
                    font=("Georgia", 18, "bold"),
                    bg=colors["card"],
                    fg=colors["cardText"]).pack(anchor="w")
            rateValue = float(rating) if rating else 0.0
            stars = "★" * int(rateValue) + "☆" * (5 - int(rateValue))
            tk.Label(bizCard, text=f"{stars} {rateValue} ({review_count or 0} reviews)", 
                     font=("Georgia", 12), bg=colors["card"], fg=colors["ratingStars"]).pack(anchor="w")
            tk.Label(bizCard, text=f"{description}", font=("Georgia", 10), bg=colors["card"], fg=colors["cardText"],
                     wraplength=800, justify="left").pack(anchor='w', pady=5)
            
            #Action Buttons Container
            actBtnCont = tk.Frame(bizCard, bg=colors["card"])
            actBtnCont.pack(fill="x", side="bottom")

            tk.Button(actBtnCont, text="Website Link", bg="#D16459", fg=colors["buttonText"], 
                     relief="flat", padx=10, cursor="hand2",
                      command=lambda link=website_link: self.openWebsite(link)).pack(side="right", padx=5)

            if self.userEmail:
                bmSaved = self.db.isBookmarked(self.userEmail, biz_id)
                bmTxt = "🔖 Bookmarked" if bmSaved else "☆ Bookmark"
                bmColor = colors["bookmarkAdded"] if bmSaved else colors["bookmarkRemove"]
                
                bmBtn = tk.Button(bizCard, text=bmTxt, bg=bmColor, fg=colors["buttonText"], 
                                 relief="flat", padx=10, cursor="hand2")
                bmBtn.config(command=lambda b=biz_id, btn=bmBtn: self.onBookmarkToggle(b, btn))
                bmBtn.place(relx=1.0, rely=0.0, x=-10, y=10, anchor="ne")

                tk.Button(actBtnCont, text="Rate Business", bg=colors["button"], fg=colors["buttonText"], 
                         relief="flat", padx=10, cursor="hand2",
                          command=lambda b_id=biz_id, b_name=biz_name: self.openRatingPopup(b_id, b_name)).pack(side="right", padx=(10,0))
                tk.Button(actBtnCont, text="Write a Review", bg=colors["button"], fg=colors["buttonText"], 
                         relief="flat", padx=10, cursor="hand2", 
                         command=lambda b_id=biz_id, b_name=biz_name:
                        self.openReviewPopup(self.root, self.db, b_id, b_name)).pack(side="right", padx=(10, 0))
                
                #Button only shows when coupons are available
                active_coups = self.db.fetchCouponsByBusiness(biz_id)
                if active_coups:
                    tk.Button(actBtnCont, text="View Coupons", bg=colors["button"], fg=colors["buttonText"], 
                             relief="flat", padx=10, cursor="hand2",
                              command=lambda b_id=biz_id, b_name=biz_name: self.showBusinessCoupons(b_id, b_name)).pack(side="right", padx=(10, 0))

    #Function that creates the homepage when program is runs
    def homeUi(self):
        """Creates the homepage when program runs"""
        colors = self.getColors()
        
        # If mainPageFrame already exists, destroy it and create a new one
        if hasattr(self, 'mainPageFrame'):
            try:
                self.mainPageFrame.destroy()
            except:
                pass
        
        self.mainPageFrame = tk.Frame(self.root, bg=colors["bg"])
        self.mainPageFrame.place(relx=0.5, rely=0.5, anchor="center")
        
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            imgPath = os.path.join(script_dir, "logo.png")
            img = Image.open(imgPath).resize((500, 320))
            photo = ImageTk.PhotoImage(img)
            logoLabel = tk.Label(self.mainPageFrame, image=photo, bg=colors["bg"], bd=0)
            logoLabel.image = photo 
            logoLabel.grid(row=0, column=0, padx=0)
        except:
            tk.Label(self.mainPageFrame, text="[Logo Error]", 
                    bg=colors["bg"], fg=colors["text"], 
                    font=("Georgia", 20)).grid(row=0, column=0)
        
        #Pibbit title and slogan
        tk.Label(self.mainPageFrame, text="PIBBIT", 
                font=("Georgia", 100, "bold"),
                fg=colors["text"], bg=colors["bg"]).grid(row=0, column=1, sticky="w")
        
        # Slogan with special color handling
        slogan_color = "#6E2F20" if not self.darkMode else "#FFA07A"
        tk.Label(self.mainPageFrame, 
                text="Local business now becomes just a PIBBIT away",
                font=("Georgia", 25), fg=slogan_color, 
                bg=colors["bg"]).grid(row=1, column=1, sticky="w")

#Generating Costumizable Report-----------------------------------------------------------------------------------------------------------------------
    def printBusinesses(self, businesses, catName):
        self.updateInstructions("Preparing PDF report... Please wait.")
        #Generates presentatble report and prevents the report from printing businesses that aren't complete yet
        #Filtering input data by using list comprehension. if business is null then it removes it
        #We learned about Reportlab and how to effectively use it with-->
        #https://www.blog.pythonlibrary.org/2021/09/15/getting-started-with-reportlabs-canvas/
        filterInData = [b for b in businesses if b[1] and b[1] != "None"]
        
        if not filterInData:
            messagebox.showwarning("Print Error", "No valid businesses available to print.")
            return

        #This stops the pdf from printing in the vscode editorby using the system's temporary directory
        tempDirectory = tempfile.gettempdir()
        fileName = os.path.join(tempDirectory, f"{catName}_Report.pdf")
        
        try:
            printCanv = canvas.Canvas(fileName, pagesize=letter)
            width, height = letter
            #managing the y-coordinate
            y = height - 1*inch 

            #Header
            printCanv.setFont("Helvetica-Bold", 20)
            printCanv.drawString(1*inch, y, "PIBBIT Business Report")
            y -= 0.3*inch
            printCanv.setFont("Helvetica", 12)
            printCanv.drawString(1*inch, y, f"Category: {catName}")
            y -= 0.5*inch
            printCanv.line(1*inch, y + 0.1*inch, 7.5*inch, y + 0.1*inch)

            for biz in filterInData:
                if y < 1.5*inch: #Makes sure that when the businesses reach the bottom of the page, it automatically creates a new page to reset y to the top
                    printCanv.showPage()
                    y = height - 1*inch

                #Unpacks the tuples easily and directly
                _, name, rating, reviews, desc, link = biz
                
                #Businesses attributes directly to the pdf
                printCanv.setFont("Helvetica-Bold", 14)
                printCanv.drawString(1*inch, y, str(name))
                y -= 0.2*inch
                
                printCanv.setFont("Helvetica", 10)
                printCanv.drawString(1*inch, y, f"Rating: {rating or 0} | Reviews: {reviews or 0}")
                y -= 0.2*inch
                
                printCanv.setFont("Helvetica-Oblique", 10)
                description = str(desc)
                if len(description) > 90: description = description[:87] + "..."
                printCanv.drawString(1*inch, y, description)
                y -= 0.2*inch
                
                printCanv.setFont("Helvetica", 10)
                printCanv.setFillColorRGB(0, 0, 1) 
                printCanv.drawString(1*inch, y, f"Website: {link}")
                printCanv.setFillColorRGB(0, 0, 0) 
                
                y -= 0.4*inch 

            printCanv.save()
            
            #Opening the PDF automatically from the temp location
            os.startfile(fileName)
            self.updateInstructions("Report generated successfully!")
        #In case of an error, it notifies user
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate PDF: {e}")
            
#Coupons and Deals--------------------------------------------------------------------------------------------------------------------------------
    def showBusinessCoupons(self, biz_id, biz_name):
        colors = self.getColors()
        self.updateInstructions(f"Viewing deals for {biz_name}. Use the codes at checkout!")
        # Create a small popup window
        popup = tk.Toplevel(self.root)
        popup.title(f"Deals for {biz_name}")
        popup.geometry("500x400")
        popup.configure(bg=colors["card"])

        tk.Label(popup, text=f"Coupons for {biz_name}", 
                font=("Georgia", 14, "bold"), bg=colors["card"], fg=colors["cardText"], pady=10).pack()

        #Fetch specific coupons
        coupons = self.db.fetchCouponsByBusiness(biz_id)

        if not coupons:
            tk.Label(popup, text="No active coupons for this business.", 
                    font=("Georgia", 11), bg=colors["card"], fg=colors["cardText"]).pack(pady=50)
        else:
            for title, description, coupon_code in coupons:
                f = tk.Frame(popup, bg=colors["bg"] if self.darkMode else "white", 
                           relief="groove", bd=2, padx=10, pady=10)
                f.pack(fill="x", padx=20, pady=5)
                
                tk.Label(f, text=title, font=("Georgia", 12, "bold"), 
                        bg=f.cget('bg'), fg=colors["accent"]).pack(anchor="w")
                tk.Label(f, text=description, font=("Georgia", 10), 
                        bg=f.cget('bg'), fg=colors["cardText"], wraplength=400).pack(anchor="w")
                
                # The actual code
                codeLbl = tk.Label(f, text=f"CODE: {coupon_code}", font=("Courier", 12, "bold"), 
                                    bg="#F0F0F0", fg="#6E2F20", padx=5)
                codeLbl.pack(side="left", pady=5)
                
    def showAllCouponsPage(self):
        colors = self.getColors()
        self.current_view = 'coupons'
        self.updateInstructions("Local Savings: Browse all active deals in your area.")
        
        #Resetting UI
        self.mainPageFrame.place_forget()
        for widget in self.resultsContainer.winfo_children():
            widget.destroy()
        self.resultsContainer.pack(fill="both", expand=True)
        #Apply theme to results container
        self.resultsContainer.configure(bg=colors["bg"])

        #Setting up Canvas with Dynamic Width
        canvas = tk.Canvas(self.resultsContainer, bg=colors["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.resultsContainer, orient="vertical", command=canvas.yview)
        self.scrollingFrame = tk.Frame(canvas, bg=colors["bg"]) # Standardized name
        
        # This function ensures the frame expands to fill the canvas width
        def configure_canvas(e):
            canvas.itemconfig(
                canvas.create_window((0, 0), window=self.scrollingFrame, anchor="nw"), 
                width=e.width
            )
        canvas.bind('<Configure>', configure_canvas)
        
        self.scrollingFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # 3. Standard Header
        tk.Label(self.scrollingFrame, text="All Local Deals", font=("Georgia", 24, "bold"), 
                 bg=colors["bg"], fg=colors["text"], pady=20).pack()

        all_coupons = self.db.fetchAllCoupons()

        #Rendering Cards using the same logic as displayBusinesses
        for biz_name, title, desc, code in all_coupons:
            #Consistent Card Frame
            card = tk.Frame(self.scrollingFrame, bg=colors["card"], 
                            highlightbackground=colors["highlight"], highlightthickness=2,
                            padx=15, pady=10)
            
            #Using the same padding as the Business Cards
            card.pack(fill="x", pady=10, padx=50)

            #Business Name
            tk.Label(card, text=biz_name, font=("Georgia", 18, "bold"), 
                    bg=colors["card"], fg=colors["cardText"]).pack(anchor="w")
            
            #Coupon Details
            tk.Label(card, text=title, font=("Georgia", 14, "italic"), 
                    bg=colors["card"], fg=colors["accent"]).pack(anchor="w")
            tk.Label(card, text=desc, font=("Georgia", 11), 
                    bg=colors["card"], fg=colors["cardText"], wraplength=800, justify="left").pack(anchor="w", pady=5)
            
            #Standardized Footer Area
            footer = tk.Frame(card, bg=colors["card"])
            footer.pack(fill="x", pady=(10, 0))
            
            tk.Label(footer, text=f"CODE: {code}", font=("Courier", 14, "bold"), 
                     bg="#F0F0F0", fg="#6E2F20", padx=8, pady=4).pack(side="left")                
#Handling Captcha and bot safety after opening login and signup page--------------------------------------------------------------------------------------------------
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

    def openWebsite(self, website_link):
        try:
            self.updateInstructions(f"Opening browser to visit {website_link}...")
            webbrowser.open(website_link, new=2)
        except Exception as e:
            print(f"Error: {e}")
            
    def applyTheme(self):
        colors = self.getColors()

        #Root background
        self.root.configure(bg=colors["bg"])

        #Navbar and its children
        self.navBar.configure(bg=colors["nav"])
        
        #Update navigation buttons if they exist
        if hasattr(self, 'mb'):
            self.mb.configure(bg=colors["button"], fg=colors["buttonText"])
            # Update the menu colors
            if hasattr(self.mb, 'menu'):
                self.mb.menu.configure(bg=colors["button"], fg=colors["buttonText"])
        
        if hasattr(self, 'coupsNDeals'):
            self.coupsNDeals.configure(bg=colors["button"], fg=colors["buttonText"])
        
        if hasattr(self, 'helpBtn'):
            self.helpBtn.configure(bg=colors["button"], fg=colors["buttonText"])
        
        if hasattr(self, 'bookmarks'):
            self.bookmarks.configure(bg=colors["button"], fg=colors["buttonText"])
        
        if hasattr(self, 'darkBtn'):
            self.darkBtn.configure(
                text="☀️ Light Mode" if self.darkMode else "🌙 Dark Mode",
                bg=colors["button"], 
                fg=colors["buttonText"]
            )
        
        if hasattr(self, 'profileBtn'):
            self.profileBtn.configure(bg=colors["nav"], fg=colors["text"])
            if hasattr(self.profileBtn, 'menu'):
                self.profileBtn.menu.configure(bg=colors["card"], fg=colors["cardText"])
        
        if hasattr(self, 'signup_btn'):
            self.signup_btn.configure(bg=colors["button"], fg=colors["buttonText"])
        
        if hasattr(self, 'login_btn'):
            self.login_btn.configure(bg=colors["button"], fg=colors["buttonText"])
        
        if hasattr(self, 'home_button'):
            self.home_button.configure(bg=colors["nav"])

        #Results container
        self.resultsContainer.configure(bg=colors["bg"])

        #Footer
        self.footer.configure(bg=colors["footer"], fg="white")

        
        self.homeUi()
        
        if not self.mainPageFrame.winfo_ismapped():
            self.mainPageFrame.place_forget()

        #Updates cards if they exist
        if hasattr(self, "cardsFrame"):
            self.cardsFrame.configure(bg=colors["bg"])
            for card in self.cardsFrame.winfo_children():
                try:
                    card.configure(bg=colors["card"])
                    #Updates labels inside cards
                    for child in card.winfo_children():
                        if (isinstance(child, tk.Label)):
                            if ("★" in child.cget('text') or "☆" in child.cget('text')):
                                child.configure(bg=colors["card"], fg=colors["ratingStars"])
                            else:
                                child.configure(bg=colors["card"], fg=colors["cardText"])
                        if (isinstance(child, tk.Frame)):  # For action button container
                            child.configure(bg=colors["card"])
                            for btn in child.winfo_children():
                                if isinstance(btn, tk.Button):
                                    btn.configure(bg=colors["button"], fg=colors["buttonText"])
                except:
                    pass

        # Update scrolling frame if it exists
        if hasattr(self, 'scrollingFrame'):
            self.scrollingFrame.configure(bg=colors["bg"])
            
        # Update city menu if it exists
        if hasattr(self, 'citySelectDrpMenu'):
            self.citySelectDrpMenu.configure(bg=colors["button"], fg=colors["buttonText"])
            
        # Refresh current view to ensure all elements have correct theme
        self.refreshCurrentView()
    def toggleDarkMode(self):
        self.darkMode = not self.darkMode
        self.applyTheme()