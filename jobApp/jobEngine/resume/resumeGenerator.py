# create a class which will generate a resume based on the job description
import os   
import re
class ResumeGenerator:
    def __init__(self, job_description_url):
        match = re.match(r"(https://www\.linkedin\.com/jobs/view/\d+)", job_description_url)
        self.job_description = match.group(1) if match else None
        if not self.job_description:
            raise ValueError("Invalid job description URL. Please provide a valid LinkedIn job description URL.")
        print(f"Job description URL: {self.job_description}")
        
    def run(self):
        # run the docker container
        folder = "../../../AI_Resume_Creator"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(current_dir, folder)
        print("locating the folder")
        print(folder)
        os.chdir(folder)
        # get the current directory
        command = f"""docker run \
        -v {folder}/output/:/app/output/ \
        -v {folder}/input/:/app/input/ \
        ai-resume-creator-python-image \
        --resume /app/input/sami_dhiab_resume.yaml \
        --url "{self.job_description}"
        """

        print("running command")
        print(command)
        os.system(command)
        print("resume generated successfully")
    
    def get_resume(self):
        # locate the latest created *.pdf files in the output folder 
        output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../AI_Resume_Creator/output")
        pdf_files = [f for f in os.listdir(output_folder) if f.endswith('.pdf')]
        if not pdf_files:
            raise FileNotFoundError("No PDF files found in the output folder.")
        
        latest_pdf = max(pdf_files, key=lambda f: os.path.getctime(os.path.join(output_folder, f)))
        generated_resume_path = os.path.join(output_folder, latest_pdf)

        print(f"Generated resume located at: {generated_resume_path}")
        return generated_resume_path

# Example usage
if __name__ == "__main__":
    # Define the URL of the job description and the path to the resume
    job_description_url = "https://www.linkedin.com/jobs/view/4139695980/jkdnfbkdbfbnbjrsfnrjnkfbsr"
    
    # Initialize the ResumeGenerator with the job description URL and resume path
    resume_generator = ResumeGenerator(job_description_url)
    
    # Run the resume generator
    resume_generator.run()

    # Get the path to the generated resume
    resume_path = resume_generator.get_resume()