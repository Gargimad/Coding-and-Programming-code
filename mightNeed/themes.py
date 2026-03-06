'''
Theme management for Pibbit
'''
class Themes:
    def __init__(self):
        self.darkMode = False
        self.lightColors = {
            "bg": "#DAA520",
            "nav": "#DAA520",
            "card": "#DDE0D6",
            "card_text": "black",
            "accent": "#2D5A27",
            "accent_text": "white",
            "text": "black",
            "footer": "#2D5A27",
            "button": "#2D5A27",
            "button_text": "white",
            "highlight": "#6B8E23",
            "bookmark_added": "#E1AD01",
            "bookmark_remove": "#A2D98E",
            "rating_stars": "#E1AD01"
        }

        self.darkColors = {
            "bg": "#1E1E1E",
            "nav": "#2B2B2B",
            "card": "#333333",
            "card_text": "#FFFFFF",
            "accent": "#3D7A35",
            "accent_text": "#FFFFFF",
            "text": "#FFFFFF",
            "footer": "#111111",
            "button": "#3D7A35",
            "button_text": "#FFFFFF",
            "highlight": "#4A7023",
            "bookmark_added": "#B8860B",
            "bookmark_remove": "#2D5A27",
            "rating_stars": "#FFD700"
        }
    
    def toggle(self):
        self.darkMode = not self.darkMode
        return self.get_colors()
    
    def get_colors(self):
        return self.darkColors if self.darkMode else self.lightColors