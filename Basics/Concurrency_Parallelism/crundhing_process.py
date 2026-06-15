from multiprocessing import Process
import time

def crunching():
    print('Started crunching...')

    total = 0
    for _ in range(10**8):
        total += 1

    print('Crunching done.')


if __name__ == '__main__':

    start_time = time.time()

    processes = [Process(target=crunching) for _ in range(2)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    end_time = time.time()

    print(f'Processing finished in {end_time - start_time:.2f} seconds')


