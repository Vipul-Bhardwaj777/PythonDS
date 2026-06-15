from multiprocessing import Process, cpu_count
import time

def brew():
    print('Brewing started')
    count = 0

    for _ in range(100_000_000):
        count += 1

    print('Brewing Ended')

if __name__ == '__main__':
    start_time = time.time()

    logical_cores = cpu_count()
    pohysical_cores = int(logical_cores/2)


    processes = [Process(target=brew) for _ in range(pohysical_cores)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    end_time = time.time()

    print(f'Brewing ended in {end_time - start_time:.2f} seconds')