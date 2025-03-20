# create a class which will generate a resume based on the job description
import os   
import re
import logging
logger = logging.getLogger(__name__)

class ResumeGenerator:
    def __init__(self, job_description_url):
        match = re.match(r"(https://www\.linkedin\.com/jobs/view/\d+)", job_description_url)
        self.job_description = match.group(1) if match else None
        if not self.job_description:
            raise ValueError("Invalid job description URL. Please provide a valid LinkedIn job description URL.")
        logger.info(f"Job description URL: {self.job_description}")
        
    def run(self, firstname:str, lastname:str):
        # run the docker container
        folder = "../../../AI_Resume_Creator"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(current_dir, folder)
        logger.info("locating the folder")
        logger.info(folder)
        os.chdir(folder)
        # get the current directory
        command = f"""docker run \
        -v {folder}/output/:/app/output/ \
        -v {folder}/input/:/app/input/ \
        ai-resume-creator-python-image \
        --resume /app/input/{firstname.lower()}_{lastname.lower()}_resume.yaml \
        --job_description_url "{self.job_description}"
        """

        logger.info("running command")
        logger.info(command)
        os.system(command)
        logger.info("resume generated successfully")
    
    def get_resume(self, firstname:str, lastname:str, company:str):
        # locate the latest created *.pdf files in the output folder 
        output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../AI_Resume_Creator/output")
        resume_pdf = f"{firstname.lower()}_{lastname.lower()}_resume_{company}.pdf"
        generated_resume_path = os.path.join(output_folder, resume_pdf)
        resume_path = os.path.abspath(generated_resume_path)
        logger.info(f"Generated resume located at: {resume_path}")
        return resume_path
    
    def get_resume_content(self, firstname:str, lastname:str, company:str):
        input_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../AI_Resume_Creator/input")
        resume_yaml =  f"{firstname.lower()}_{lastname.lower()}_resume_{company}.yaml"
        resume_yaml_path = os.path.join(input_folder, resume_yaml)
        with open(resume_yaml_path, 'r') as file:
            resume_content = file.read()
        logger.info(f"Resume content read from {resume_yaml_path}")
        logger.info(resume_content)
        return resume_content

# Example usage
if __name__ == "__main__":
    # Define the URL of the job description and the path to the resume
    job_description_url = "https://www.linkedin.com/jobs/view/4139695980/jkdnfbkdbfbnbjrsfnrjnkfbsr"
    
    # Initialize the ResumeGenerator with the job description URL and resume path
    resume_generator = ResumeGenerator(job_description_url)
    
    # Run the resume generator
    #resume_generator.run()

    # Get the path to the generated resume
    resume_path = resume_generator.get_resume()

    # Get the content of the generated resume
    resume_content = resume_generator.get_resume_content("sami", "dhiab")