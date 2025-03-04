# create a class which will generate a resume based on the job description
import os   

class ResumeGenerator:
    def __init__(self, job_description_url, resume_path):
        self.job_description = job_description_url
        self.resume_path = resume_path
    
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


# Example usage
if __name__ == "__main__":
    # Define the URL of the job description and the path to the resume
    job_description_url = "https://www.linkedin.com/jobs/view/4143254223"
    resume_path = "path/to/resume.yaml"
    
    # Initialize the ResumeGenerator with the job description URL and resume path
    resume_generator = ResumeGenerator(job_description_url, resume_path)
    
    # Run the resume generator
    resume_generator.run()