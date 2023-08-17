import os
import glob

class BaseConfig:
    config_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.abspath(os.path.join(config_path, "../data"))
    secrets_path = os.path.abspath(os.path.join(config_path, "../secrets"))
    @staticmethod
    def print_paths():
        print("config Path:", BaseConfig.config_path)
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
    resume_paths = glob.glob(os.path.join(BaseConfig.data_path, "*resume*.pdf"))
    cover_paths = glob.glob(os.path.join(BaseConfig.data_path, "*cover*.pdf"))
    links_file_path = glob.glob(os.path.join(BaseConfig.data_path, "*links*.csv"))
    jobs_file_path = glob.glob(os.path.join(BaseConfig.data_path, "*jobs*.csv"))
    @staticmethod
    def print_paths():
        print("Resume Paths:", UserConfig.resume_paths)
        print("Cover Paths:", UserConfig.cover_paths)
        print("Links File Path:", UserConfig.links_file_path)
        print("Jobs File Path:", UserConfig.jobs_file_path)

    @staticmethod
    def get_resume_paths():
        return UserConfig.resume_paths

    @staticmethod
    def get_cover_paths():
        return UserConfig.cover_paths

    @staticmethod
    def get_links_file_path():
        return UserConfig.links_file_path

    @staticmethod
    def get_jobs_file_path():
        return UserConfig.jobs_file_path

    @staticmethod
    def get_resume_path(resume_name):
        for resume_path in UserConfig.resume_paths:
            if resume_name in resume_path:
                return resume_path
        return None
    @staticmethod
    def get_cover_path(resume_name):
        for cover_path in UserConfig.cover_paths:
            if resume_name in cover_path:
                return cover_path
        return None
    
class AppConfig(BaseConfig):
    cookies_paths = glob.glob(os.path.join(BaseConfig.data_path, "*cookies*.pdf"))
    credentials_paths = glob.glob(os.path.join(BaseConfig.data_path, "*credentials*.pdf"))
    openai_path = glob.glob(os.path.join(BaseConfig.data_path, "*openai*.csv"))
    gmail_key_file_path = glob.glob(os.path.join(BaseConfig.data_path, "*jobs*.csv"))
    @staticmethod
    def print_paths():
        print("cookies Paths:", AppConfig.cookies_paths)
        print("credentials Paths:", AppConfig.credentials_paths)
        print("openai Path:", AppConfig.openai_path)
        print("gmail key_File Path:", AppConfig.gmail_key_file_path)

    @staticmethod
    def get_cookies_paths():
        return AppConfig.cookies_paths

    @staticmethod
    def get_credentials_paths():
        return AppConfig.credentials_paths

    @staticmethod
    def get_openai_path():
        return AppConfig.openai_path

    @staticmethod
    def get_gmail_key_file_path():
        return AppConfig.gmail_key_file_path

   
    

if __name__ == "__main__":
    config = BaseConfig()
    config.print_paths()
