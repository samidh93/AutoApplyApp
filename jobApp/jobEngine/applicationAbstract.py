from gmail import Gmail
from candidateProfile import CandidateProfile, ChatGPT
from jobBuilderLinkedin import JobBuilder, JobParser, Job

from abc import ABC, abstractmethod

    
class Application(ABC):
    def __init__(self, candidate: CandidateProfile, jobOffers:list[Job]) -> None:
        self.candidate_profile = candidate
        self.jobs = jobOffers

    @abstractmethod
    def ApplyForJob(self, job:Job):
        pass

    
    def ApplyForAll(self):
        for j in self.jobs:
            self.ApplyForJob(j)
