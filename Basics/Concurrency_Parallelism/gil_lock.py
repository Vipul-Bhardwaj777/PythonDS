import threading
import time

def brew():
    print(f'{threading.current_thread().name} Brewing started')
    count = 0

    for _ in range(100_000_000):
        count += 1
    
    print(f'{threading.current_thread().name} Brewing Ended')


thread_1 = threading.Thread(target=brew, name='Barista-1')
thread_2 = threading.Thread(target=brew, name='Barista-2')

start_time = time.time() 

thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()

end_time = time.time()

print(f'Task completed in {end_time - start_time:.2f} seconds')