import fcntl
import logging
logger = logging.getLogger(__name__)

class FileLocker:
    def __init__(self):
        pass

    def lockForRead(self, file):
        try:
            # Acquire a shared lock on the file for reading
            fcntl.flock(file, fcntl.LOCK_SH)
            logger.info("Locking file for reading")
        except Exception as e:
            logger.info(f"Failed to lock for reading: {str(e)}")

    def lockForWrite(self, file):
        try:
            # Acquire an exclusive lock on the file for writing
            fcntl.flock(file, fcntl.LOCK_EX)
            logger.info("Locking file for writing")
        except Exception as e:
            logger.info(f"Failed to lock for writing: {str(e)}")

    def unlock(self, file):
        try:
            # Release the lock on the file
            fcntl.flock(file, fcntl.LOCK_UN)
            logger.info("Unlocking file")
        except Exception as e:
            logger.info(f"Failed to unlock: {str(e)}")