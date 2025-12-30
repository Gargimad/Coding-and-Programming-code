import tkinter as tk
from tkinter import messagebox
from db import Database
import random
from dashboardPage import DashboardPage
class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("PIBBIT - Login")
        self.root.state("zoomed")
        self.db = Database()
        self.a = random.randint(1, 9)
        self.b = random.randint(1, 9)

        self.createUi()

    def createUi(self):
        self.frame = tk.Frame(self.root, padx=40, pady=40)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.frame, text="Login", font=("Georgia", 32)).pack(pady=10)
        
        input_container = tk.Frame(self.frame)
        input_container.pack(pady=10)
        
        tk.Label(input_container, text="Email:", font=("Georgia", 16)).grid(row=0, column=0, sticky="e", padx=5)
        self.emailEntry = tk.Entry(input_container, width=30)
        self.emailEntry.grid(row=0, column=1, pady=5)
        tk.Label(input_container, text="Password:", font=("Georgia", 16)).grid(row=1, column=0, sticky="e", padx=5)
        self.passwordEntry = tk.Entry(input_container, width=30, show="*")
        self.passwordEntry.grid(row = 1, column = 1, pady=5)

        tk.Label(
            self.frame,
            text=f"I am not a robot: {self.a} + {self.b} = ?"
        ).pack(pady=10)

        self.captchaEntry = tk.Entry(self.frame, width=10)
        self.captchaEntry.pack()

        tk.Button(
            self.frame,
            text="Login",
            command=self.loginUser,
            cursor = "hand2"
        ).pack(pady=20)

    def loginUser(self):
        email = self.emailEntry.get().strip()
        password = self.passwordEntry.get().strip()
        answer = self.captchaEntry.get().strip()

        if not answer.isdigit() or int(answer) != self.a + self.b:
            messagebox.showerror("Error", "Human verification failed.")
            return

        if self.db.userExists(email, password):
            messagebox.showinfo("Success", "Login successful!")
            self.login_success(email)
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def login_success(self, email):
        # Destroy ONLY the login container
        self.frame.destroy()
        
        # Load the next screen
        self.dashboardPage = DashboardPage(self.root, email)