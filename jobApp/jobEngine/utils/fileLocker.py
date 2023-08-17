
class FileLocker:
    def __init__(self) -> None:
        pass

    def lockForRead(self, file):
        # Acquire a shared lock on the file
        #msvcrt.locking(file.fileno(), msvcrt.LK_LOCK, 1)
        print("locking file for reading")
    def lockForWrite(self,file):
        # Acquire a lock on the file
        #msvcrt.locking(file.fileno(), msvcrt.LK_LOCK, 1)
        print("locking file for writing")

    def unlock(self, file):
        #unlock
        #msvcrt.locking(file.fileno(), msvcrt.LK_UNLCK, 1)
        print("unlocking file")



    