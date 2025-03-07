from fpdf import FPDF
import os

class PDFGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)

    def create_pdf(self, title, content, output_path):
        """Generates a PDF report with the given title and content."""
        self.pdf.add_page()
        self.pdf.set_font("Arial", style='B', size=16)
        self.pdf.cell(200, 10, title, ln=True, align='C')
        self.pdf.ln(10)

        self.pdf.set_font("Arial", size=12)
        self.pdf.multi_cell(0, 10, content)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        self.pdf.output(output_path)
        print(f"📄 PDF generated: {output_path}")