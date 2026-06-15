from multiprocessing import Process
import time

def brew_chai(name):
    print(f'Start brewing #{name}')
    time.sleep(3)
    print(f'End brewing #{name}')


if __name__ == "__main__":
    chai_makers = [ Process(target=brew_chai, args=(f'{i}')) for i in range(1, 4)]

    for process in chai_makers:
        process.start()

    for process in chai_makers:
        process.join()

    print('All chai served!')