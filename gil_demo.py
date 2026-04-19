import threading
import time

counter = 0

def increase():
    global counter
    for _ in range(1000000):
        counter += 1

start = time.time()

t1 = threading.Thread(target=increase)
t2 = threading.Thread(target=increase)

t1.start()
t2.start()

t1.join()
t2.join()

end = time.time()

print("Counter:", counter)
print("Time:", end - start)