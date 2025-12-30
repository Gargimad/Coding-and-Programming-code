import tkinter as tk
from tkinter import messagebox
from db import Database
import random

class SignUp:
    def __init__(self, root):
        self.root = root
        self.root.title("PIBBIT - Sign Up")
        self.root.state("zoomed")
        self.db = Database()

        self.a = random.randint(1, 9)
        self.b = random.randint(1, 9)

        self.createUi()

    def createUi(self):
        frame = tk.Frame(self.root, padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Sign Up", font=("Arial", 32)).pack(pady=10)

        input_container = tk.Frame(frame)
        input_container.pack(pady=10)
        
        tk.Label(input_container, text="Email:", font=("Arial", 16)).grid(row=0, column=0, sticky="e", padx=5)
        self.emailEntry = tk.Entry(input_container, width=30)
        self.emailEntry.grid(row=0, column=1, pady=5)
        tk.Label(input_container, text="Password:", font=("Arial", 16)).grid(row=1, column=0, sticky="e", padx=5)
        self.passwordEntry = tk.Entry(input_container, width=30, show="*")
        self.passwordEntry.grid(row = 1, column = 1, pady=5)

        tk.Label(
            frame,
            text=f"I am not a robot: {self.a} + {self.b} = ?"
        ).pack(pady=10)

        self.captchaEntry = tk.Entry(frame, width=10)
        self.captchaEntry.pack()

        tk.Button(
            frame,
            text="Create Account",
            command=self.createAccount
        ).pack(pady=20)

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