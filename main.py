'''
Gargi Madala, Grace Wu, Dhanvi Ramkumar
Pibbit Main
FBLA- Coding and Programming
26 January 2026
'''
import tkinter as tk
from startScreen import StartScreen
from db import Database

def main():
    root = tk.Tk()
    StartScreen(root, userEmail="")
    root.mainloop()

if (__name__ == "__main__"):
    main()