'''
Gargi Madala, Grace Wu, Dhanvi Ramkumar
Pibbit Start Screen
FBLA- Coding and Programming
26 January 2026
'''
#Imports:
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from db import Database
import webbrowser
import os
from qna import QnaPage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import tempfile

#Try/Except to help features fit into computers with different sizes
try: 
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class StartScreen:
    #Innitializing the class
    def __init__(self, root, userEmail):
        #Connecting to database and controlling tkinter application framework
        self.root = root
        self.db = Database()
        self.root.title("PIBBIT")
        self.root.state("zoomed")
        self.root.configure(bg="#DAA520")
        
        self.userEmail = userEmail
        self.navBar = tk.Frame(self.root, bg="#DAA520")
        self.navBar.pack(side="top", fill="x", padx=20, pady=20)
        self.resultsContainer = tk.Frame(self.root, bg="#DAA520")
        
        self.createUi() #Creates the front Pibbit Page
        self.createDynamicNav() #Creates the navigation bar at the top

    def createDynamicNav(self):
        # Adding a logo button to the left of the Explore button
        try: 
            homeLogo = Image.open(os.path.join(os.path.dirname(__file__), "homeLogo.png")).resize((50, 50))
            self.homeLogo = ImageTk.PhotoImage(homeLogo)
            tk.Button(self.navBar, image=self.homeLogo, bg="#DAA520", bd=0, cursor="hand2", 
                      command=lambda: [self.resultsContainer.pack_forget(), self.mainPageFrame.place(relx=0.5, rely=0.5, anchor="center")]
                     ).pack(side="left", padx=(0, 10))
        except:
            pass
        #Creating dynamic menubar dropdowns that sorts businesses by category name
        self.mb = tk.Menubutton(
            self.navBar, text="Explore ⏷", 
            bg="#2D5A27", fg="white", 
            font=("Georgia", 12), width=20, 
            direction='below', relief='flat', cursor="hand2")
        self.mb.pack(side="left", padx=(0,10))
        
        #On click of explore, the button calls the function displayBusinesses and shows all businesses
        self.mb.bind("<Button-1>", lambda e: self.displayBusinesses(1, 'Explore',0))

        mainMenu = tk.Menu(self.mb, tearoff=0, bg="#2D5A27", fg="white", font=("Georgia", 11), activebackground="#3D7A35")
        self.mb["menu"] = mainMenu
        #Calling the categories from database
        categories = self.fetchCategories()  
        #Iterating the categories and subcategories and displaying business on click of each subcategory     
        for cat_id, cat_name in categories:
            sub_menu = tk.Menu(mainMenu, tearoff=0, bg="#2D5A27", fg="white")
            subcategories = self.fetchSubcategories(cat_id)
            for sub_id, sub_name in subcategories:
                sub_menu.add_command(
                    label=sub_name,
                    command=lambda sId=sub_id, sName=sub_name: self.displayBusinesses(sId, sName,0) 
                )
            mainMenu.add_cascade(label=cat_name, menu=sub_menu)
        #Displaying sign up and login button when user has not signed in
        if not self.userEmail:
            self.createButton(self.navBar, "Sign Up", "#2D5A27", self.openSignUp)
            self.createButton(self.navBar, "Login", "#2D5A27", self.openLogin)
        
        else:
            #Creating buttons in the top navigation bar that are available only when user signs in
            self.coupsNDeals = tk.Button(self.navBar, text="Coupons and Deals", 
                                        bg="#2D5A27", fg="white", font=("Georgia", 12), 
                                        width=20, relief='flat', cursor="hand2")
            self.coupsNDeals.config(command=self.showAllCouponsPage)
            self.coupsNDeals.pack(side="left", padx=(0,10))
            
            self.qna_btn = tk.Button(self.navBar, text="Q&A",
                                     bg="#2D5A27", fg="white", font=("Georgia", 12), 
                                     width=20, relief='flat', cursor="hand2", 
                                     command=self.showQna)
            self.qna_btn.pack(side="left", padx=(0,10))
            
            self.bookmarks = tk.Button(self.navBar, text="Bookmarks",
                                      bg="#2D5A27", fg="white", font=("Georgia", 12), 
                                      width=20, relief='flat', cursor="hand2",
                                      command=lambda: self.displayBusinesses(-1, "Bookmarks",0))
            self.bookmarks.pack(side="left", padx=(0,10))
            
            #Profile settings for logged in user
            self.profile_btn = tk.Menubutton(self.navBar, text="👤 Profile ✎", font=("Arial", 11),
                                            bg="#DAA520", relief="flat", cursor="hand2", width=20)
            self.profile_btn.pack(side="right")

            profile_menu = tk.Menu(self.profile_btn, tearoff=0, bg="white", fg="black")
            profile_menu.add_command(label="Edit Profile")
            profile_menu.add_command(label="Settings")
            profile_menu.add_separator()
            profile_menu.add_command(label="Logout")
            self.profile_btn["menu"] = profile_menu

    #Function that displays the QnA
    def showQna(self):
        self.mainPageFrame.place_forget()
        for widget in self.resultsContainer.winfo_children():
            widget.destroy()
            
        self.resultsContainer.pack(fill="both", expand=True)
        colors = {'bg': "#DAA520", 'darkText': "black", 'navBg': "#2D5A27"}
        qna_view = QnaPage(self.resultsContainer, colors)
        qna_view.draw()

    #Defining createButton which makes the login and Signup buttons at the top when user is not logged in
    def createButton(self, parent, text, color, command):
        btn = tk.Button(parent, text=text, font=("Georgia", 12, "bold"),
                        bg=color, fg="white", width=15, pady=8,
                        bd=0, command=command, cursor="hand2")
        btn.pack(side="right", padx=10)

    # Function to create the interactive star rating popup
    def openRatingPopup(self, biz_id, biz_name):
        popup = tk.Toplevel(self.root)
        popup.title(f"Rate {biz_name}")
        popup.geometry("450x250")
        popup.configure(bg="#DAA520")
        
        tk.Label(popup, text=f"Rate {biz_name}", 
                 font=("Georgia", 14, "bold"), bg="#DAA520").pack(pady=15)

        star_frame = tk.Frame(popup, bg="#DAA520")
        star_frame.pack()

        self.selected_rating = 0
        star_buttons = []

        def set_rating(score):
            self.selected_rating = score
            for i, btn in enumerate(star_buttons):
                btn.config(fg="#FFD700" if i < score else "#C0C0C0")

        for i in range(1, 6):
            btn = tk.Button(star_frame, text="★", font=("Arial", 30),
                            bg="#DAA520", fg="#C0C0C0", bd=0, 
                            activebackground="#DAA520", cursor="hand2",
                            command=lambda s=i: set_rating(s))
            btn.pack(side="left")
            star_buttons.append(btn)

        def submit_rating():
            if self.selected_rating == 0:
                messagebox.showwarning("Selection Required", "Please select a star rating!")
                return
            
            success = self.db.updateBusinessRating(biz_id, self.selected_rating)
            if success:
                #messagebox.showinfo("Success", "Business rated successfully!")
                popup.destroy()
                self.displayBusinesses(1, "Explore",0) 
            else:
                messagebox.showerror("Error", "Could not submit rating.")

        tk.Button(popup, text="Submit Rating", bg="#2D5A27", fg="white", font=("Georgia", 10, "bold"),
                  padx=20, command=submit_rating, cursor="hand2").pack(pady=25)

    #Fetches categories from category table in pibbit database
    def openReviewPopup(self, biz_id, biz_name):
        #opens new screen
        popup = tk.Toplevel(self.root)
        popup.title(f"Review {biz_name}")
        popup.geometry("800x500")
        popup.configure(bg="#DAA520")
        popup.grab_set()

        tk.Label(
            popup,
            text=f"Write a review for {biz_name}",
            font=("Georgia", 16, "bold"),
            bg="#DAA520"
        ).pack(pady=15)

        #Write review
        review_box = tk.Text(
            popup,
            height=10,
            font=("Georgia", 11),
            wrap="word"
        )
        review_box.pack(padx=20, pady=10, fill="both", expand=True)

        def submit_review():
            review_text = review_box.get("1.0", "end").strip()
            if not review_text:
                return

            # TODO: save to DB
            # self.db.saveReview(self.userEmail, biz_id, review_text)

            popup.destroy()

        tk.Button(
            popup,
            text="Submit Review",
            bg="#2D5A27",
            fg="white",
            font=("Georgia", 12),
            relief="flat",
            command=submit_review
        ).pack(pady=15)
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

    def sortByRatings(self, businesses):
        """Sorts businesses by rating (highest first)"""
        if not businesses: return
        sorted_list = sorted(
            businesses,
            key=lambda b: (float(b[2]) if b[2] not in (None, "", "N/A") else 0.0),
            reverse=True
        )
        self.renderBusinessCards(sorted_list)

    def sortByReviews(self, businesses):
        """Sorts businesses by review count (highest first)"""
        if not businesses: return
        sorted_list = sorted(
            businesses,
            key=lambda b: (int(b[3]) if b[3] else 0),
            reverse=True
        )
        self.renderBusinessCards(sorted_list)

    # Internal function to handle bookmark click and UI update
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
        canvas = tk.Canvas(self.resultsContainer, bg="#DAA520", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.resultsContainer, orient="vertical", command=canvas.yview)
        self.scrollingFrame = tk.Frame(canvas, bg="#DAA520")
        self.scrollingFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=self.scrollingFrame, anchor="nw")
        
        #Calls the function that configures the canvas created before
        def configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', configure_canvas)

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

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
        button_frame = tk.Frame(top_bar, bg="#DAA520")
        button_frame.pack(side="right")
        self.city_mb = tk.Menubutton(button_frame, text="Select GA City ⏷", 
                             bg="#2D5A27", fg="white", font=("Georgia", 10), 
                             width=15, relief="flat")
        self.city_mb.pack(side="left", padx=5)

        # Create the empty Menu object
        self.city_menu = tk.Menu(self.city_mb, tearoff=0, bg="#2D5A27", fg="white")
        self.city_mb["menu"] = self.city_menu

        # IMPORTANT: Bind the click event to trigger the dynamic update
        self.city_mb.bind("<Button-1>", lambda e: self.displayCities())
        tk.Button(button_frame, text="Highest Ratings", bg="#2D5A27", fg="white", 
                  font=("Georgia", 10), width=15, relief="flat", cursor="hand2",
                  command=lambda: self.sortByRatings(businesses)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Most Reviewed", bg="#2D5A27", fg="white", 
                  font=("Georgia", 10), width=15, relief="flat", cursor="hand2",
                  command=lambda: self.sortByReviews(businesses)).pack(side="left", padx=5)
        tk.Button(button_frame, text="🖨️", bg="#DAA520", fg="white", 
                  font=("Georgia", 15), width=4, relief="flat", cursor="hand2",
                  command= lambda: self.printBusinesses(businesses, sub_name)).pack(side="left", padx = 2)

        # Container where cards will actually be drawn
        self.cards_frame = tk.Frame(self.scrollingFrame, bg="#DAA520")
        self.cards_frame.pack(fill="both", expand=True)
        
        self.renderBusinessCards(businesses)
    def displayCities(self):
        self.city_menu.delete(0, 'end')
        cities = self.db.fetchCities()
        if not cities:
            self.city_menu.add_command(label="No cities found", state="disabled")
            return
    # 3. Add an "All Cities" option
        self.city_menu.add_command(label="All Cities", command=lambda: self.displayBusinesses(1, "Explore", 0))
        self.city_menu.add_separator()
        for city_id, city_name in cities:
            self.city_menu.add_command(
            label=city_name,
            # Use default arguments in lambda (c_id=city_id) to avoid the "closure" bug
            command=lambda c_id=city_id, c_name=city_name: self.displayBusinesses(0,0, c_id)
        )
            
    def renderBusinessCards(self, businesses):
        # Clear existing cards first
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        if not businesses:
            tk.Label(self.cards_frame, text="No businesses found.", bg="#DAA520", font=("Georgia", 12)).pack(pady=20)
            return

        for biz_id, biz_name, rating, review_count, description, website_link in businesses:
            if any(field is None for field in [biz_name, description, website_link]):
                continue
            
            bizCard = tk.Frame(self.cards_frame, bg="#DDE0D6", highlightbackground="#6B8E23", 
                               highlightthickness=2, padx=15, pady=10)
            bizCard.pack(fill="x", pady=10, padx=50)               
            
            tk.Label(bizCard, text=biz_name, font=("Georgia", 18, "bold"), bg="#DDE0D6").pack(anchor="w")
            
            #Rating display
            rating_val = float(rating) if rating else 0.0
            stars = "★" * int(rating_val) + "☆" * (5 - int(rating_val))
            tk.Label(bizCard, text=f"{stars} {rating_val} ({review_count or 0} reviews)", 
                     font=("Georgia", 12), bg="#DDE0D6", fg="#E1AD01").pack(anchor="w")
            
            tk.Label(bizCard, text=f"{description}", font=("Georgia", 10), bg="#DDE0D6", 
                     wraplength=800, justify="left").pack(anchor='w', pady=5)
            
            # Action Buttons
            btn_container = tk.Frame(bizCard, bg="#DDE0D6")
            btn_container.pack(fill="x", side="bottom")

            tk.Button(btn_container, text="Website Link", bg="#E4937A", relief="flat", padx=10, cursor="hand2",
                      command=lambda link=website_link: self.openWebsite(link)).pack(side="right", padx=5)

            if self.userEmail:
                is_saved = self.db.isBookmarked(self.userEmail, biz_id)
                bm_text = "🔖 Bookmarked" if is_saved else "☆ Bookmark"
                bm_color = "#E1AD01" if is_saved else "#A2D98E"
                
                bm_btn = tk.Button(bizCard, text=bm_text, bg=bm_color, relief="flat", padx=10, cursor="hand2")
                bm_btn.config(command=lambda b=biz_id, btn=bm_btn: self.onBookmarkToggle(b, btn))
                bm_btn.place(relx=1.0, rely=0.0, x=-10, y=10, anchor="ne")

                tk.Button(btn_container, text="Rate Business", bg="#A2D98E", relief="flat", padx=10, cursor="hand2",
                          command=lambda b_id=biz_id, b_name=biz_name: self.openRatingPopup(b_id, b_name)).pack(side="right", padx=(10,0))
                tk.Button(btn_container, text="Write a Review", bg="#A2D98E", relief="flat", padx=10, cursor="hand2", command=lambda b_id=biz_id, b_name=biz_name:
                        self.openReviewPopup(b_id, b_name)).pack(side="right", padx=(10, 0))
                tk.Button(btn_container, text="View Coupons", bg="#A2D98E", relief="flat", padx=10, cursor="hand2",
                          command=lambda b_id=biz_id, b_name=biz_name: self.showBusinessCoupons(b_id, b_name)).pack(side="right", padx=(10, 0))


    #Function that gets called when website link is clicked
    def openWebsite(self, website_link):
        try:
            webbrowser.open(website_link, new=2)
        except Exception as e:
            print(f"Error: {e}")

    #Function that creates the homepage when program is runs
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
            tk.Label(self.mainPageFrame, text="[Logo Error]", bg="#DAA520", fg="white", font=("Georgia", 20)).grid(row=0, column=0)
        #Pibbit title and slogan in the first screen when run
        tk.Label(self.mainPageFrame, text="PIBBIT", font=("Georgia", 100, "bold"),
                 fg="black", bg="#DAA520").grid(row=0, column=1, sticky="w")
        tk.Label(self.mainPageFrame, text="Local business now becomes just a PIBBIT away",
                 font=("Georgia", 25), fg="#6E2F20", bg="#DAA520").grid(row=1, column=1, sticky="w")
        
    def printBusinesses(self, businesses, category_name):
        """Generates a professional PDF report without saving it in the project folder."""
        # FIX: Filter out None/Empty businesses before printing
        valid_businesses = [b for b in businesses if b[1] and b[1] != "None"]
        
        if not valid_businesses:
            messagebox.showwarning("Print Error", "No valid businesses available to print.")
            return

        # FIX: Create path in the system temp directory to avoid VS Code folder
        temp_dir = tempfile.gettempdir()
        filename = os.path.join(temp_dir, f"{category_name}_Report.pdf")
        
        try:
            c = canvas.Canvas(filename, pagesize=letter)
            width, height = letter
            y = height - 1*inch 

            # Header
            c.setFont("Helvetica-Bold", 20)
            c.drawString(1*inch, y, "PIBBIT Business Report")
            y -= 0.3*inch
            c.setFont("Helvetica", 12)
            c.drawString(1*inch, y, f"Category: {category_name}")
            y -= 0.5*inch
            c.line(1*inch, y + 0.1*inch, 7.5*inch, y + 0.1*inch)

            for biz in valid_businesses:
                if y < 1.5*inch:
                    c.showPage()
                    y = height - 1*inch

                # Unpacking the tuple directly
                _, name, rating, reviews, desc, link = biz
                
                # Business Attributes directly into PDF
                c.setFont("Helvetica-Bold", 14)
                c.drawString(1*inch, y, str(name))
                y -= 0.2*inch
                
                c.setFont("Helvetica", 10)
                c.drawString(1*inch, y, f"Rating: {rating or 0} | Reviews: {reviews or 0}")
                y -= 0.2*inch
                
                c.setFont("Helvetica-Oblique", 10)
                description = str(desc)
                if len(description) > 90: description = description[:87] + "..."
                c.drawString(1*inch, y, description)
                y -= 0.2*inch
                
                c.setFont("Helvetica", 10)
                c.setFillColorRGB(0, 0, 1) 
                c.drawString(1*inch, y, f"Website: {link}")
                c.setFillColorRGB(0, 0, 0) 
                
                y -= 0.4*inch 

            c.save()
            
            # Open the PDF automatically from the temp location
            os.startfile(filename)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate PDF: {e}")
    def showBusinessCoupons(self, biz_id, biz_name):
        # Create a small popup window
        popup = tk.Toplevel(self.root)
        popup.title(f"Deals for {biz_name}")
        popup.geometry("500x400")
        popup.configure(bg="#DDE0D6")

        tk.Label(popup, text=f"Active Coupons: {biz_name}", 
                font=("Georgia", 14, "bold"), bg="#DDE0D6", pady=10).pack()

        # Fetch specific coupons
        coupons = self.db.fetchCouponsByBusiness(biz_id)

        if not coupons:
            tk.Label(popup, text="No active coupons for this business.", 
                    font=("Georgia", 11), bg="#DDE0D6").pack(pady=50)
        else:
            for title, desc, code, expiry in coupons:
                f = tk.Frame(popup, bg="white", relief="groove", bd=2, padx=10, pady=10)
                f.pack(fill="x", padx=20, pady=5)
                
                tk.Label(f, text=title, font=("Georgia", 12, "bold"), bg="white", fg="#2D5A27").pack(anchor="w")
                tk.Label(f, text=desc, font=("Georgia", 10), bg="white", wraplength=400).pack(anchor="w")
                
                # The actual code
                code_lbl = tk.Label(f, text=f"CODE: {code}", font=("Courier", 12, "bold"), 
                                    bg="#F0F0F0", fg="#6E2F20", padx=5)
                code_lbl.pack(side="left", pady=5)
                
                if expiry:
                    tk.Label(f, text=f"Expires: {expiry}", font=("Arial", 8), bg="white").pack(side="right")
    def showAllCouponsPage(self):
        """Displays all coupons from all businesses in the main results container."""
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
            for biz_name, title, code in all_coupons:
                lbl = tk.Label(self.resultsContainer, text=f"{biz_name}: {title} - Use Code: {code}", 
                            bg="#DDE0D6", pady=5, font=("Georgia", 12))
                lbl.pack(fill="x", padx=50, pady=2)
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