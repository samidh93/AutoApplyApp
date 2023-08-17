from abc import ABC, abstractmethod


class ApplicationBuilder(ABC):
    @abstractmethod
    def set_candidate_profile(self, profile):
        pass

    @abstractmethod
    def set_jobs(self, jobs):
        pass

    @abstractmethod
    def build_application(self):
        pass

