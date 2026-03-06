'''
Business display and sorting logic
'''
import tkinter as tk
from guiElements import BusinessCard, ScrollableFrame

class BusinessDisplay:
    def __init__(self, parent, db, userEmail, theme_manager, callbacks):
        self.parent = parent
        self.db = db
        self.userEmail = userEmail
        self.theme = theme_manager
        self.callbacks = callbacks
        self.current_businesses = []
    
    def show(self, sub_id, sub_name, city_id):
        colors = self.theme.get_colors()
        self.parent.place_forget() if hasattr(self.parent, 'place_forget') else None
        
        # Clear container
        for widget in self.callbacks['container'].winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        scroll_frame = ScrollableFrame(self.callbacks['container'], colors)
        scroll_frame.pack()
        
        # Add header and sorting
        self._add_header(scroll_frame.scrollable_frame, sub_id, sub_name, colors)
        
        # Fetch businesses
        self.current_businesses = self._fetch_businesses(sub_id, city_id)
        
        # Display cards
        self._display_cards(scroll_frame.scrollable_frame)
    
    def _fetch_businesses(self, sub_id, city_id):
        if sub_id == 1:
            return self.db.fetchAllBusinesses()
        elif sub_id == -1:
            return self.db.fetchBookmarkedBusinesses(self.userEmail)
        elif sub_id == 0 and city_id != 0:
            return self.db.fetchBusinessByCity(city_id)
        else:
            return self.db.fetchBusinessesBySubs(sub_id)
    
    def _display_cards(self, parent):
        colors = self.theme.get_colors()
        cards_frame = tk.Frame(parent, bg=colors["bg"])
        cards_frame.pack(fill="both", expand=True)
        
        if not self.current_businesses:
            tk.Label(cards_frame, text="No businesses found.", 
                    bg=colors["bg"], fg=colors["text"], 
                    font=("Georgia", 12)).pack(pady=20)
            return
        
        for biz in self.current_businesses:
            if any(field is None for field in [biz[1], biz[4], biz[5]]):
                continue
            
            card_callbacks = {
                'open_website': self.callbacks['open_website'],
                'rate': lambda b_id=biz[0], name=biz[1]: self.callbacks['rate_business'](b_id, name),
                'review': lambda b_id=biz[0], name=biz[1]: self.callbacks['write_review'](b_id, name),
                'bookmark': lambda b_id=biz[0]: self.callbacks['toggle_bookmark'](b_id)
            }
            
            BusinessCard(cards_frame, biz, colors, card_callbacks)