import time
import threading
import multiprocessing
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("full_test.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def io_task(name, delay):
    logging.info(f"{name} started")
    time.sleep(delay)
    logging.info(f"{name} finished")

def cpu_task(limit):
    total = 0
    for i in range(limit):
        total += i * i
    return total

def cpu_thread_worker(limit, results, index):
    logging.info(f"Thread-{index + 1} CPU task started")
    results[index] = cpu_task(limit)
    logging.info(f"Thread-{index + 1} CPU task finished")

def cpu_process_worker(limit, queue, name):
    setup_logging()
    logging.info(f"{name} CPU task started")
    result = cpu_task(limit)
    queue.put(result)
    logging.info(f"{name} CPU task finished")

def normal_io_test():
    print("\n" + "=" * 60)
    print("1. NORMAL I/O TEST")
    print("=" * 60)

    start = time.perf_counter()

    for i in range(3):
        io_task(f"Normal-Task-{i + 1}", 2)

    end = time.perf_counter()

    print(f"Normal I/O time: {end - start:.2f} seconds")

def threading_io_test():
    print("\n" + "=" * 60)
    print("2. THREADING I/O TEST")
    print("=" * 60)

    start = time.perf_counter()

    threads = []

    for i in range(3):
        t = threading.Thread(target=io_task, args=(f"Thread-Task-{i + 1}", 2))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.perf_counter()

    print(f"Threading I/O time: {end - start:.2f} seconds")
    print("Threading is better for waiting tasks like API calls, downloads, and file reading")

def gil_test():
    print("\n" + "=" * 60)
    print("3. GIL TEST WITH THREADS")
    print("=" * 60)

    limit = 7_000_000
    results = [None, None]

    start = time.perf_counter()

    t1 = threading.Thread(target=cpu_thread_worker, args=(limit, results, 0))
    t2 = threading.Thread(target=cpu_thread_worker, args=(limit, results, 1))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    end = time.perf_counter()

    print(f"Threaded CPU time: {end - start:.2f} seconds")
    print("Because of the GIL, threads do not help much for CPU-heavy Python work")

def multiprocessing_test():
    print("\n" + "=" * 60)
    print("4. MULTIPROCESSING TEST")
    print("=" * 60)

    limit = 7_000_000
    queue = multiprocessing.Queue()

    start = time.perf_counter()

    p1 = multiprocessing.Process(target=cpu_process_worker, args=(limit, queue, "Process-1"))
    p2 = multiprocessing.Process(target=cpu_process_worker, args=(limit, queue, "Process-2"))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    result1 = queue.get()
    result2 = queue.get()

    end = time.perf_counter()

    print(f"Multiprocessing CPU time: {end - start:.2f} seconds")
    print(f"Results collected: {result1 is not None and result2 is not None}")
    print("Multiprocessing is better for CPU-heavy tasks")

def logging_test():
    print("\n" + "=" * 60)
    print("5. LOGGING TEST")
    print("=" * 60)

    try:
        logging.info("Logging test started")
        x = 10 / 2
        logging.info(f"First result: {x}")
        y = 10 / 0
        logging.info(f"Second result: {y}")
    except ZeroDivisionError:
        logging.error("Error: division by zero")

    print("Logging test finished")
    print("Check full_test.log file")

def summary():
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print("Normal execution: one task after another")
    print("Threading: best for I/O-bound tasks")
    print("GIL: limits CPU performance with threads")
    print("Multiprocessing: best for CPU-bound tasks")
    print("Logging: useful for monitoring and debugging")

def main():
    setup_logging()
    normal_io_test()
    threading_io_test()
    gil_test()
    multiprocessing_test()
    logging_test()
    summary()

if __name__ == "__main__":
    main()