'''
Utility functions
'''
import webbrowser

def open_website(url, update_callback=None):
    """Open website in browser"""
    if update_callback:
        update_callback(f"Opening browser to visit {url}...")
    try:
        webbrowser.open(url, new=2)
    except Exception as e:
        print(f"Error: {e}")

def format_rating(rating):
    """Convert rating to star format"""
    rateValue = float(rating) if rating else 0.0
    return "★" * int(rateValue) + "☆" * (5 - int(rateValue))