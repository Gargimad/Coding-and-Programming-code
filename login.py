'''
Gargi Madala, Grace Wu, Dhanvi Ramkumar
Pibbit Login
FBLA- Coding and Programming
26 January 2026
'''

import tkinter as tk
from tkinter import messagebox
from db import Database
from startScreen import StartScreen
import random
import re
import string

# Define colors
BG = "#ffffff"
PRIMARY = "#e29578"
ACCENT = "#C48B42"
TEXT = "#626A52"

class Login:

    def __init__(self, root):

        self.root = root
        self.root.title("PIBBIT - Login")
        self.root.state("zoomed")
        self.root.configure(bg=BG)

        self.db = Database()

        # Initialize CAPTCHA
        self.captcha_text = ""
        self.generate_new_captcha()

        self.loginUi()

    def generate_new_captcha(self):
        """Generates a random 6-character alphanumeric string."""
        chars = string.ascii_uppercase + string.digits
        self.captcha_text = ''.join(random.choice(chars) for _ in range(6))

    def refresh_captcha(self):
        """Refreshes the CAPTCHA text."""
        self.generate_new_captcha()
        display_text = " ".join(self.captcha_text)
        self.captcha_label.config(text=display_text)

    def loginUi(self):

        self.frame = tk.Frame(self.root, bg=BG, padx=50, pady=50)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            self.frame,
            text="Log In",
            font=("Georgia", 36, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(pady=(0, 30))

        form = tk.Frame(self.frame, bg=BG)
        form.pack()

        # Email
        tk.Label(form, text="Email", bg=BG, fg=TEXT, font=("Georgia", 14)).pack(anchor="w")
        self.emailEntry = tk.Entry(form, width=35, relief="solid", bd=1)
        self.emailEntry.pack(pady=(0, 15))

        tk.Label(
            form,
            text="Use format: example@domain.com",
            bg=BG,
            fg=ACCENT,
            font=("Georgia", 9, "italic")
        ).pack(anchor="w", pady=(0, 15))

        # Password
        tk.Label(form, text="Password", bg=BG, fg=TEXT, font=("Georgia", 14)).pack(anchor="w")
        self.passwordEntry = tk.Entry(form, width=35, show="*", relief="solid", bd=1)
        self.passwordEntry.pack(pady=(0, 20))

        # CAPTCHA Section
        captcha_frame = tk.Frame(self.frame, bg=BG)
        captcha_frame.pack(pady=10)

        tk.Label(
            captcha_frame,
            text="Enter the characters below:",
            bg=BG,
            fg=TEXT,
            font=("Georgia", 10)
        ).pack()

        self.captcha_label = tk.Label(
            captcha_frame,
            text=" ".join(self.captcha_text),
            bg="#f0f0f0",
            fg=ACCENT,
            font=("Courier", 20, "bold italic"),
            padx=10
        )

        self.captcha_label.pack(pady=5)

        tk.Button(
            captcha_frame,
            text="Refresh Code",
            font=("Georgia", 8),
            command=self.refresh_captcha,
            bd=0,
            fg=PRIMARY,
            bg=BG,
            cursor="hand2"
        ).pack()

        self.captchaEntry = tk.Entry(
            self.frame,
            width=15,
            relief="solid",
            bd=1,
            justify="center",
            font=("Arial", 12)
        )

        self.captchaEntry.pack(pady=5)

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
        ).pack(pady=(10,0))

    def loginUser(self):

        email = self.emailEntry.get().strip()
        password = self.passwordEntry.get().strip()
        captcha_input = self.captchaEntry.get().strip().upper()

        emailPatt = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not email:
            messagebox.showerror("Error", "Email field cannot be empty.")
            return

        if not re.match(emailPatt, email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        # CAPTCHA validation
        if captcha_input != self.captcha_text:
            messagebox.showerror("Error", "CAPTCHA verification failed. Please try again.")
            self.refresh_captcha()
            return

        if self.db.userExists(email, password):
            self.frame.destroy()
            StartScreen(self.root, email)
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def openSignUp(self):
        self.root.destroy()
        from signup import SignUp
        root = tk.Tk()
        SignUp(root)
        root.mainloop()

    def backToGuest(self):
        self.root.destroy()
        root = tk.Tk()
        StartScreen(root, userEmail="")
        root.mainloop()