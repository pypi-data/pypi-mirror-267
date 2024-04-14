import logging
from threading import Semaphore, Thread
from typing import Optional

logger = logging.getLogger(__name__)


def threaded(*, sema: Optional[Semaphore] = None):
    def threaded_func(func):
        """
        Decorator that multithreads the target function
        with the given parameters. Returns the thread
        created for the function
        """

        def wrapper(*args, **kwargs):
            # acquire sema if sema is provided
            if sema is not None:
                sema.acquire()
            try:
                thread = Thread(target=func, args=args, kwargs=kwargs)
                thread.start()
                if sema is not None:
                    thread.join()  # join if sema is provided, and then release
                    sema.release()
            except Exception as e:
                logger.critical(f"Failed to run thread due to exception {e}")
                raise e  # bubble up the exception
            finally:
                # release sema if acquired
                if sema is not None:
                    sema.release()

            return thread

        return wrapper

    return threaded_func
