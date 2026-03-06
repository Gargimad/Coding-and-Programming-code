'''
Reusable UI components for Pibbit
'''
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class BusinessCard:
    """Creates a business card widget"""
    def __init__(self, parent, biz_data, colors, callbacks):
        self.frame = tk.Frame(
            parent,
            bg=colors["card"],
            highlightbackground=colors["highlight"],
            highlightthickness=2,
            padx=15,
            pady=10
        )
        self.frame.pack(fill="x", pady=10, padx=50)
        
        biz_id, biz_name, rating, review_count, description, website_link = biz_data
        
        # Business name
        tk.Label(self.frame, text=biz_name,
                font=("Georgia", 18, "bold"),
                bg=colors["card"],
                fg=colors["card_text"]).pack(anchor="w")
        
        # Rating stars
        rateValue = float(rating) if rating else 0.0
        stars = "★" * int(rateValue) + "☆" * (5 - int(rateValue))
        tk.Label(self.frame, text=f"{stars} {rateValue} ({review_count or 0} reviews)", 
                 font=("Georgia", 12), bg=colors["card"], fg=colors["rating_stars"]).pack(anchor="w")
        
        # Description
        tk.Label(self.frame, text=f"{description}", font=("Georgia", 10), 
                bg=colors["card"], fg=colors["card_text"],
                wraplength=800, justify="left").pack(anchor='w', pady=5)
        
        # Action buttons
        self._create_buttons(colors, callbacks, biz_id, biz_name, website_link)
    
    def _create_buttons(self, colors, callbacks, biz_id, biz_name, website_link):
        actBtnCont = tk.Frame(self.frame, bg=colors["card"])
        actBtnCont.pack(fill="x", side="bottom")
        
        tk.Button(actBtnCont, text="Website Link", bg=colors["button"], fg=colors["button_text"], 
                 relief="flat", padx=10, cursor="hand2",
                 command=lambda: callbacks['open_website'](website_link)).pack(side="right", padx=5)
        
        # Only show these if user is logged in (check if callbacks exist)
        if 'rate' in callbacks:
            tk.Button(actBtnCont, text="Rate Business", bg=colors["button"], fg=colors["button_text"], 
                     relief="flat", padx=10, cursor="hand2",
                     command=lambda: callbacks['rate']()).pack(side="right", padx=(10,0))
        
        if 'review' in callbacks:
            tk.Button(actBtnCont, text="Write a Review", bg=colors["button"], fg=colors["button_text"], 
                     relief="flat", padx=10, cursor="hand2",
                     command=lambda: callbacks['review']()).pack(side="right", padx=(10,0))
        
        if 'coupons' in callbacks:
            tk.Button(actBtnCont, text="View Coupons", bg=colors["button"], fg=colors["button_text"], 
                     relief="flat", padx=10, cursor="hand2",
                     command=lambda: callbacks['coupons']()).pack(side="right", padx=(10,0))
        
        # Bookmark button (top right corner)
        if 'bookmark' in callbacks and callbacks.get('is_bookmarked') is not None:
            bmTxt = "🔖 Bookmarked" if callbacks['is_bookmarked'] else "☆ Bookmark"
            bmColor = colors["bookmark_added"] if callbacks['is_bookmarked'] else colors["bookmark_remove"]
            
            bmBtn = tk.Button(self.frame, text=bmTxt, bg=bmColor, fg=colors["button_text"], 
                             relief="flat", padx=10, cursor="hand2",
                             command=lambda: callbacks['bookmark']())
            bmBtn.place(relx=1.0, rely=0.0, x=-10, y=10, anchor="ne")

class NavBar:
    """Creates the navigation bar"""
    def __init__(self, parent, userEmail, callbacks, theme_manager):
        self.parent = parent
        self.userEmail = userEmail
        self.callbacks = callbacks
        self.theme = theme_manager
        self.buttons = {}
        self.menus = {}
        self.create()
    
    def create(self):
        colors = self.theme.get_colors()
        self.frame = tk.Frame(self.parent, bg=colors["nav"])
        self.frame.pack(side="top", fill="x", padx=20, pady=20)
        
        # Home logo
        self._add_home_button()
        
        # Explore menu
        self._add_explore_menu()
        
        # User-specific buttons
        if not self.userEmail:
            self._add_guest_buttons()
        else:
            self._add_user_buttons()
    
    def _add_home_button(self):
        colors = self.theme.get_colors()
        try:
            homeLogo = Image.open(os.path.join(os.path.dirname(__file__), "homeLogo.png")).resize((50, 50))
            self.homeLogo = ImageTk.PhotoImage(homeLogo)
            btn = tk.Button(self.frame, image=self.homeLogo, bg=colors["nav"], 
                          bd=0, cursor="hand2", command=self.callbacks.get('go_home', lambda: None))
            btn.pack(side="left", padx=(0, 10))
            
            # Hover instruction
            if 'update_instruction' in self.callbacks:
                btn.bind("<Enter>", lambda e: self.callbacks['update_instruction']("Click to return to the main dashboard."))
            
            self.buttons['home'] = btn
        except Exception as e:
            print(f"Could not load home logo: {e}")
            # Fallback text button
            btn = tk.Button(self.frame, text="🏠 Home", bg=colors["button"], fg=colors["button_text"],
                          font=("Georgia", 12), cursor="hand2", command=self.callbacks.get('go_home', lambda: None))
            btn.pack(side="left", padx=(0, 10))
            self.buttons['home'] = btn
    
    def _add_explore_menu(self):
        colors = self.theme.get_colors()
        self.mb = tk.Menubutton(self.frame, text="Explore ⏷", bg=colors["button"], 
                               fg=colors["button_text"], font=("Georgia", 12), 
                               width=20, direction='below', relief='flat', cursor="hand2")
        self.mb.pack(side="left", padx=(0,10))
        
        # Bind click to explore callback
        if 'explore' in self.callbacks:
            self.mb.bind("<Button-1>", lambda e: self.callbacks['explore']())
        
        # Hover instruction
        if 'update_instruction' in self.callbacks:
            self.mb.bind("<Enter>", lambda e: self.callbacks['update_instruction']("Browse businesses by category or location."))
        
        self.buttons['explore'] = self.mb
        
        # Create menu structure
        self._create_category_menus()
    
    def _create_category_menus(self):
        colors = self.theme.get_colors()
        mainMenu = tk.Menu(self.mb, tearoff=0, bg=colors["button"], fg=colors["button_text"], 
                          font=("Georgia", 11), activebackground=colors["accent"])
        self.mb["menu"] = mainMenu
        
        # Get categories from callback
        if 'get_categories' in self.callbacks:
            categories = self.callbacks['get_categories']()
            
            for cat_id, cat_name in categories:
                subCatMenu = tk.Menu(mainMenu, tearoff=0, bg=colors["button"], fg=colors["button_text"])
                
                # Get subcategories
                if 'get_subcategories' in self.callbacks:
                    subcategories = self.callbacks['get_subcategories'](cat_id)
                    for sub_id, sub_name in subcategories:
                        subCatMenu.add_command(
                            label=sub_name,
                            command=lambda sId=sub_id, sName=sub_name: 
                                self.callbacks['show_category'](sId, sName, 0)
                        )
                
                mainMenu.add_cascade(label=cat_name, menu=subCatMenu)
    
    def _add_guest_buttons(self):
        """Add Sign Up and Login buttons for guest users"""
        colors = self.theme.get_colors()
        
        # Sign Up button
        signup_btn = tk.Button(
            self.frame, 
            text="Sign Up", 
            font=("Georgia", 12, "bold"),
            bg=colors["button"], 
            fg=colors["button_text"], 
            width=15, 
            pady=8,
            bd=0, 
            cursor="hand2",
            command=self.callbacks.get('open_signup', lambda: None)
        )
        signup_btn.pack(side="right", padx=10)
        
        # Hover instruction
        if 'update_instruction' in self.callbacks:
            signup_btn.bind("<Enter>", lambda e: self.callbacks['update_instruction'](
                "Join PIBBIT to bookmark businesses and get coupons!"
            ))
        
        self.buttons['signup'] = signup_btn
        
        # Login button
        login_btn = tk.Button(
            self.frame, 
            text="Login", 
            font=("Georgia", 12, "bold"),
            bg=colors["button"], 
            fg=colors["button_text"], 
            width=15, 
            pady=8,
            bd=0, 
            cursor="hand2",
            command=self.callbacks.get('open_login', lambda: None)
        )
        login_btn.pack(side="right", padx=10)
        
        # Hover instruction
        if 'update_instruction' in self.callbacks:
            login_btn.bind("<Enter>", lambda e: self.callbacks['update_instruction'](
                "Log in to access your saved businesses and deals."
            ))
        
        self.buttons['login'] = login_btn
    
    def _add_user_buttons(self):
        """Add buttons for logged-in users"""
        colors = self.theme.get_colors()
        
        # Dark mode toggle button (rightmost)
        self.darkBtn = tk.Button(
            self.frame,
            text="🌙 Dark Mode",
            bg=colors["button"],
            fg=colors["button_text"],
            font=("Georgia", 12),
            width=15,
            relief="flat",
            cursor="hand2",
            command=self.callbacks.get('toggle_dark', lambda: None)
        )
        self.darkBtn.pack(side="right", padx=10)
        
        # Profile button
        self.profileBtn = tk.Menubutton(
            self.frame, 
            text="👤 Profile ✎", 
            font=("Arial", 11),
            bg=colors["nav"], 
            fg=colors["text"],
            relief="flat", 
            cursor="hand2", 
            width=20
        )
        self.profileBtn.pack(side="right")
        
        # Hover instruction
        if 'update_instruction' in self.callbacks:
            self.profileBtn.bind("<Enter>", lambda e: self.callbacks['update_instruction'](
                "Manage your account settings and profile details."
            ))
        
        # Profile menu
        pfpMenuOpts = tk.Menu(
            self.profileBtn, 
            tearoff=0, 
            bg=colors["card"] if self.theme.darkMode else "white", 
            fg=colors["card_text"]
        )
        pfpMenuOpts.add_command(label="Edit Profile", command=self.callbacks.get('edit_profile', lambda: None))
        pfpMenuOpts.add_command(label="Settings", command=self.callbacks.get('settings', lambda: None))
        pfpMenuOpts.add_separator()
        pfpMenuOpts.add_command(label="Logout", command=self.callbacks.get('logout', lambda: None))
        self.profileBtn["menu"] = pfpMenuOpts
        
        self.buttons['profile'] = self.profileBtn
        
        # Coupons and Deals button
        if 'show_coupons' in self.callbacks:
            coupsBtn = tk.Button(
                self.frame, 
                text="Coupons and Deals", 
                bg=colors["button"], 
                fg=colors["button_text"], 
                font=("Georgia", 12), 
                width=20, 
                relief='flat', 
                cursor="hand2",
                command=self.callbacks['show_coupons']
            )
            coupsBtn.pack(side="left", padx=(0,10))
            
            # Hover instruction
            if 'update_instruction' in self.callbacks:
                coupsBtn.bind("<Enter>", lambda e: self.callbacks['update_instruction'](
                    "View exclusive local discounts and promo codes."
                ))
            
            self.buttons['coupons'] = coupsBtn
        
        # Help/Q&A button
        if 'show_help' in self.callbacks:
            helpBtn = tk.Button(
                self.frame, 
                text="Help",
                bg=colors["button"], 
                fg=colors["button_text"], 
                font=("Georgia", 12), 
                width=20, 
                relief='flat', 
                cursor="hand2",
                command=self.callbacks['show_help']
            )
            helpBtn.pack(side="left", padx=(0,10))
            
            # Hover instruction
            if 'update_instruction' in self.callbacks:
                helpBtn.bind("<Enter>", lambda e: self.callbacks['update_instruction'](
                    "Have a question? Visit our interactive Q&A support."
                ))
            
            self.buttons['help'] = helpBtn
        
        # Bookmarks button
        if 'show_bookmarks' in self.callbacks:
            bookmarksBtn = tk.Button(
                self.frame, 
                text="Bookmarks",
                bg=colors["button"], 
                fg=colors["button_text"], 
                font=("Georgia", 12), 
                width=20, 
                relief='flat', 
                cursor="hand2",
                command=self.callbacks['show_bookmarks']
            )
            bookmarksBtn.pack(side="left", padx=(0,10))
            
            # Hover instruction
            if 'update_instruction' in self.callbacks:
                bookmarksBtn.bind("<Enter>", lambda e: self.callbacks['update_instruction'](
                    "View businesses you have saved to your favorites."
                ))
            
            self.buttons['bookmarks'] = bookmarksBtn
    
    def update_theme(self):
        """Update colors when theme changes"""
        colors = self.theme.get_colors()
        self.frame.configure(bg=colors["nav"])
        
        # Update all buttons
        for btn_name, btn in self.buttons.items():
            if btn_name == 'home':
                btn.configure(bg=colors["nav"])
            elif btn_name in ['signup', 'login', 'coupons', 'help', 'bookmarks']:
                btn.configure(bg=colors["button"], fg=colors["button_text"])
            elif btn_name == 'explore':
                btn.configure(bg=colors["button"], fg=colors["button_text"])
            elif btn_name == 'profile':
                btn.configure(bg=colors["nav"], fg=colors["text"])
        
        # Update dark mode button text
        if hasattr(self, 'darkBtn'):
            self.darkBtn.configure(
                text="☀️ Light Mode" if self.theme.darkMode else "🌙 Dark Mode",
                bg=colors["button"], 
                fg=colors["button_text"]
            )
        
        # Update menus
        if hasattr(self, 'mb') and self.mb["menu"]:
            self.mb["menu"].configure(bg=colors["button"], fg=colors["button_text"])

class ScrollableFrame:
    """Creates a scrollable frame container"""
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        self.canvas = tk.Canvas(parent, bg=colors["bg"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=colors["bg"])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.bind('<Configure>', self._on_canvas_configure)
    
    def _on_canvas_configure(self, e):
        self.canvas.itemconfig("all", width=e.width)
    
    def pack(self):
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
    
    def destroy(self):
        """Clean up scrollable frame"""
        self.scrollbar.destroy()
        self.canvas.destroy()