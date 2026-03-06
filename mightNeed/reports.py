'''
PDF Report Generation
'''
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import tempfile
import os
from tkinter import messagebox

class ReportGenerator:
    @staticmethod
    def generate(businesses, category_name, update_callback):
        update_callback("Preparing PDF report... Please wait.")
        
        filtered = [b for b in businesses if b[1] and b[1] != "None"]
        if not filtered:
            messagebox.showwarning("Print Error", "No valid businesses available to print.")
            return
        
        temp_dir = tempfile.gettempdir()
        filename = os.path.join(temp_dir, f"{category_name}_Report.pdf")
        
        try:
            c = canvas.Canvas(filename, pagesize=letter)
            width, height = letter
            y = height - 1*inch
            
            # Header
            c.setFont("Helvetica-Bold", 20)
            c.drawString(1*inch, y, "PIBBIT Business Report")
            y -= 0.3*inch
            c.setFont("Helvetica", 12)
            c.drawString(1*inch, y, f"Category: {category_name}")
            y -= 0.5*inch
            c.line(1*inch, y + 0.1*inch, 7.5*inch, y + 0.1*inch)
            
            for biz in filtered:
                if y < 1.5*inch:
                    c.showPage()
                    y = height - 1*inch
                
                _, name, rating, reviews, desc, link = biz
                
                c.setFont("Helvetica-Bold", 14)
                c.drawString(1*inch, y, str(name))
                y -= 0.2*inch
                
                c.setFont("Helvetica", 10)
                c.drawString(1*inch, y, f"Rating: {rating or 0} | Reviews: {reviews or 0}")
                y -= 0.2*inch
                
                c.setFont("Helvetica-Oblique", 10)
                desc = str(desc)
                if len(desc) > 90: desc = desc[:87] + "..."
                c.drawString(1*inch, y, desc)
                y -= 0.2*inch
                
                c.setFont("Helvetica", 10)
                c.setFillColorRGB(0, 0, 1)
                c.drawString(1*inch, y, f"Website: {link}")
                c.setFillColorRGB(0, 0, 0)
                y -= 0.4*inch
            
            c.save()
            os.startfile(filename)
            update_callback("Report generated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate PDF: {e}")