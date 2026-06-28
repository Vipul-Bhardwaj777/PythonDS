from multiprocessing import Process, Queue


def brew(q):
    q.put("Masala Chai")


if __name__ == "__main__":

    q = Queue()

    p = Process(target=brew, args=(q,))
    p.start()
    p.join()

    print(q.get())
