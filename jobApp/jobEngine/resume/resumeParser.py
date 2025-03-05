from PyPDF2 import PdfReader, PdfWriter
#from reportlab.pdfgen import canvas # should be deleted
import pdfplumber
import os
from datetime import date
import re
import requests
import os
import docx
from urllib.parse import urlparse
from datetime import date
from ..config.config import UserConfig
import shutil
import logging
logger = logging.getLogger(__name__)

class Resume:
    def __init__(self, file_path, candidate_firstname=None, candidate_lastname= None):
        self.resume = file_path
        logger.info(f"resume file: {file_path}")
        if self.is_url(file_path): # url case: download and save it with candidate name, date under the config data
            self.resume = self.download_pdf(file_path, UserConfig.get_data_path(), candidate_firstname, candidate_lastname)
        else: # file system case: copy to config data with renaming to candidate name
            self.resume = self.move_and_rename_pdf(file_path, UserConfig.get_data_path(), candidate_firstname, candidate_lastname )
            #self.resume_text = self.generate_resume()
        ## the section must be defined in higher level apis
        self.sections = ["PROFESSIONAL EXPERIENCE", "EDUCATION", "VOLUNTEER EXPERIENCE", "TRAINING", "ACCOMPLISHMENT", "KEY COMPETENCIES"]

    def is_url(self, input_str):
        """
        Check if the given input string is a valid URL.

        :param input_str: The input string to be checked.
        :return: True if input is a valid URL, False otherwise.
        """
        parsed_url = urlparse(input_str)
        return parsed_url.scheme and parsed_url.netloc

    def download_pdf(self, url, output_directory, firstname, lastname):
        """
        Download a PDF file from the specified URL and save it with a custom filename in the specified output directory.
        
        :param url: The URL of the PDF file.
        :param output_directory: The directory where the PDF file will be saved.
        :param firstname: The first name to include in the custom filename.
        :param lastname: The last name to include in the custom filename.
        :return: The full path to the downloaded PDF file.
        """
        try:
            # Send an HTTP GET request to the PDF URL
            response = requests.get(url)
            
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Extract the filename from the URL
                filename = url.split("/")[-1]
                
                # Construct the custom filename in the "firstname_lastname_resume.pdf" format
                current_date = date.today().strftime("%Y-%m-%d")
                custom_filename = f"resume_{firstname}_{lastname}_{current_date}.pdf"
                
                # Construct the full path to save the file in the output directory
                output_path = os.path.join(output_directory, custom_filename)
                
                # Get the file content and save it to the specified output path
                with open(output_path, "wb") as file:
                    file.write(response.content)
                
                logger.info(f"PDF file downloaded successfully as {output_path}.")
                return output_path
            else:
                logger.info(f"Failed to download the PDF file. Status code: {response.status_code}")
        except Exception as e:
            logger.info(f"An error occurred: {str(e)}")
        
        return None

    
    def move_and_rename_pdf(self, input_path, output_directory, first_name, last_name):
        """
        Move and rename a PDF file to a specific location.

        :param input_path: The path to the input PDF file.
        :param output_directory: The directory where the PDF file will be moved.
        :param first_name: The first name for the new filename.
        :param last_name: The last name for the new filename.
        :return: The full path to the moved and renamed PDF file.
        """
        try:
            # Check if the input file exists
            if not os.path.isfile(input_path):
                raise FileNotFoundError("Input PDF file not found.")
            
            # Get the current date in YYYY-MM-DD format
            today_date = date.today().strftime("%Y-%m-%d")
            
            # Construct the new filename using first name, last name, and today's date
            new_filename = f"resume_{first_name}_{last_name}_{today_date}.pdf"
            
            # Construct the full path for the new location
            new_path = os.path.join(output_directory, new_filename)
            
            # copy the file to the new location
            shutil.copy(input_path, new_path)
            
            logger.info(f"PDF file copied and renamed to {new_path}.")
            return new_path
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
        
        return None

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
        ##logger.info(text)
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
                logger.info("----------------------------------------------------")
                logger.info(f"{begin_section} section not found in resume")
                exit()
            end_match = re.search(end_regex, self.resume_text, start_match.end())
            if not end_match:
                end_pos = len(self.resume_text)
            else:
                end_pos = end_match.start()
            # Extract the text between the start and end positions
            section_text = self.resume_text[start_match.end():end_pos]
            # Print the extracted text
            logger.info("----------------------------------------------------")
            logger.info(f"{begin_section}")
            #logger.info(section_text)    
            return section_text
        
        # Simple string search
        start_pos = self.resume_text.find(begin_section)
        if start_pos == -1:
                logger.info("----------------------------------------------------")
                logger.info(f"{begin_section} section not found in resume.")
        end_pos = self.resume_text.find(end_section, start_pos + len(begin_section))
        if end_pos == -1:
            end_pos = len(self.resume_text)
        # Extract the text between the start and end positions
        section_text = self.resume_text[start_pos + len(begin_section):end_pos]
        # Print the extracted text
        logger.info("----------------------------------------------------")
        logger.info(f"{begin_section}")
        #logger.info(section_text)  
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
        return self.extract_section("first last", self.sections[0])




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
    resume = Resume('https://708f8437-9497-45e7-a86f-8a969c24d91c.usrfiles.com/ugd/4b8c9.pdf')
    

    