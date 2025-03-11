import os
import glob
import json
import logging
logger = logging.getLogger(__name__)

class BaseConfig:
    config_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.abspath(os.path.join(config_path, "../../data/"))
    secrets_path = os.path.abspath(os.path.join(config_path, "../../secrets/"))
    @staticmethod
    def print_files():
        print("config base Path:", BaseConfig.config_path)
        print("Data Path:", BaseConfig.data_path)
        print("secrets Path:", BaseConfig.secrets_path)

    @staticmethod
    def get_data_path():
        return BaseConfig.data_path
    @staticmethod
    def get_secrets_path():
        return BaseConfig.secrets_path
    @staticmethod
    def get_config_path():
        return BaseConfig.config_path
    
class UserConfig(BaseConfig):
    resume_files:list = glob.glob(os.path.join(BaseConfig.data_path, "*resume*.pdf"))
    cover_files:list = glob.glob(os.path.join(BaseConfig.data_path, "*cover*.pdf"))
    links_files:list = glob.glob(os.path.join(BaseConfig.data_path, "*links*.csv"))
    jobs_files:list = glob.glob(os.path.join(BaseConfig.data_path, "*jobs*.csv"))
    result_files:list = glob.glob(os.path.join(BaseConfig.data_path, "*result*.json"))
    cookies_files:list = glob.glob(os.path.join(BaseConfig.secrets_path, "*cookies*.json"))

    @staticmethod
    def print_files():
        print("Resume files:", UserConfig.resume_files)
        print("Cover files:", UserConfig.cover_files)
        print("Links files:", UserConfig.links_files)
        print("Jobs files:", UserConfig.jobs_files)
        print("Result files:", UserConfig.result_files)
        print("cookies files:", UserConfig.cookies_files)

    @staticmethod
    def get_resume_files():
        return UserConfig.resume_files

    @staticmethod
    def get_cover_files():
        return UserConfig.cover_files

    @staticmethod
    def get_links_files():
        return UserConfig.links_files
    
    @staticmethod
    def get_result_files():
        return UserConfig.result_files
    @staticmethod
    def get_cookies_files():
        return UserConfig.cookies_files
    @staticmethod
    def get_cookies_file(byowner, byfield):
        for cookie_file in UserConfig.cookies_files:
            print("cookies file: ", cookie_file)
            if byowner in cookie_file and byfield in cookie_file:
                print("cookie file found: ", cookie_file)
                return cookie_file
        return None

    @staticmethod
    def get_jobs_files(job_title:str, job_location:str, field_id:str):
        for job_file in UserConfig.jobs_files:
            if job_title.replace(" ", "_").replace(",","_") in job_file and job_location.replace(" ", "_").replace(",","_") in job_file and field_id.replace(" ", "_").replace(",","_") in job_file:
                print("find jobs file: ", job_file)
                return job_file
        return None
    
    @staticmethod
    def get_jobs_result_json_path(jobs_csv_in:str):
        # Remove the .csv extension and append "result.json"
        base_name = os.path.splitext(jobs_csv_in)[0]
        result_file = f"{base_name}_result.json"
        logger.info(f"jobs result file: {result_file}")
        return result_file

    @staticmethod
    def find_jobs_result_json_file(unique_id, return_data_json=True):
        for result_path in UserConfig.result_files:
            if unique_id in result_path:
                if os.path.isfile(result_path):
                    with open(result_path, 'r') as json_file:
                        json_data:dict = json.load(json_file)
                        if return_data_json:
                            return json_data
                        else:
                            # If return_data_json is False, return the file path
                            return result_path

        # Return None if the file is not found
        return None
    
    @staticmethod
    def get_resume_path(resume_name):
        for resume_path in UserConfig.resume_files:
            if resume_name in resume_path:
                return resume_path
        return None
    @staticmethod
    def get_cover_path(cover_name):
        for cover_path in UserConfig.cover_files:
            if cover_name in cover_path:
                return cover_path
        return None
    
class AppConfig(BaseConfig):
    credentials_files = glob.glob(os.path.join(BaseConfig.data_path, "*credentials*.pdf"))
    openai_path = glob.glob(os.path.join(BaseConfig.data_path, "*openai*.csv"))
    gmail_key_files = glob.glob(os.path.join(BaseConfig.data_path, "*jobs*.csv"))
    @staticmethod
    def print_files():
        print("credentials files:", AppConfig.credentials_files)
        print("openai Path:", AppConfig.openai_path)
        print("gmail key_File Path:", AppConfig.gmail_key_files)



    @staticmethod
    def get_credentials_files():
        return AppConfig.credentials_files

    @staticmethod
    def get_openai_path():
        return AppConfig.openai_path

    @staticmethod
    def get_gmail_key_files():
        return AppConfig.gmail_key_files

   
    

if __name__ == "__main__":
    print("BaseConfig Path:", BaseConfig().get_secrets_path())
    #userconfig = UserConfig()
    #file = userconfig.secrets_path
    #print("file path returned: ", file)
    
