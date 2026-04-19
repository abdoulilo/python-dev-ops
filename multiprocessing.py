from multiprocessing import Process, Queue
import time
from common.logger_config import get_logger

logger = get_logger("multiprocessing_demo")

def cpu_task(limit, queue, worker_name):
    logger.info(f"{worker_name} started CPU task")
    total = 0
    for i in range(limit):
        total += i * i
    queue.put(total)
    logger.info(f"{worker_name} finished CPU task")

def run_multiprocessing_demo():
    limit = 8_000_000
    queue = Queue()

    start = time.perf_counter()

    p1 = Process(target=cpu_task, args=(limit, queue, "Process-1"))
    p2 = Process(target=cpu_task, args=(limit, queue, "Process-2"))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    result1 = queue.get()
    result2 = queue.get()

    end = time.perf_counter()
    total = end - start

    print("\nMULTIPROCESSING RESULT")
    print(f"Total time: {total:.2f} seconds")
    print("Best for: CPU-heavy tasks like calculations, data processing, image processing")
    print(f"Results collected: {result1 is not None and result2 is not None}")

if __name__ == "__main__":
    run_multiprocessing_demo()