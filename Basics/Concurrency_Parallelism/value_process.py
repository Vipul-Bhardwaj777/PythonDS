from multiprocessing import Process, Value

def increment(count):
    for _ in range(100000):
        with count.get_lock():
            count.value += 1


if __name__ == '__main__':
    count = Value('i', 0)

    p = Process(target=increment, args=(count, ))
    p.start()
    p.join()

    print(count.value)