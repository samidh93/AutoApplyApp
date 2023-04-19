import subprocess
import os

current_path = os.path.dirname(os.path.abspath(__file__))

joblinkservice = "\jobLinksMicroService.py"
jobbuildservice = "\jobBuildMicroService.py"
emailapplyservice = "\emailApplyMicroService.py"
# start the firsf'
#p1 = subprocess.Popen(['python', current_path+joblinkservice])
#p1.wait()

# start the seconf'
p2 = subprocess.Popen(['python', current_path+jobbuildservice])
p2.wait()

# start the thirf'
p3 = subprocess.Popen(['python', current_path+emailapplyservice])
p3.wait()
