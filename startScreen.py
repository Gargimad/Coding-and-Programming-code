import tkinter as tk
from PIL import Image, ImageTk

class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("PIBBIT")
        self.root.state("zoomed")
        self.root.configure(bg="#f5f4ee")
        self.createUi()
    def createUi(self):
        cardFrame = tk.Frame(self.root, bg="#fdfcf6", padx=50, pady=50)
        cardFrame.place(relx=0.5, rely=0.5, anchor="center")

        img = Image.open(r"C:\Gargi Madala\python\Coding and Programming SLC Project\logo.png").resize((300, 180))
        self.logoPhoto = ImageTk.PhotoImage(img)

        tk.Label(cardFrame, image=self.logoPhoto, bg="#fdfcf6").pack(pady=10)

        tk.Label(
            cardFrame,
            text="PIBBIT",
            font=("Georgia", 28, "bold"),
            fg="#626A52",
            bg="#fdfcf6"
        ).pack(pady=20)

        self.createButton(cardFrame, "Sign Up", "#C48B42", self.openSignUp)
        self.createButton(cardFrame, "Login", "#C48B42", self.openLogin)
        self.createButton(cardFrame, "Guest", "#e29578", self.openGuest)

    def createButton(self, parent, text, color, command):
        tk.Button(
            parent, text=text,
            font=("Georgia", 12, "bold"),
            bg=color, fg="white",
            width=18, pady=8,
            bd=0, command=command,
            cursor = "hand2"
        ).pack(pady=8)

    def openSignUp(self):
        self.root.destroy()
        from signup import SignUp
        root = tk.Tk()
        SignUp(root)
        root.mainloop()

    def openLogin(self):
        self.root.destroy()
        from login import Login
        root = tk.Tk()
        Login(root)
        root.mainloop()

    def openGuest(self):
        self.root.destroy()
        root = tk.Tk()
        root.title("PIBBIT - Guest")
        root.state("zoomed")
        tk.Label(
            root,
            text="Guest Mode (Limited Access)",
            font=("Helvetica", 24)
        ).pack(expand=True)
