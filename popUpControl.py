'''
Gargi Madala, Grace Wu, Dhanvi Ramkumar
Pibbit Rating and Reviews Popup Control
FBLA- Coding and Programming
26 January 2026
'''
#Imports
import tkinter as tk
from tkinter import messagebox
from db import Database

class RatingPopup:
    def __init__(self, root, db, biz_id, biz_name, refreshCallBck):
        #Innitialization
        self.root = root
        self.db = db
        self.biz_id = biz_id
        self.refreshCallBck = refreshCallBck
        self.ratingGiven = 0

        #Popup logic
        self.popUp = tk.Toplevel(self.root)
        self.popUp.title(f"Rate {biz_name}")
        self.popUp.geometry("450x250")
        self.popUp.configure(bg="#DAA520")
        self.popUp.grab_set()
        
        #Main content of the popup
        tk.Label(self.popUp, text=f"Rate {biz_name}", 
                 font=("Georgia", 14, "bold"), bg="#DAA520").pack(pady=15)
        #Rating location frame
        ratingLocFrame = tk.Frame(self.popUp, bg="#DAA520")
        ratingLocFrame.pack()
        self.starBtns = []
        
        #For loop to show stars whenever user clicks 'rate business'
        for i in range(1, 6):
            btn = tk.Button(ratingLocFrame, text="★", font=("Arial", 30),
                            bg="#DAA520", fg="#C0C0C0", bd=0, 
                            activebackground="#DAA520", cursor="hand2",
                            command=lambda s=i: self.setRating(s))
            btn.pack(side="left")
            self.starBtns.append(btn)
        #submits rating to add to the total rating average
        tk.Button(self.popUp, text="Submit Rating", bg="#2D5A27", fg="white", 
                  font=("Georgia", 10, "bold"), padx=20, 
                  command=self.submitRating, cursor="hand2").pack(pady=25)
        
    #Allowing user to set rating
    def setRating(self, score):
        self.ratingGiven = score
        for i, btn in enumerate(self.starBtns):
            btn.config(fg="#FFD700" if i < score else "#C0C0C0")
            
    #Allowing user to submit rating
    def submitRating(self):
        if self.ratingGiven == 0:
            messagebox.showwarning("Selection Required", "Please select a star rating!")
            return
        success = self.db.updateBusinessRating(self.biz_id, self.ratingGiven)
        if success:
            self.popUp.destroy()
            if (self.refreshCallBck):
                self.refreshCallBck(1, "Explore", 0) 
        else:
            messagebox.showerror("Error", "Could not submit rating.")
            
#Handling reviews
class ReviewPopup:
    def __init__(self, root, db, biz_id, biz_name, userEmail):
        #Innitialization
        self.root = root
        self.db = db
        self.biz_id = biz_id
        self.userEmail = userEmail
        self.popUp = tk.Toplevel(self.root)
        self.popUp.title(f"Review {biz_name}")
        self.popUp.geometry("800x500")
        self.popUp.configure(bg="#DAA520")
        self.popUp.grab_set()
        #Review popup content
        tk.Label(self.popUp, text=f"Write a review for {biz_name}",
                 font=("Georgia", 16, "bold"), bg="#DAA520").pack(pady=15)

        self.reviewBox = tk.Text(self.popUp, height=10, font=("Georgia", 11), wrap="word")
        self.reviewBox.pack(padx=20, pady=10, fill="both", expand=True)
        #Allows user to submit review
        def submitReview():
            reviewInputText = self.reviewBox.get("1.0", "end").strip()
            if not reviewInputText:
                return
            self.db.saveReview(self.userEmail, biz_id, reviewInputText)
            self.popUp.destroy()
        #Submitting review button
        tk.Button(self.popUp, text="Submit Review", bg="#2D5A27", fg="white",
                  font=("Georgia", 12), relief="flat", command=submitReview).pack(pady=15)