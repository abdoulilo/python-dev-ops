import threading
import time
from common.logger_config import get_logger

logger = get_logger("threading_demo")

def download_task(task_id, delay):
    logger.info(f"Task {task_id} started")
    time.sleep(delay)
    logger.info(f"Task {task_id} finished")

def run_threading_demo():
    start = time.perf_counter()

    threads = []

    for i in range(5):
        thread = threading.Thread(target=download_task, args=(i + 1, 2))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end = time.perf_counter()
    total = end - start

    print("\nTHREADING RESULT")
    print(f"Total time: {total:.2f} seconds")
    print("Best for: I/O tasks like waiting, downloading, API calls, reading files")

if __name__ == "__main__":
    run_threading_demo()