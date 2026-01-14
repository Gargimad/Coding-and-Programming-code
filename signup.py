import tkinter as tk
from tkinter import messagebox
from db import Database
import random

BG = "#ffffff"
PRIMARY = "#e29578"
ACCENT = "#C48B42"
TEXT = "#626A52"

class SignUp:
    def __init__(self, root):
        self.root = root
        self.root.title("PIBBIT - Sign Up")
        self.root.state("zoomed")
        self.root.configure(bg=BG)

        self.db = Database()
        self.a = random.randint(1, 9)
        self.b = random.randint(1, 9)

        self.createUi()

    def createUi(self):
        frame = tk.Frame(self.root, bg=BG, padx=50, pady=50)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            frame, text="Create Account",
            font=("Georgia", 36, "bold"),
            fg=TEXT, bg=BG
        ).pack(pady=(0, 30))

        form = tk.Frame(frame, bg=BG)
        form.pack()

        tk.Label(form, text="Email", bg=BG, fg=TEXT, font=("Georgia", 14)).pack(anchor="w")
        self.emailEntry = tk.Entry(form, width=35, relief="solid", bd=1)
        self.emailEntry.pack(pady=(0, 15))

        tk.Label(form, text="Password", bg=BG, fg=TEXT, font=("Georgia", 14)).pack(anchor="w")
        self.passwordEntry = tk.Entry(form, width=35, show="*", relief="solid", bd=1)
        self.passwordEntry.pack(pady=(0, 20))

        tk.Label(
            frame,
            text=f"I am not a robot: {self.a} + {self.b} = ?",
            bg=BG, fg=TEXT
        ).pack()

        self.captchaEntry = tk.Entry(frame, width=10, relief="solid", bd=1)
        self.captchaEntry.pack(pady=10)

        tk.Button(
            frame,
            text="Create Account",
            bg=PRIMARY,
            fg="white",
            font=("Georgia", 14, "bold"),
            width=25,
            bd=0,
            pady=8,
            cursor="hand2",
            command=self.createAccount
        ).pack(pady=25)

    def createAccount(self):
        email = self.emailEntry.get().strip()
        password = self.passwordEntry.get().strip()
        answer = self.captchaEntry.get().strip()

        if not answer.isdigit() or int(answer) != self.a + self.b:
            messagebox.showerror("Error", "Human verification failed.")
            return

        if self.db.addUser(email, password):
            messagebox.showinfo("Success", "Account created!")
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Account already exists.")