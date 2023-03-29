from PyPDF2 import PdfReader

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

if __name__ == '__main__':
    resume = Resume('data/resume.pdf')
    text = resume.text
    print(text)