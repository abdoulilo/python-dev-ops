import threading
import time
from common.logger_config import get_logger

logger = get_logger("gil_demo")

def cpu_task(limit):
    total = 0
    for i in range(limit):
        total += i * i
    return total

def worker(limit, results, index):
    logger.info(f"Thread {index + 1} started CPU task")
    results[index] = cpu_task(limit)
    logger.info(f"Thread {index + 1} finished CPU task")

def run_gil_demo():
    limit = 8_000_000
    results = [None, None]

    start = time.perf_counter()

    t1 = threading.Thread(target=worker, args=(limit, results, 0))
    t2 = threading.Thread(target=worker, args=(limit, results, 1))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    end = time.perf_counter()
    total = end - start

    print("\nGIL DEMO RESULT")
    print(f"Total time with 2 threads on CPU work: {total:.2f} seconds")
    print("Meaning: threads do not speed up CPU-heavy Python code much because of the GIL")

if __name__ == "__main__":
    run_gil_demo()