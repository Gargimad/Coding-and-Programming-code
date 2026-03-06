'''
Coupon display management
'''
import tkinter as tk

class CouponManager:
    def __init__(self, db, theme_manager):
        self.db = db
        self.theme = theme_manager
    
    def show_business_coupons(self, parent, biz_id, biz_name):
        colors = self.theme.get_colors()
        
        popup = tk.Toplevel(parent)
        popup.title(f"Deals for {biz_name}")
        popup.geometry("500x400")
        popup.configure(bg=colors["card"])
        
        tk.Label(popup, text=f"Coupons for {biz_name}", 
                font=("Georgia", 14, "bold"), 
                bg=colors["card"], fg=colors["card_text"], pady=10).pack()
        
        coupons = self.db.fetchCouponsByBusiness(biz_id)
        
        if not coupons:
            tk.Label(popup, text="No active coupons for this business.", 
                    font=("Georgia", 11), 
                    bg=colors["card"], fg=colors["card_text"]).pack(pady=50)
        else:
            for title, description, coupon_code in coupons:
                self._create_coupon_card(popup, title, description, coupon_code, colors)
    
    def _create_coupon_card(self, parent, title, desc, code, colors):
        f = tk.Frame(parent, bg=colors["bg"] if self.theme.darkMode else "white", 
                    relief="groove", bd=2, padx=10, pady=10)
        f.pack(fill="x", padx=20, pady=5)
        
        tk.Label(f, text=title, font=("Georgia", 12, "bold"), 
                bg=f.cget('bg'), fg=colors["accent"]).pack(anchor="w")
        tk.Label(f, text=desc, font=("Georgia", 10), 
                bg=f.cget('bg'), fg=colors["card_text"], 
                wraplength=400).pack(anchor="w")
        
        tk.Label(f, text=f"CODE: {code}", font=("Courier", 12, "bold"), 
                bg="#F0F0F0", fg="#6E2F20", padx=5).pack(side="left", pady=5)