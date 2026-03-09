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

    def refresh_captcha(self):
        #'Refresh code' to refresh the captcha 6-letter characters
        self.genNewCaptcha()
        #Adding spaces
        display_text = " ".join(self.captchaCont)
        self.captcha_label.config(text=display_text)

    def signupUi(self):
        frame = tk.Frame(self.root, bg=BG, padx=50, pady=50)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Create Account", font=("Georgia", 36, "bold"), fg=TEXT, bg=BG).pack(pady=(0, 30))

        form = tk.Frame(frame, bg=BG)
        form.pack()

        # --- Email Field ---
        tk.Label(form, text="Email", bg=BG, fg=TEXT, font=("Georgia", 14)).pack(anchor="w")
        self.emailEntry = tk.Entry(form, width=35, relief="solid", bd=1)
        self.emailEntry.pack(pady=(0, 15))
        tk.Label(form, text="Use format: example@domain.com", bg=BG, fg=ACCENT, font=("Georgia", 9, "italic")).pack(anchor="w", pady=(0, 15))

        # --- Password Fields ---
        tk.Label(form, bg=BG, text="Password", fg=TEXT, font=("Georgia", 14)).pack(anchor="w")
        self.passwordEntry = tk.Entry(form, width=35, show="*", relief="solid", bd=1)
        self.passwordEntry.pack(pady=(0, 10))
        tk.Label(form, text="Min. 8 characters (Must include a number & special character)", bg=BG, fg=ACCENT, font=("Georgia", 8, "italic"), wraplength=250).pack(anchor="w", pady=(0, 15))
        
        tk.Label(form, bg=BG, text="Confirm Password", fg=TEXT, font=("Georgia", 14)).pack(anchor="w")
        self.confirmPasswordEntry = tk.Entry(form, width=35, show="*", relief="solid", bd=1)
        self.confirmPasswordEntry.pack(pady=(0, 20))

        # --- Enhanced CAPTCHA Section ---
        captcha_frame = tk.Frame(frame, bg=BG) #Holds the 
        captcha_frame.pack(pady=10)

        tk.Label(captcha_frame, text="Enter the characters below:", bg=BG, fg=TEXT, font=("Georgia", 10)).pack()
        
        # Displaying CAPTCHA with wide spacing and distinct background
        self.captcha_label = tk.Label(captcha_frame, 
                                     text=" ".join(self.captchaCont), 
                                     bg="#f0f0f0", 
                                     fg=ACCENT, 
                                     font=("Courier", 20, "bold italic"),
                                     padx=10)
        self.captcha_label.pack(pady=5)
        # Small Refresh Button
        tk.Button(captcha_frame, text="Refresh Code", font=("Georgia", 8), command=self.refresh_captcha, bd=0, fg=PRIMARY, bg=BG, cursor="hand2").pack()

        self.captchaEntry = tk.Entry(frame, width=15, relief="solid", bd=1, justify="center", font=("Arial", 12))
        self.captchaEntry.pack(pady=5)

        # --- Buttons ---
        tk.Button(frame, text="Create Account", bg=PRIMARY, fg="white", font=("Georgia", 14, "bold"), width=25, bd=0, pady=8, cursor="hand2", command=self.createAccount).pack(pady=25)
        tk.Button(frame, text="Use Existing Account", bg=BG, fg=PRIMARY, font=("Georgia", 14, "bold"), width=25, bd=2, relief="solid", cursor="hand2", command=self.openLogin).pack(pady=(10,0))
        tk.Button(frame, text="Back to Guest", bg=BG, fg=PRIMARY, font=("Georgia", 14, "bold"), width=25, bd=2, relief="solid", cursor="hand2", command=self.backToGuest).pack(pady=(10,0))

    def send_verification_email(self, receiver_email, code):
        """Sends a 6-digit code to the user's email."""
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
        user_email = self.emailEntry.get().strip()
        password = self.passwordEntry.get().strip()
        confirmPassword = self.confirmPasswordEntry.get().strip()
        
        # Capture character-based CAPTCHA and normalize to uppercase
        captcha_input = self.captchaEntry.get().strip().upper()
        
        emailPatt = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        passwordPatt = r"^(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})"
        
        # Validation checks
        if password != confirmPassword:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if not user_email or not re.match(emailPatt, user_email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        if not re.match(passwordPatt, password):
            messagebox.showerror("Weak Password", "Password must be at least 8 characters long and include a number/special character.")
            return
            
        # Verify String CAPTCHA
        if captcha_input != self.captchaCont:
            messagebox.showerror("Error", "CAPTCHA verification failed. Please try again.")
            self.refresh_captcha() #Force a new code on failure
            return

        # Generate and Send OTP
        verification_code = str(secrets.randbelow(900000) + 100000)
        
        if self.send_verification_email(user_email, verification_code):
            user_input = simpledialog.askstring("Verify Email", f"Code sent to {user_email}:")
            
            if user_input == verification_code:
                if self.db.addUser(user_email, password):
                    messagebox.showinfo("Success", "Account verified and created!")
                    self.openApp(user_email)
                else:
                    messagebox.showerror("Error", "Account already exists.")
            else:
                messagebox.showerror("Error", "Invalid verification code.")
        else:
            messagebox.showerror("Error", "Failed to send email. Check SMTP settings.")

    def openApp(self, user_email):
        from startScreen import StartScreen
        self.root.destroy()
        new_root = tk.Tk()
        StartScreen(new_root, userEmail=user_email)
        new_root.mainloop()

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