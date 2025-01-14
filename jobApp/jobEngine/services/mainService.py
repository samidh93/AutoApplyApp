import subprocess
import os

current_path = os.path.dirname(os.path.abspath(__file__))
joblinkservice = current_path+"\jobLinksMicroService.py"
jobbuildservice = current_path+"\jobBuildMicroService.py"
emailapplyservice = current_path+"\emailApplyMicroService.py"
easyapplyservice = current_path+"\easyApplyMicroService.py"
directapplyservice = current_path+"\directApplyMicroService.py"
csv_jobs = "jobApp/data/links.csv"
csv_jobs = "jobApp/data/jobs.csv"

#p1 = subprocess.Popen(['python',joblinkservice, csv_jobs])
#p1.wait()
#p2 = subprocess.Popen(['python',jobbuildservice, csv_jobs, csv_jobs ])
#p2.wait()
p3 = subprocess.Popen(['python',easyapplyservice, csv_jobs])
p3.wait()
