import fcntl

class FileLocker:
    def __init__(self):
        pass

    def lockForRead(self, file):
        try:
            # Acquire a shared lock on the file for reading
            fcntl.flock(file, fcntl.LOCK_SH)
            print("Locking file for reading")
        except Exception as e:
            print(f"Failed to lock for reading: {str(e)}")

    def lockForWrite(self, file):
        try:
            # Acquire an exclusive lock on the file for writing
            fcntl.flock(file, fcntl.LOCK_EX)
            print("Locking file for writing")
        except Exception as e:
            print(f"Failed to lock for writing: {str(e)}")

    def unlock(self, file):
        try:
            # Release the lock on the file
            fcntl.flock(file, fcntl.LOCK_UN)
            print("Unlocking file")
        except Exception as e:
            print(f"Failed to unlock: {str(e)}")