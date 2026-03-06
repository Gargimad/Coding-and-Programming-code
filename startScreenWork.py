'''
Gargi Madala, Grace Wu, Dhanvi Ramkumar
Pibbit Start Screen - MAIN
FBLA- Coding and Programming
26 January 2026
'''
import tkinter as tk
from tkinter import messagebox
import os
import sys

# Import our modular components
from themes import Themes
from guiElements import NavBar, ScrollableFrame
from businessDisplay import BusinessDisplay
from coupons import CouponManager
from reports import ReportGenerator
from utilities import open_website, format_rating

# Database and page imports
from db import Database
from qna import QnaPage
from popUpControl import RatingPopup, ReviewPopup

# DPI Awareness
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class StartScreen:
    def __init__(self, root, userEmail):
        self.root = root
        self.db = Database()
        self.userEmail = userEmail
        self.theme = Themes()
        
        # Setup main window
        self.root.title("PIBBIT")
        self.root.state("zoomed")
        self.root.configure(bg=self.theme.get_colors()["bg"])
        
        # Initialize components
        self.coupon_manager = CouponManager(self.db, self.theme)
        self.business_display = None
        
        # Create containers
        self.navBar = tk.Frame(self.root)
        self.resultsContainer = tk.Frame(self.root)
        
        # Footer
        self.instructionVar = tk.StringVar(value="Welcome to PIBBIT! Use 'Explore' to find local businesses.")
        self.footer = tk.Label(
            self.root, textvariable=self.instructionVar,
            bg="#2D5A27", fg="white", font=("Georgia", 11, "italic"),
            pady=8, bd=1, relief="sunken"
        )
        self.footer.pack(side="bottom", fill="x")
        
        # Create callbacks dictionary
        self.callbacks = {
            'go_home': self.go_home,
            'explore': lambda: self.displayBusinesses(1, 'Explore', 0),
            'open_website': lambda url: open_website(url, self.updateInstructions),
            'rate_business': self.openRatingPopup,
            'write_review': self.openReviewPopup,
            'toggle_bookmark': self.onBookmarkToggle,
            'container': self.resultsContainer
        }
        
        # Create UI
        self.create_navbar()
        self.homeUi()
        
        # Initialize business display after callbacks are set
        self.business_display = BusinessDisplay(
            self.mainPageFrame, self.db, self.userEmail, 
            self.theme, self.callbacks
        )
    
    def create_navbar(self):
        """Create navigation bar using NavBar component"""
        self.nav_bar = NavBar(self.root, self.userEmail, self.callbacks, self.theme)
        self.navBar = self.nav_bar.frame
    
    def updateInstructions(self, text):
        self.instructionVar.set(text)
    
    def go_home(self):
        self.updateInstructions("Welcome Home! Select a category to start.")
        self.resultsContainer.pack_forget()
        self.mainPageFrame.place(relx=0.5, rely=0.5, anchor="center")
    
    def homeUi(self):
        colors = self.theme.get_colors()
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
        
        tk.Label(self.mainPageFrame, text="PIBBIT", 
                font=("Georgia", 100, "bold"),
                fg=colors["text"], bg=colors["bg"]).grid(row=0, column=1, sticky="w")
        tk.Label(self.mainPageFrame, 
                text="Local business now becomes just a PIBBIT away",
                font=("Georgia", 25), 
                fg="#6E2F20" if not self.theme.darkMode else "#FFA07A", 
                bg=colors["bg"]).grid(row=1, column=1, sticky="w")
    
    def displayBusinesses(self, sub_id, sub_name, city_id):
        self.mainPageFrame.place_forget()
        if self.business_display:
            self.business_display.show(sub_id, sub_name, city_id)
        self.resultsContainer.pack(fill="both", expand=True)
    
    def showQA(self):
        self.updateInstructions("Interactive Support: Browse common questions or search for help.")
        self.mainPageFrame.place_forget()
        for widget in self.resultsContainer.winfo_children():
            widget.destroy()
        self.resultsContainer.pack(fill="both", expand=True)
        QnaPage(self.resultsContainer, self.root).show()
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
            key=lambda b: (float(b[2]) if b[2] not in (None, "", "N/A") else 0.0), #Sorts list by using lambda
            reverse=True
        )
        self.renderBusinessCards(sortingBizes)

    def sortByReviews(self, businesses):
        self.updateInstructions("Sorting by review count: Showing the most discussed businesses.")
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
        colors = self.darkColors if self.darkMode else self.lightColors
        res = self.db.toggleBookmark(self.userEmail, biz_id)
        if res == "added":
            button.config(text="🔖 Bookmarked", bg=colors["bookmark_added"])
            self.updateInstructions("Business saved to your bookmarks!")
        else:
            button.config(text="☆ Bookmark", bg=colors["bookmark_remove"])
            self.updateInstructions("Business removed from bookmarks.")

    #Displays businesses on the resultsContainer frame with scrollbar frame        
#Selection of communities-------------------------------------------------------------------------------------------------------------------------------------
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

    def toggleDarkMode(self):
        self.theme.toggle()
        colors = self.theme.get_colors()
        
        # Update root
        self.root.configure(bg=colors["bg"])
        
        # Update navbar (you'll need to add a refresh method to NavBar)
        self.nav_bar.frame.configure(bg=colors["nav"])
        
        # Update footer
        self.footer.configure(bg=colors["footer"])
        
        # Update main page if visible
        if self.mainPageFrame.winfo_ismapped():
            self.mainPageFrame.configure(bg=colors["bg"])
            for widget in self.mainPageFrame.winfo_children():
                if isinstance(widget, tk.Label):
                    if widget.cget('text') == "PIBBIT":
                        widget.configure(bg=colors["bg"], fg=colors["text"])
        
        # Refresh current view
        self.darkBtn.config(text="☀️ Light Mode" if self.theme.darkMode else "🌙 Dark Mode")