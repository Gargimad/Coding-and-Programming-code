'''
Gargi Madala, Grace Wu, Dhanvi Ramkumar
Pibbit Login
FBLA- Coding and Programming
26 January 2026
'''
import tkinter as tk
from tkinter import messagebox
from db import Database
import random
from startScreen import StartScreen
import re

# Define colors
BG = "#ffffff"
PRIMARY = "#e29578"
ACCENT = "#C48B42"
TEXT = "#626A52"

class Login:
    def __init__(self, root):
        # Initialize the login window
        self.root = root
        self.root.title("PIBBIT - Login")
        self.root.state("zoomed")
        self.root.configure(bg=BG)

        # Define user credentials validation
        self.db = Database()

        # random numbers for simple captcha
        self.a = random.randint(1, 9)
        self.b = random.randint(1, 9)

        #build the UI
        self.loginUi()

    def loginUi(self):
        # Create the login UI
        self.frame = tk.Frame(self.root, bg=BG, padx=50, pady=50)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(
            self.frame, text="Log In",
            font=("Georgia", 36, "bold"),
            fg=TEXT, bg=BG
        ).pack(pady=(0, 30))

        #form frame to group input fields
        form = tk.Frame(self.frame, bg=BG)
        form.pack()

        # Email and Password fields
        tk.Label(form, text="Email", bg=BG, fg=TEXT, font=("Georgia", 14)).pack(anchor="w")
        self.emailEntry = tk.Entry(form, width=35, relief="solid", bd=1)
        self.emailEntry.pack(pady=(0, 15))

        tk.Label(form, text="Password", bg=BG, fg=TEXT, font=("Georgia", 14)).pack(anchor="w")
        self.passwordEntry = tk.Entry(form, width=35, show="*", relief="solid", bd=1)
        self.passwordEntry.pack(pady=(0, 20))

        # simple math captcha for human verification
        tk.Label(
            self.frame,
            text=f"I am not a robot: {self.a} + {self.b} = ?",
            bg=BG, fg=TEXT
        ).pack()

        self.captchaEntry = tk.Entry(self.frame, width=10, relief="solid", bd=1)
        self.captchaEntry.pack(pady=10)

        # Login Button
        tk.Button(
            self.frame,
            text="Next",
            bg=PRIMARY,
            fg="white",
            font=("Georgia", 14, "bold"),
            width=25,
            bd=0,
            pady=8,
            cursor="hand2",
            command=self.loginUser
        ).pack(pady=25)

        tk.Label(self.frame, text="OR", bg=BG, fg=TEXT).pack(pady=10)

        # Sign Up Button
        tk.Button(
            self.frame,
            text="Create an account",
            bg=BG,
            fg=PRIMARY,
            font=("Georgia", 14, "bold"),
            width=25,
            bd=2,
            relief="solid",
            cursor="hand2",
            command=self.openSignUp
        ).pack()
        tk.Button(
            self.frame,
            text="Back to Guest",
            bg=BG,
            fg=PRIMARY,
            font=("Georgia", 14, "bold"),
            width=25,
            bd=2,
            relief="solid",
            cursor="hand2",
            command=self.backToGuest
        ).pack(pady = (10,0))
    def backToGuest(self):
        # Open the Sign Up window
        self.root.destroy()
        from startScreen import StartScreen
        root = tk.Tk()
        StartScreen(root, userEmail="")
        root.mainloop()
    def openSignUp(self):
        # Open the Sign Up window
        self.root.destroy()
        from signup import SignUp
        root = tk.Tk()
        SignUp(root)
        root.mainloop()

    def loginUser(self):
        # Validate user credentials and login
        email = self.emailEntry.get().strip()
        password = self.passwordEntry.get().strip()
        answer = self.captchaEntry.get().strip()
        emailPatt = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' #Email pattern

        # Validate captcha credentials using database
        if not email:
            messagebox.showerror("Error", "Email field cannot be empty.")
            return
            
        if not re.match(emailPatt, email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        if not answer.isdigit() or int(answer) != self.a + self.b:
            messagebox.showerror("Error", "Human verification failed.")
            return

        if self.db.userExists(email, password):
            self.frame.destroy()
            StartScreen(self.root, email)
        else:
            messagebox.showerror("Error", "Invalid credentials.")