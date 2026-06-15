import threading
import time

def crunching():
    print('Started Crunching the number...')

    total = 0
    for _ in range(10**8):
        total += 1

    print('Crunching done.')

start_time = time.time()

threads = [threading.Thread(target=crunching) for _ in range(2)]

for t in threads:
    t.start()

for t in threads:
    t.join()

end_time = time.time()

print(f'Processing finished after {end_time - start_time:.2f} seconds')

