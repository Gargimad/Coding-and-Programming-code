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
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
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
        self.navBar = tk.Frame(self.root, bg="#DAA520") #Setting up frame for the navigation bar at the tops
        self.navBar.pack(side="top", fill="x", padx=20, pady=20)
        self.resultsContainer = tk.Frame(self.root, bg="#DAA520") #Creating frame for the results container which will hold a lot of pages
        self.homeUi() #Creates the front Pibbit Page
        self.createDynamicNav() #Creates the navigation bar at the top
        
        
#Dynamic navigation bar using sqlite database values for easy navigation--------------------------------------------------------------------------------------
    def createDynamicNav(self):
        #Creating the dynamic navigation bar
        try: 
            #Creating the home logo next to the explore page for easy navigation
            homeLogo = Image.open(os.path.join(os.path.dirname(__file__), "homeLogo.png")).resize((50, 50)) #Sizing home page
            self.homeLogo = ImageTk.PhotoImage(homeLogo) #Using Tkinter image
            homeButton = tk.Button(self.navBar, image=self.homeLogo, bg="#DAA520", bd=0, cursor="hand2", 
                              command=lambda: [self.resultsContainer.pack_forget(), self.mainPageFrame.place(relx=0.5, rely=0.5, anchor="center")]
                              ).pack(side="left", padx=(0, 10)) #Home button to direct user back to home page when necessary
        except:
            messagebox.showwarning("Error", f"Could not load home logo")
        #Creating dynamic menubar dropdowns that sorts businesses by category name
        self.mb = tk.Menubutton( #Creating the menubutton for the Explore
            self.navBar, text="Explore ⏷", 
            bg="#2D5A27", fg="white", 
            font=("Georgia", 12), width=20, 
            direction='below', relief='flat', cursor="hand2")
        self.mb.pack(side="left", padx=(0,10))
#Sorting businesses by category------------------------------------------------------------------------------------------------------------------------
        #On click of explore, the button calls the function displayBusinesses and shows all businesses
        self.mb.bind("<Button-1>", lambda e: self.displayBusinesses(1, 'Explore',0))

        mainMenu = tk.Menu(self.mb, tearoff=0, bg="#2D5A27", fg="white", font=("Georgia", 11), activebackground="#3D7A35")
        self.mb["menu"] = mainMenu
        #Calling the categories from database
        categories = self.fetchCategories()  
        #Iterating the categories and subcategories and displaying business on click of each subcategory     
        for cat_id, cat_name in categories:
            subCatMenu = tk.Menu(mainMenu, tearoff=0, bg="#2D5A27", fg="white")
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
            self.guestExPgButtons(self.navBar, "Sign Up", "#2D5A27", self.openSignUp)
            self.guestExPgButtons(self.navBar, "Login", "#2D5A27", self.openLogin)
        
        else:
            #Creating buttons in the top navigation bar that are available only when user signs in
            #Coupons and deals
            self.coupsNDeals = tk.Button(self.navBar, text="Coupons and Deals", 
                                        bg="#2D5A27", fg="white", font=("Georgia", 12), 
                                        width=20, relief='flat', cursor="hand2")
            self.coupsNDeals.config(command=self.showAllCouponsPage) #Shows all coupons
            self.coupsNDeals.pack(side="left", padx=(0,10))
            
            #Interactive Q&A Button
            self.helpBtn = tk.Button(self.navBar, text="Help",
                                     bg="#2D5A27", fg="white", font=("Georgia", 12), 
                                     width=20, relief='flat', cursor="hand2", 
                                     command=self.showQA) # Pointing to new function
            self.helpBtn.pack(side="left", padx=(0,10))
            
            #Handling bookmarks with the buttons
            self.bookmarks = tk.Button(self.navBar, text="Bookmarks",
                                      bg="#2D5A27", fg="white", font=("Georgia", 12), 
                                      width=20, relief='flat', cursor="hand2",
                                      command=lambda: self.displayBusinesses(-1, "Bookmarks",0))
            self.bookmarks.pack(side="left", padx=(0,10))
            
            #Profile settings for logged in user
            self.profileBtn = tk.Menubutton(self.navBar, text="👤 Profile ✎", font=("Arial", 11),
                                            bg="#DAA520", relief="flat", cursor="hand2", width=20)
            self.profileBtn.pack(side="right")

            pfpMenuOpts = tk.Menu(self.profileBtn, tearoff=0, bg="white", fg="black")
            pfpMenuOpts.add_command(label="Edit Profile")
            pfpMenuOpts.add_command(label="Settings")
            pfpMenuOpts.add_separator()
            pfpMenuOpts.add_command(label="Logout")
            self.profileBtn["menu"] = pfpMenuOpts
            
#Intelligent Q&A -------------------------------------------------------------------------------------------------------------------------------------

    #Showing an interactive Q&A with data in another file - Modular code because the data is in another file- keeps things clean
    def showQA(self):
        #Hides the main frame
        self.mainPageFrame.place_forget()
        #Clears the result container to display this page
        for widget in self.resultsContainer.winfo_children():
            widget.destroy()  
        #Packs the container
        self.resultsContainer.pack(fill="both", expand=True)
        #Showing the qna page
        qnaPageShow = QnaPage(self.resultsContainer, self.root)
        qnaPageShow.show()

    #Defining guestExPgButtons which makes the login and Signup buttons at the top when user is not logged in
    def guestExPgButtons(self, parent, text, color, command):
        btn = tk.Button(parent, text=text, font=("Georgia", 12, "bold"),
                        bg=color, fg="white", width=15, pady=8,
                        bd=0, command=command, cursor="hand2")
        btn.pack(side="right", padx=10)

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
        #Sorting ratings by order- highest rating first and lowest rating last
        if not businesses: return
        sortingBizes = sorted(
            businesses,
            key=lambda b: (float(b[2]) if b[2] not in (None, "", "N/A") else 0.0),
            reverse=True
        )
        self.renderBusinessCards(sortingBizes)

    def sortByReviews(self, businesses):
        #Sorts businesses by review count- highest first to lowest last
        if not businesses: return
        sortingBizes = sorted(
            businesses,
            key=lambda b: (int(b[3]) if b[3] else 0),
            reverse=True
        )
        self.renderBusinessCards(sortingBizes)

#Bookmarks-----------------------------------------------------------------------------------------------------------------------------------------
    
    def onBookmarkToggle(self, biz_id, button):
        res = self.db.toggleBookmark(self.userEmail, biz_id)
        if res == "added":
            button.config(text="🔖 Bookmarked", bg="#E1AD01")
        else:
            button.config(text="☆ Bookmark", bg="#A2D98E")

    #Displays businesses on the resultsContainer frame with scrollbar frame
    def displayBusinesses(self, sub_id, sub_name, city_id):
        self.mainPageFrame.place_forget()
        #Destroys container before displaying new information
        for widget in self.resultsContainer.winfo_children():
            widget.destroy()
            
        self.resultsContainer.pack(fill="both", expand=True)
        #Creates the canvas that holds scrolling bar
        resultsContCanvas = tk.Canvas(self.resultsContainer, bg="#DAA520", highlightthickness=0) #Results Containter Canvas
        scrollbar = tk.Scrollbar(self.resultsContainer, orient="vertical", command=resultsContCanvas.yview)
        self.scrollingFrame = tk.Frame(resultsContCanvas, bg="#DAA520")
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
        top_bar = tk.Frame(self.scrollingFrame, bg="#DAA520")
        top_bar.pack(fill="x", pady=10, padx=50)

        #If explore is clicked, it displays all the businesses
        if sub_id == 1:
            tk.Label(top_bar, text="All Businesses:", 
                  font=("Georgia", 20, "bold"), bg="#DAA520").pack(side="left")
            businesses = self.fetchAllBusinesses()
        elif sub_id == -1:
            # Displays businesses that the user has saved
            tk.Label(top_bar, text="Your Bookmarked Businesses:", 
                  font=("Georgia", 20, "bold"), bg="#DAA520").pack(side="left")
            businesses = self.db.fetchBookmarkedBusinesses(self.userEmail)
        elif sub_id == 0 and city_id != 0:
            tk.Label(top_bar, text=f"Businesses in Selected City:", 
                  font=("Georgia", 20, "bold"), bg="#DAA520").pack(side="left")
            businesses = self.db.fetchBusinessByCity(city_id)
        else:
            tk.Label(top_bar, text=f"Results for {sub_name}:", 
                  font=("Georgia", 20, "bold"), bg="#DAA520").pack(side="left")
            businesses = self.fetchBusinessesBySubs(sub_id) 

        # Sorting Buttons
        sortingBtnFrame = tk.Frame(top_bar, bg="#DAA520")
        sortingBtnFrame.pack(side="right")
        self.city_mb = tk.Menubutton(sortingBtnFrame, text="Select GA City ⏷", 
                               bg="#2D5A27", fg="white", font=("Georgia", 10), 
                               width=15, relief="flat")
        self.city_mb.pack(side="left", padx=5)

        # Create the empty Menu object
        self.citySelectDrpMenu = tk.Menu(self.city_mb, tearoff=0, bg="#2D5A27", fg="white")
        self.city_mb["menu"] = self.citySelectDrpMenu

        # IMPORTANT: Bind the click event to trigger the dynamic update
        self.city_mb.bind("<Button-1>", lambda e: self.displayCities())
        tk.Button(sortingBtnFrame, text="Highest Ratings", bg="#2D5A27", fg="white", 
                  font=("Georgia", 10), width=15, relief="flat", cursor="hand2",
                  command=lambda: self.sortByRatings(businesses)).pack(side="left", padx=5)
        tk.Button(sortingBtnFrame, text="Most Reviewed", bg="#2D5A27", fg="white", 
                  font=("Georgia", 10), width=15, relief="flat", cursor="hand2",
                  command=lambda: self.sortByReviews(businesses)).pack(side="left", padx=5)
        tk.Button(sortingBtnFrame, text="🖨️", bg="#DAA520", fg="white", 
                  font=("Georgia", 15), width=4, relief="flat", cursor="hand2",
                  command= lambda: self.printBusinesses(businesses, sub_name)).pack(side="left", padx = 2)

        #Container where cards will actually be drawn
        self.cardsFrame = tk.Frame(self.scrollingFrame, bg="#DAA520")
        self.cardsFrame.pack(fill="both", expand=True)
        self.renderBusinessCards(businesses)
        
#Selection of communities-------------------------------------------------------------------------------------------------------------------------------------
    def displayCities(self):
        self.citySelectDrpMenu.delete(0, 'end')
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
            # Use default arguments in lambda (c_id=city_id) to avoid the "closure" bug
            command=lambda c_id=city_id, c_name=city_name: self.displayBusinesses(0,0, c_id)
        )
            
    def renderBusinessCards(self, businesses):
        # Clear existing cards first
        for widget in self.cardsFrame.winfo_children():
            widget.destroy()
        if not businesses:
            tk.Label(self.cardsFrame, text="No businesses found.", bg="#DAA520", font=("Georgia", 12)).pack(pady=20)
            return
        for biz_id, biz_name, rating, review_count, description, website_link in businesses:
            if any(field is None for field in [biz_name, description, website_link]):
                continue
            bizCard = tk.Frame(self.cardsFrame, bg="#DDE0D6", highlightbackground="#6B8E23", 
                               highlightthickness=2, padx=15, pady=10)
            bizCard.pack(fill="x", pady=10, padx=50)               
            tk.Label(bizCard, text=biz_name, font=("Georgia", 18, "bold"), bg="#DDE0D6").pack(anchor="w")
            #Rating display
            rateValue = float(rating) if rating else 0.0
            stars = "★" * int(rateValue) + "☆" * (5 - int(rateValue))
            tk.Label(bizCard, text=f"{stars} {rateValue} ({review_count or 0} reviews)", 
                     font=("Georgia", 12), bg="#DDE0D6", fg="#E1AD01").pack(anchor="w")
            tk.Label(bizCard, text=f"{description}", font=("Georgia", 10), bg="#DDE0D6", 
                     wraplength=800, justify="left").pack(anchor='w', pady=5)
            
            #Action Buttons Container
            actBtnCont = tk.Frame(bizCard, bg="#DDE0D6")
            actBtnCont.pack(fill="x", side="bottom")

            tk.Button(actBtnCont, text="Website Link", bg="#E4937A", relief="flat", padx=10, cursor="hand2",
                      command=lambda link=website_link: self.openWebsite(link)).pack(side="right", padx=5)

            if self.userEmail:
                bmSaved = self.db.isBookmarked(self.userEmail, biz_id)
                bmTxt = "🔖 Bookmarked" if bmSaved else "☆ Bookmark"
                bmColor = "#E1AD01" if bmSaved else "#A2D98E"
                
                bmBtn = tk.Button(bizCard, text=bmTxt, bg=bmColor, relief="flat", padx=10, cursor="hand2")
                bmBtn.config(command=lambda b=biz_id, btn=bmBtn: self.onBookmarkToggle(b, btn))
                bmBtn.place(relx=1.0, rely=0.0, x=-10, y=10, anchor="ne")

                tk.Button(actBtnCont, text="Rate Business", bg="#A2D98E", relief="flat", padx=10, cursor="hand2",
                          command=lambda b_id=biz_id, b_name=biz_name: self.openRatingPopup(b_id, b_name)).pack(side="right", padx=(10,0))
                tk.Button(actBtnCont, text="Write a Review", bg="#A2D98E", relief="flat", padx=10, cursor="hand2", command=lambda b_id=biz_id, b_name=biz_name:
                        self.openReviewPopup(self.root, self.db, b_id, b_name)).pack(side="right", padx=(10, 0))
                
                #Button only shows when coupons are available
                active_coups = self.db.fetchCouponsByBusiness(biz_id)
                if active_coups:
                    tk.Button(actBtnCont, text="View Coupons", bg="#A2D98E", relief="flat", padx=10, cursor="hand2",
                              command=lambda b_id=biz_id, b_name=biz_name: self.showBusinessCoupons(b_id, b_name)).pack(side="right", padx=(10, 0))

    #Function that creates the homepage when program is runs
    def homeUi(self):
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
            tk.Label(self.mainPageFrame, text="[Logo Error]", bg="#DAA520", fg="white", font=("Georgia", 20)).grid(row=0, column=0)
        #Pibbit title and slogan in the first screen when run
        tk.Label(self.mainPageFrame, text="PIBBIT", font=("Georgia", 100, "bold"),
                 fg="black", bg="#DAA520").grid(row=0, column=1, sticky="w")
        tk.Label(self.mainPageFrame, text="Local business now becomes just a PIBBIT away",
                 font=("Georgia", 25), fg="#6E2F20", bg="#DAA520").grid(row=1, column=1, sticky="w")

#Generating Costumizable Report-----------------------------------------------------------------------------------------------------------------------
    def printBusinesses(self, businesses, catName):
        #Generates presentatble report and prevents the report from printing businesses that aren't complete yet
        #Filtering input data by using list comprehension. if business is null then it removes it
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
            
            # Open the PDF automatically from the temp location
            os.startfile(fileName)
        #In case of an error, it notifies user
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate PDF: {e}")
            
#Coupons and Deals--------------------------------------------------------------------------------------------------------------------------------
    def showBusinessCoupons(self, biz_id, biz_name):
        # Create a small popup window
        popup = tk.Toplevel(self.root)
        popup.title(f"Deals for {biz_name}")
        popup.geometry("500x400")
        popup.configure(bg="#DDE0D6")

        tk.Label(popup, text=f"Coupons for {biz_name}", 
                font=("Georgia", 14, "bold"), bg="#DDE0D6", pady=10).pack()

        # Fetch specific coupons
        coupons = self.db.fetchCouponsByBusiness(biz_id)

        if not coupons:
            tk.Label(popup, text="No active coupons for this business.", 
                    font=("Georgia", 11), bg="#DDE0D6").pack(pady=50)
        else:
            for title, description, coupon_code in coupons:
                f = tk.Frame(popup, bg="white", relief="groove", bd=2, padx=10, pady=10)
                f.pack(fill="x", padx=20, pady=5)
                
                tk.Label(f, text=title, font=("Georgia", 12, "bold"), bg="white", fg="#2D5A27").pack(anchor="w")
                tk.Label(f, text=description, font=("Georgia", 10), bg="white", wraplength=400).pack(anchor="w")
                
                # The actual code
                code_lbl = tk.Label(f, text=f"CODE: {coupon_code}", font=("Courier", 12, "bold"), 
                                    bg="#F0F0F0", fg="#6E2F20", padx=5)
                code_lbl.pack(side="left", pady=5)
                
    def showAllCouponsPage(self):
        self.mainPageFrame.place_forget()
        for widget in self.resultsContainer.winfo_children():
            widget.destroy()
        self.resultsContainer.pack(fill="both", expand=True)

        tk.Label(self.resultsContainer, text="All Local Deals", font=("Georgia", 24, "bold"), bg="#DAA520").pack(pady=20)
        
        # This assumes your db.py has fetchAllCoupons()
        all_coupons = self.db.fetchAllCoupons() 
        
        if not all_coupons:
            tk.Label(self.resultsContainer, text="No active deals found.", bg="#DAA520").pack()
        else:
            # Loop through and create simple labels or frames for each coupon
            for biz_name, title, description, coupon_code in all_coupons:
                lbl = tk.Label(self.resultsContainer, text=f"{biz_name}: {title} - Use Code: {coupon_code}\n {description}", 
                            bg="#DDE0D6", pady=5, font=("Georgia", 12))
                lbl.pack(fill="x", padx=50, pady=2)
                
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
            webbrowser.open(website_link, new=2)
        except Exception as e:
            print(f"Error: {e}")