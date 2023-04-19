import fcntl

class FileLocker:
    def __init__(self) -> None:
        pass

    def lockForRead(self, file):
        # Acquire a shared lock on the file
        fcntl.flock(file, fcntl.LOCK_SH)
    def lockForWrite(self,file):
        # Acquire a lock on the file
        fcntl.flock(file, fcntl.LOCK_EX)
    def unlock(self, file):
        #unlock
        fcntl.flock(file, fcntl.LOCK_UN)


    