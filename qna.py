import tkinter as tk
from tkinter import ttk

class QnaPage:
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors

        # Sample QnA Questions
        self.qnaData = [
            {"question": "What is this app?", "answer": "This app helps users find and compare local businesses based on ratings and reviews."},
            {"question": "How are businesses ranked?", "answer": "Businesses are ranked by customer ratings provided by the community."},
            {"question": "Where do the ratings come from?", "answer": "Ratings are collected from verified customer reviews within the app."},
            {"question": "Can I visit a business website?", "answer": "Yes! Each business card includes a direct website link button."},
            {"question": "Why do some businesses have fewer stars?", "answer": "Star ratings are based on average customer feedback. Fewer stars indicate lower average scores."}
        ]
    
    def draw(self):
        # Header
        tk.Label(self.parent, text="Q&A Page", 
                 font=("Georgia", 26, "bold"), bg=self.colors['bg'], 
                 fg=self.colors['darkText']).pack(anchor="w", padx=45, pady=(20, 10))

        # Main Container
        container = tk.Frame(self.parent, bg=self.colors['bg'])
        container.pack(fill="both", expand=True, padx=45, pady=10)

        # Scrollbar and Canvas
        canvas = tk.Canvas(container, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        # Content frame inside Canvas
        self.scrollable_content = tk.Frame(canvas, bg=self.colors['bg'])

        self.scrollable_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")
        
        # Keep internal width consistent with canvas
        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Populate cards
        for question in self.qnaData:
            self.qnaCards(question)

    def qnaCards(self, question):
        # Q&A cards design
        qnaCard = tk.Frame(self.scrollable_content, bg="white", 
                            highlightbackground=self.colors['navBg'], 
                            highlightthickness=1, padx=20, pady=15)
        qnaCard.pack(fill="x", pady=8, padx=5)
        
        info_frame = tk.Frame(qnaCard, bg="white")
        info_frame.pack(side="left", fill="x", expand=True)

        # Question Title
        tk.Label(info_frame, text=question['question'], font=("Arial", 15, "bold"), 
                 bg="white", fg=self.colors['darkText']).pack(anchor="w")
        
        # Answer Text with Wraplength to prevent horizontal overflow
        tk.Label(info_frame, text=question['answer'], font=("Arial", 11), 
                 bg="white", fg="#787276", wraplength=900, justify="left").pack(anchor="w", pady=(5, 0))