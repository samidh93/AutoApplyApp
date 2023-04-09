from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import docx
#from docx2pdf import convert

class Resume:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = self.extract_text()
        
    def extract_text(self):
        with open(self.file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            page_count = len(pdf_reader.pages) 
            text = ''
            for i in range(page_count):
                page = pdf_reader.pages[i]
                text += page.extract_text()
        return text
    @staticmethod
    def saveContentToPdf( input_text, output_pdf):
        # Create a new PDF file
        pdf_file = canvas.Canvas(output_pdf)
        # Write text to the PDF file
        pdf_file.drawString(100, 750, input_text)
        # Save and close the PDF file
        pdf_file.save()
        return pdf_file

    @staticmethod
    def saveContentToDocx( input_text, output_docx, output_pdf=None):

        # Create a new Word document
        document = docx.Document()

        # Add some text to the document
        document.add_paragraph(input_text)

        # Save the document
        document.save(output_docx)

        if output_pdf is not None:
            # Convert a Word document to PDF
            #convert(output_pdf)
            pass
            
if __name__ == '__main__':
    resume = Resume('jobApp/data/resume.pdf')
    text = resume.text
    print(text)
    pdf = Resume.saveContentToPdf('hello there','jobApp/data/new_resume.pdf' )
    doc = Resume.saveContentToDocx(text, 'jobApp/data/resume.docx')
    