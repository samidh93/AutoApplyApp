from gmail import Gmail
from candidateProfile import CandidateProfile, ChatGPT
from jobBuilderLinkedin import JobBuilder, JobParser, Job

from abc import ABC, abstractmethod

    
class Application(ABC):
    def __init__(self, candidate: CandidateProfile, jobOffers:list[Job]) -> None:
        self.candidate = candidate
        self.jobs_to_apply_for = jobOffers

    @abstractmethod
    def ApplyForJob(self, job:Job):
        pass

    
    def ApplyForAll(self):
        for j in self.jobs_to_apply_for:
            self.ApplyForJob(j)
