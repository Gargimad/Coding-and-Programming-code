import tkinter as tk
from tkinter import messagebox
from db import Database
import random
from startScreen import StartScreen

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
        self.a = random.randint(1, 9)
        self.b = random.randint(1, 9)

        self.createUi()

    def createUi(self):
        self.frame = tk.Frame(self.root, bg=BG, padx=50, pady=50)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            self.frame, text="Log In",
            font=("Georgia", 36, "bold"),
            fg=TEXT, bg=BG
        ).pack(pady=(0, 30))

        form = tk.Frame(self.frame, bg=BG)
        form.pack()

        tk.Label(form, text="Email", bg=BG, fg=TEXT, font=("Georgia", 14)).pack(anchor="w")
        self.emailEntry = tk.Entry(form, width=35, relief="solid", bd=1)
        self.emailEntry.pack(pady=(0, 15))

        tk.Label(form, text="Password", bg=BG, fg=TEXT, font=("Georgia", 14)).pack(anchor="w")
        self.passwordEntry = tk.Entry(form, width=35, show="*", relief="solid", bd=1)
        self.passwordEntry.pack(pady=(0, 20))

        tk.Label(
            self.frame,
            text=f"I am not a robot: {self.a} + {self.b} = ?",
            bg=BG, fg=TEXT
        ).pack()

        self.captchaEntry = tk.Entry(self.frame, width=10, relief="solid", bd=1)
        self.captchaEntry.pack(pady=10)

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
    def openSignUp(self):
        self.root.destroy()
        from signup import SignUp
        root = tk.Tk()
        SignUp(root)
        root.mainloop()

    def loginUser(self):
        email = self.emailEntry.get().strip()
        password = self.passwordEntry.get().strip()
        answer = self.captchaEntry.get().strip()

        if not answer.isdigit() or int(answer) != self.a + self.b:
            messagebox.showerror("Error", "Human verification failed.")
            return

        if self.db.userExists(email, password):
            self.frame.destroy()
            StartScreen(self.root, email)
        else:
            messagebox.showerror("Error", "Invalid credentials.")