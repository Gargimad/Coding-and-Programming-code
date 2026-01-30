#Imports
import tkinter as tk
from tkinter import messagebox
from db import Database
import random
import re #Used to validate email format

#Color Schemes
BG = "#ffffff" #Background color
PRIMARY = "#e29578" #Primary Color
ACCENT = "#C48B42" #Accent Color
TEXT = "#626A52" #Text Colors
#Class of Signup Page
class SignUp:
    #Innitialization
    def __init__(self, root):
        self.root = root
        self.root.title("PIBBIT - Sign Up")
        self.root.state("zoomed")
        self.root.configure(bg=BG)
        #Connection to database
        self.db = Database()
        self.a = random.randint(1, 9)
        self.b = random.randint(1, 9)

        self.signupUi()

    def signupUi(self):
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
        #Creating button to submit the signup form
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
        #Creating 2 buttons for other pages' navigation: loginpage and guest page
        tk.Button(
            #This first button is for users who already have existing accounts
            frame,
            text="Use Existing Account",
            bg=BG,
            fg=PRIMARY,
            font=("Georgia", 14, "bold"),
            width=25,
            bd=2,
            relief="solid",
            cursor="hand2",
            command=self.openLogin
        ).pack(pady = (10,0))
        tk.Button(
            #This button is for users who want to go back to the first page
            frame,
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
        #Opens the guest page again for users to explore if they desire
        from startScreen import StartScreen #We put the imports inside the functions so python doesn't circulate and get confused
        self.root.destroy()
        root = tk.Tk()
        StartScreen(root, userEmail="")
        root.mainloop()
    def openLogin(self):
        #Opens the login page
        from login import Login #We put the imports inside the functions so python doesn't circulate and get confused
        self.root.destroy()
        root = tk.Tk()
        Login(root)
        root.mainloop()
    #Function that creates an account--------------------------------
    def createAccount(self):
        #Gets email + password that user inputted
        email = self.emailEntry.get().strip()
        password = self.passwordEntry.get().strip()
        #Variable to start the simple captcha entry
        answer = self.captchaEntry.get().strip()
        emailPatt = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not email:
            #When email is left empty
            messagebox.showerror("Error", "Email field cannot be empty.")
            return
            
        if not re.match(emailPatt, email):
            #When email is invalid
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        if not answer.isdigit() or int(answer) != self.a + self.b:
            #When user fails to enter the correct sum
            messagebox.showerror("Error", "Human verification failed.")
            return

        if self.db.addUser(email, password):
            #When account is created
            messagebox.showinfo("Success", "Account created!")
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Account already exists.\n Click 'Use Existing Account' to log in")