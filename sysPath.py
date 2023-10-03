import sys
import os

class PathManager:
    def __init__(self):
        # Get the path to the project's root directory
        self.project_root = os.path.dirname(os.path.abspath(__file__))

    def add_project_root_to_sys_path(self):
        # Add the project root to sys.path
        sys.path.insert(0, self.project_root)

    def show_sys_path(self):
        # Display the current sys.path
        for path in sys.path:
            print(path)

# Example usage:
if __name__ == "__main__":
    #path_manager = PathManager()
    #path_manager.add_project_root_to_sys_path()
    #path_manager.show_sys_path()import os
    import multiprocessing
    import os
    num_cores = os.cpu_count()
    
    print(f"Number of CPU cores (threads) available: {num_cores}")