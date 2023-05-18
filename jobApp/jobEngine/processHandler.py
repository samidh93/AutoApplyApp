'''
class for handling processes and communication betweem them on higher level:
starting, terminatingetc..
'''
import subprocess
import os


class ProcessHandler:
    def __init__(self, process_script_path:str) -> None:
        self.process_script_path = process_script_path
        self.pids= []
        self.processes = []
        
    def start_process(self)->int:
        # Start the process passed to the constructor
        print("starting new process ")
        DETACHED_PROCESS = 0x00000008
        process = subprocess.Popen(["python", self.process_script_path], creationflags=DETACHED_PROCESS )
        self.process = process
        self.pid =process.pid
        self.pids.append(self.pid)
        return process.pid

    def start_new_process(self,process_script_path)->int:
        # Start new process from this function
        print("starting new process ")
        DETACHED_PROCESS = 0x00000008
        process = subprocess.Popen(["python", process_script_path], creationflags=DETACHED_PROCESS )
        self.pid =process.pid
        self.process = process
        print(f"with pid {process.pid}")
        self.pids.append(self.pid)
        return process.pid
       
    def kill_process_pid(self, process:subprocess.Popen):
        # Kill the process passed to the constructor
        process.terminate()
        self.pids.remove(process.pid)

    def kill_last_process(self):
        self.process.terminate()
        self.pids.remove(self.process.pid)

    