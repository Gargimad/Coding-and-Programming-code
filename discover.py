import tkinter as tk
from tkinter import ttk

class DiscoverPage:
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        
        # Sample Business Data
        self.businesses = [
            {"name": "The Green Bean", "cat": "Cafe", "rate": "4.8", "dist": "0.5 miles"},
            {"name": "Tech Repair Hub", "cat": "IT Services", "rate": "4.5", "dist": "1.2 miles"},
            {"name": "Iron Gym", "cat": "Fitness", "rate": "4.9", "dist": "2.0 miles"},
            {"name": "Artisanal Bakes", "cat": "Bakery", "rate": "4.7", "dist": "0.8 miles"},
            {"name": "Sparkle Cleaners", "cat": "Laundry", "rate": "4.2", "dist": "3.1 miles"},
            {"name": "Pet Paradise", "cat": "Pet Shop", "rate": "4.6", "dist": "1.5 miles"},
            {"name": "Solaris Yoga", "cat": "Wellness", "rate": "4.9", "dist": "1.1 miles"},
            {"name": "Byte Bistro", "cat": "Restaurant", "rate": "4.4", "dist": "0.3 miles"}
        ]

    def draw(self):
        """Main method to draw the Discover page onto the parent container"""
        # 1. Page Title
        tk.Label(self.parent, text="Explore Businesses", 
                 font=("Georgia", 26, "bold"), bg=self.colors['bg'], 
                 fg=self.colors['darkText']).pack(anchor="w", padx=45, pady=(20, 10))

        # 2. Scrollable Area Setup
        # We use a Canvas + Scrollbar to allow a long list of businesses
        container = tk.Frame(self.parent, bg=self.colors['bg'])
        container.pack(fill="both", expand=True, padx=45, pady=10)

        canvas = tk.Canvas(container, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        # This frame holds the actual business cards
        self.scrollable_content = tk.Frame(canvas, bg=self.colors['bg'])

        # Update the scrollable area size whenever the content changes
        self.scrollable_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 3. Create Cards
        # Loop through data (doubled to demonstrate scrolling)
        for biz in self.businesses * 2:
            self.create_business_card(biz)

    def create_business_card(self, biz):
        """Creates an individual business listing row"""
        card = tk.Frame(self.scrollable_content, bg="white", 
                        highlightbackground=self.colors['navBg'], 
                        highlightthickness=1, padx=20, pady=15)
        card.pack(fill="x", pady=8, padx=5)

        # Left side: Text Details
        info_frame = tk.Frame(card, bg="white")
        info_frame.pack(side="left")

        tk.Label(info_frame, text=biz['name'], font=("Arial", 15, "bold"), 
                 bg="white", fg=self.colors['darkText']).pack(anchor="w")
        
        subtext = f"{biz['cat']}  •  ⭐ {biz['rate']}  •  📍 {biz['dist']}"
        tk.Label(info_frame, text=subtext, font=("Arial", 11), 
                 bg="white", fg="#787276").pack(anchor="w", pady=(2, 0))

        # Right side: Action Button
        btn_view = tk.Button(card, text="View Details", font=("Arial", 10, "bold"),
                             bg=self.colors['sidebar'], fg="white", relief="flat",
                             padx=15, pady=8, cursor="hand2",
                             command=lambda n=biz['name']: print(f"Opening {n}"))
        btn_view.pack(side="right")

# --- TO INTEGRATE THIS INTO YOUR MAIN SCRIPT ---
# inside your navigate_to("Discover") function:
# 
# page = DiscoverPage(self.mainContainer, self.colors)
# page.draw()