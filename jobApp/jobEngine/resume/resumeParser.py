from PyPDF2 import PdfReader, PdfWriter
#from reportlab.pdfgen import canvas # should be deleted
import pdfplumber
import re

import docx
#from docx2pdf import convert

class Resume:
    def __init__(self, file_path):
        self.file_path = file_path
        ## the section must be defined in higher level apis
        self.sections = ["PROFESSIONAL EXPERIENCE", "EDUCATION", "VOLUNTEER EXPERIENCE", "TRAINING", "ACCOMPLISHMENT", "KEY COMPETENCIES"]
        
    def parse_pdf(self):
        with open(self.file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            page_count = len(pdf_reader.pages) 
            text = ''
            for i in range(page_count):
                page = pdf_reader.pages[i]
                text += page.extract_text()
        return text
    
    def extract_text(self):
        # Parse the PDF file
        #text = str()
        #with pdfplumber.open(self.file_path) as pdf:
        #    for page in pdf.pages:
        #        text = text+ page.extract_text()
        ##print(text)
        #return text
        pass
    
    ###### Sections in resume ###
    # general method
    def extract_section(self, begin_section, end_section, use_regex=False )->str:
        if use_regex:
            # Use regex to find the start and end positions of the  section
            start_regex = re.escape(begin_section) + r"\s*([\w\s,.;:/()-]*)"
            end_regex = re.escape(end_section)
            start_match = re.search(start_regex, self.resume_text)
            if not start_match:
                print("----------------------------------------------------")
                print(f"{begin_section} section not found in resume")
                exit()
            end_match = re.search(end_regex, self.resume_text, start_match.end())
            if not end_match:
                end_pos = len(self.resume_text)
            else:
                end_pos = end_match.start()
            # Extract the text between the start and end positions
            section_text = self.resume_text[start_match.end():end_pos]
            # Print the extracted text
            print("----------------------------------------------------")
            print(f"{begin_section}")
            #print(section_text)    
            return section_text
        
        # Simple string search
        start_pos = self.resume_text.find(begin_section)
        if start_pos == -1:
                print("----------------------------------------------------")
                print(f"{begin_section} section not found in resume.")
        end_pos = self.resume_text.find(end_section, start_pos + len(begin_section))
        if end_pos == -1:
            end_pos = len(self.resume_text)
        # Extract the text between the start and end positions
        section_text = self.resume_text[start_pos + len(begin_section):end_pos]
        # Print the extracted text
        print("----------------------------------------------------")
        print(f"{begin_section}")
        #print(section_text)  
        return section_text
    # professional experience
    def extract_experience_section(self)->str:
        return self.extract_section(self.sections[0], self.sections[1])
    # education
    def extract_education_section(self)->str:
        return self.extract_section(self.sections[1], self.sections[2])
    # skills
    def extract_skills_section(self)->str:
        return self.extract_section(self.sections[4], self.sections[5])

    # bio
    def extract_info_section(self)->str:
        return self.extract_section("Zayneb Dhieb", self.sections[0])




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
    resume = Resume('jobApp/data/zayneb_dhieb_resume_english.pdf')
    #resume_text = resume.extract_text()
    resume.extract_info_section()
    resume.extract_experience_section()
    resume.extract_education_section()
    