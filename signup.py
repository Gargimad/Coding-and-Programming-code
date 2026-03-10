import tkinter as tk
from tkinter import messagebox, simpledialog
from db import Database
import random
import re 
import smtplib
import ssl
import secrets
import string  #Required for generating random character strings

#Color Schemes
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
        #We used a string based captcha
        self.captchaCont = "" #Captcha content
        self.genNewCaptcha() #Generating new Captcha

        self.signupUi()

    def genNewCaptcha(self):
        #This randomly generates a 6-letter+number string
        captchaChar = string.ascii_uppercase + string.digits #Uppercase letters and numbers
        self.captchaCont = ''.join(random.choice(captchaChar) for _ in range(6)) #Using random library to create random captcha

    def refreshCaptcha(self):
        #'Refresh code' to refresh the captcha 6-letter characters
        self.genNewCaptcha()
        #Adding spaces in the captcha
        displayText = " ".join(self.captchaCont)
        self.capchaText.config(text=displayText)

    def signupUi(self):
        frame = tk.Frame(self.root, bg=BG, padx=50, pady=50)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Create Account", font=("Georgia", 36, "bold"), fg=TEXT, bg=BG).pack(pady=(0, 30))

        form = tk.Frame(frame, bg=BG)
        form.pack()

        #Email entry + Label
        tk.Label(form, text="Email", bg=BG, fg=TEXT, font=("Georgia", 14)).pack(anchor="w")
        self.emailEntry = tk.Entry(form, width=35, relief="solid", bd=1)
        self.emailEntry.pack(pady=(0, 15))
        tk.Label(form, text="Use format: example@domain.com", bg=BG, fg=ACCENT, font=("Georgia", 9, "italic")).pack(anchor="w", pady=(0, 15))

        #Password entry + Label
        tk.Label(form, bg=BG, text="Password", fg=TEXT, font=("Georgia", 14)).pack(anchor="w")
        self.passwordEntry = tk.Entry(form, width=35, show="*", relief="solid", bd=1)
        self.passwordEntry.pack(pady=(0, 10))
        tk.Label(form, text="Min. 8 characters (Must include a number & special character)", bg=BG, fg=ACCENT, font=("Georgia", 8, "italic"), wraplength=250).pack(anchor="w", pady=(0, 15))
        
        tk.Label(form, bg=BG, text="Confirm Password", fg=TEXT, font=("Georgia", 14)).pack(anchor="w")
        self.confirmPasswordEntry = tk.Entry(form, width=35, show="*", relief="solid", bd=1)
        self.confirmPasswordEntry.pack(pady=(0, 20))

        #captcha frame to hold the random letters
        captchaFrame = tk.Frame(frame, bg=BG) #Holds the 
        captchaFrame.pack(pady=10)

        tk.Label(captchaFrame, text="Enter the characters below:", bg=BG, fg=TEXT, font=("Georgia", 10)).pack()
        
        # Displaying CAPTCHA with wide spacing and distinct background
        self.capchaText = tk.Label(captchaFrame, 
                                     text=" ".join(self.captchaCont), 
                                     bg="#f0f0f0", 
                                     fg=ACCENT, 
                                     font=("Courier", 20, "bold italic"),
                                     padx=10)
        self.capchaText.pack(pady=5)
        #Refresh Button
        tk.Button(captchaFrame, text="Refresh Code", font=("Georgia", 8), command=self.refreshCaptcha, bd=0, fg=PRIMARY, bg=BG, cursor="hand2").pack()

        self.captchaEntry = tk.Entry(frame, width=15, relief="solid", bd=1, justify="center", font=("Arial", 12))
        self.captchaEntry.pack(pady=5)

        #Buttons n the frame
        tk.Button(frame, text="Create Account", bg=PRIMARY, fg="white", font=("Georgia", 14, "bold"), width=25, bd=0, pady=8, cursor="hand2", command=self.createAccount).pack(pady=25)
        tk.Button(frame, text="Use Existing Account", bg=BG, fg=PRIMARY, font=("Georgia", 14, "bold"), width=25, bd=2, relief="solid", cursor="hand2", command=self.openLogin).pack(pady=(10,0))
        tk.Button(frame, text="Back to Guest", bg=BG, fg=PRIMARY, font=("Georgia", 14, "bold"), width=25, bd=2, relief="solid", cursor="hand2", command=self.backToGuest).pack(pady=(10,0))

    def sendVerEmail(self, receiver_email, code):
        #Sends a 6-digit code to the user's email.
        sender_email = "gargimadala17@gmail.com" 
        password = "muxz blwu nwon kcuu" # Note: Use environment variables for production!
        pibbitDisplayName = "PIBBIT"
        message = (
                    f"From: {pibbitDisplayName} <{sender_email}>\n"
                    f"To: {receiver_email}\n"
                    f"Subject: PIBBIT Verification Code\n\n"
                    f"Your verification code is: {code}"
                )        
        context = ssl.create_default_context()
        
        try: #SMTP Library - Simple Mail Transfer Protocol to easily send emails to people
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def createAccount(self):
        userEmail = self.emailEntry.get().strip()
        password = self.passwordEntry.get().strip()
        confirmPassword = self.confirmPasswordEntry.get().strip()
        
        #Capturing character-based CAPTCHA and normalize to uppercase
        captchaInput = self.captchaEntry.get().strip().upper()
        
        emailPatt = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        passwordPatt = r"^(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})"
        
        #Validation checks
        if (password != confirmPassword):
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if (not userEmail or not re.match(emailPatt, userEmail)):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        if (not re.match(passwordPatt, password)):
            messagebox.showerror("Weak Password", "Password must be at least 8 characters long and include a number/special character.")
            return
            
        # Verify String CAPTCHA
        if (captchaInput != self.captchaCont):
            messagebox.showerror("Error", "CAPTCHA verification failed. Please try again.")
            self.refreshCaptcha() #Force a new code on failure
            return

        #Generate and Send OTP
        verCode = str(secrets.randbelow(900000) + 100000)
        
        if (self.sendVerEmail(userEmail, verCode)):
            userInput = simpledialog.askstring("Verify Email", f"Code sent to {userEmail}:")
            
            if (userInput == verCode):
                if (self.db.addUser(userEmail, password)):
                    messagebox.showinfo("Success", "Account verified and created!")
                    self.openApp(userEmail)
                else:
                    messagebox.showerror("Error", "Account already exists.")
            else:
                messagebox.showerror("Error", "Invalid verification code.")
        else:
            messagebox.showerror("Error", "Failed to send email. Check SMTP settings.")

    def openApp(self, userEmail):
        from startScreen import StartScreen
        self.root.destroy()
        newRoot = tk.Tk()
        StartScreen(newRoot, userEmail=userEmail)
        newRoot.mainloop()

    def backToGuest(self):
        from startScreen import StartScreen
        self.root.destroy()
        root = tk.Tk()
        StartScreen(root, userEmail="")
        root.mainloop()

    def openLogin(self):
        from login import Login
        self.root.destroy()
        root = tk.Tk()
        Login(root)
        root.mainloop()