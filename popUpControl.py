import tkinter as tk
from tkinter import messagebox
from db import Database
class RatingPopup:
    def __init__(self, root, db, biz_id, biz_name, refresh_callback):
        self.root = root
        self.db = db
        self.biz_id = biz_id
        self.refresh_callback = refresh_callback
        self.ratingGiven = 0

        self.popup = tk.Toplevel(self.root)
        self.popup.title(f"Rate {biz_name}")
        self.popup.geometry("450x250")
        self.popup.configure(bg="#DAA520")
        self.popup.grab_set()
        
        tk.Label(self.popup, text=f"Rate {biz_name}", 
                 font=("Georgia", 14, "bold"), bg="#DAA520").pack(pady=15)

        ratingLocFrame = tk.Frame(self.popup, bg="#DAA520")
        ratingLocFrame.pack()

        self.star_buttons = []
        for i in range(1, 6):
            btn = tk.Button(ratingLocFrame, text="★", font=("Arial", 30),
                            bg="#DAA520", fg="#C0C0C0", bd=0, 
                            activebackground="#DAA520", cursor="hand2",
                            command=lambda s=i: self.setRating(s))
            btn.pack(side="left")
            self.star_buttons.append(btn)

        tk.Button(self.popup, text="Submit Rating", bg="#2D5A27", fg="white", 
                  font=("Georgia", 10, "bold"), padx=20, 
                  command=self.submitRating, cursor="hand2").pack(pady=25)

    def setRating(self, score):
        self.ratingGiven = score
        for i, btn in enumerate(self.star_buttons):
            btn.config(fg="#FFD700" if i < score else "#C0C0C0")

    def submitRating(self):
        if self.ratingGiven == 0:
            messagebox.showwarning("Selection Required", "Please select a star rating!")
            return
        
        success = self.db.updateBusinessRating(self.biz_id, self.ratingGiven)
        if success:
            self.popup.destroy()
            self.refresh_callback(1, "Explore", 0) 
        else:
            messagebox.showerror("Error", "Could not submit rating.")

class ReviewPopup:
    def __init__(self, root, db, biz_id, biz_name, userEmail):
        self.root = root
        self.db = db
        self.biz_id = biz_id
        self.userEmail = userEmail

        self.popup = tk.Toplevel(self.root)
        self.popup.title(f"Review {biz_name}")
        self.popup.geometry("800x500")
        self.popup.configure(bg="#DAA520")
        self.popup.grab_set()

        tk.Label(self.popup, text=f"Write a review for {biz_name}",
                 font=("Georgia", 16, "bold"), bg="#DAA520").pack(pady=15)

        self.reviewBox = tk.Text(self.popup, height=10, font=("Georgia", 11), wrap="word")
        self.reviewBox.pack(padx=20, pady=10, fill="both", expand=True)

        def submitReview():
            reviewInputText = self.reviewBox.get("1.0", "end").strip()
            if not reviewInputText:
                return
            self.db.saveReview(self.userEmail, biz_id, reviewInputText)
            self.popup.destroy()

        tk.Button(self.popup, text="Submit Review", bg="#2D5A27", fg="white",
                  font=("Georgia", 12), relief="flat", command=submitReview).pack(pady=15)