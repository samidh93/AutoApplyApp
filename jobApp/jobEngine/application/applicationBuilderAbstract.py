from abc import ABC, abstractmethod


class ApplicationBuilder(ABC):
    @abstractmethod
    def set_candidate_profile(self, profile):
        pass

    @abstractmethod
    def set_jobs_file(self, jobsFile):
        pass

    @abstractmethod
    def build_application(self):
        pass

