import tkinter as tk
from tkinter import messagebox, ttk
import random
from discover import DiscoverPage

class DashboardPage:
    def __init__(self, root, userEmail):
        self.root = root
        self.root.title("PIBBIT - Dashboard")
        self.root.state("zoomed")
        
        # 1. Personalize name from email
        self.username = userEmail.split('@')[0].capitalize()
        
        # 2. Styling Hexcodes
        self.colors = {
            'bg': '#F1F3E9',
            'sidebar': '#A2D98E',
            'navBg': '#DCDCD3',
            'card': '#E89076',
            'cardHover': '#cf7b63',
            'searchFill': '#ffffff',
            'searchBtn': '#A2D98E',
            'darkText': '#1A1A1A'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # --- LOGO LOADING ---
        try:
            self.logoImg = tk.PhotoImage(file=r"C:\Gargi Madala\python\Coding and Programming SLC Project\logo.png").subsample(2, 2)
        except:
            self.logoImg = None 

        # --- LAYOUT CONTAINERS ---
        # Sidebar (Green bar on the left)
        self.sidebar = tk.Frame(self.root, bg=self.colors['sidebar'], width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Main Container (Rest of the screen)
        self.mainContainer = tk.Frame(self.root, bg=self.colors['bg'])
        self.mainContainer.pack(side="left", fill="both", expand=True)
        
        # Build UI Components
        self.create_sidebar_content()
        self.create_single_row_header()
        self.create_main_content()

    def create_sidebar_content(self):
        """Navigation items moved to the sidebar"""
        tk.Label(self.sidebar, text="MENU", font=("Georgia", 18, "bold"), 
                 bg=self.colors['sidebar'], fg="#787276").pack(pady=(50, 50),padx=30)

        menuItems = [
            ("🏠 Dashboard", "Dashboard"),
            ("🔍 Discover", "Discover"),
            ("🔖 Bookmarks", "Book"),
            ("🖊 Create", "Create"),
            ("⚙️ Settings", "Settings")
        ]

        for text, ident in menuItems:
            btn = tk.Button(self.sidebar, text=text, font=("Georgia", 14), 
                            bg=self.colors['sidebar'], relief="flat", anchor="w", 
                            padx=30, pady=10, cursor="hand2",
                            command=lambda i=ident: self.navigateTo(i))
            btn.pack(fill="x")
    def navigateTo(self, page_name):
        """Clears the main container and loads a new page"""
        for widget in self.mainContainer.winfo_children():
            widget.destroy()

        self.create_single_row_header()

        if page_name == "Dashboard":
            self.create_main_content()
        elif page_name == "Discover":
            self.create_discover_page()
        else:
            # Placeholder for other pages
            tk.Label(self.mainContainer, text=f"{page_name} Page coming soon!", 
                     font=("Arial", 24), bg=self.colors['bg']).pack(pady=100)

    def create_discover_page(self):
        for widget in self.mainContainer.winfo_children():
            widget.destroy()
        self.discover_view = DiscoverPage(self.mainContainer, self.colors)
        self.discover_view.draw()

    def create_single_row_header(self):
        """Single row header containing Logo, Title, Search, and Profile"""
        header = tk.Frame(self.mainContainer, bg=self.colors['navBg'], height=70)
        header.pack(side="top", fill="x", padx=20, pady=20)
        header.pack_propagate(False)

        # 1. Branding (Logo + Title)
        brand_frame = tk.Frame(header, bg=self.colors['navBg'])
        brand_frame.pack(side="left", padx=15)

        if self.logoImg:
            tk.Label(brand_frame, image=self.logoImg, bg=self.colors['navBg']).pack(side="left")
        
        tk.Label(brand_frame, text="PIBBIT", font=("Georgia", 24, "bold"), 
                 bg=self.colors['navBg'], fg=self.colors['darkText']).pack(side="left", padx=10)

        # 2. Profile Icon (Right side)
        tk.Label(header, text="👤 Profile ✎", font=("Arial", 11), bg=self.colors['navBg'], 
                 cursor="hand2").pack(side="right", padx=20)

        # 3. Search Bar (Center/Fill remaining space)
        search_container = tk.Frame(header, bg=self.colors['navBg'])
        search_container.pack(side="right", padx=20)

        # Lime Search Icon
        tk.Label(search_container, text="🔍", bg=self.colors['searchBtn'], width=4).pack(side="left", ipady=3)
        
        # Search Input
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_container, textvariable=self.search_var, bg=self.colors['searchFill'], 
                                borderwidth=0, font=("Arial", 13), width=35)
        search_entry.pack(side="left", ipady=5)

    def draw_rounded_card(self, canvas, title, value):
        """Draws the smooth pill cards"""
        w, h = 320, 180
        r = 35 
        points = [r, 0, w-r, 0, w, 0, w, r, w, h-r, w, h, w-r, h, r, h, 0, h, 0, h-r, 0, r, 0, 0]
        rect_id = canvas.create_polygon(points, smooth=True, fill=self.colors['card'], outline="")
        
        canvas.create_text(w/2, 45, text=title, fill="white", font=("Arial", 13, "bold"))
        canvas.create_text(w/2, h/2 + 20, text=value, fill="white", font=("Arial", 32, "bold"))

        canvas.tag_bind(rect_id, "<Button-1>", lambda e: messagebox.showinfo("Card", f"Clicked {title}"))
        canvas.tag_bind(rect_id, "<Enter>", lambda e: canvas.itemconfig(rect_id, fill=self.colors['cardHover']))
        canvas.tag_bind(rect_id, "<Leave>", lambda e: canvas.itemconfig(rect_id, fill=self.colors['card']))

    def create_main_content(self):
        """Personalized welcome and card grid"""
        tk.Label(self.mainContainer, text=f"Welcome {self.username}!", 
                 font=("Arial", 26, "bold"), bg=self.colors['bg']).pack(anchor="w", padx=45)

        grid_frame = tk.Frame(self.mainContainer, bg=self.colors['bg'])
        grid_frame.pack(fill="both", expand=True, padx=40)
        grid_frame.columnconfigure((0, 1, 2), weight=1, uniform="equal")

        titles = ["Reviews Written", "Businesses Rated", "Bookmarks", "Coupons Used", "Businesses Visited", "Businesses Created"]
        for i, title in enumerate(titles):
            row, col = i // 3, i % 3
            canv = tk.Canvas(grid_frame, width=320, height=180, bg=self.colors['bg'], 
                             highlightthickness=0, cursor="hand2")
            canv.grid(row=row, column=col, padx=15, pady=15)
            self.draw_rounded_card(canv, title, str(random.randint(1, 100)))