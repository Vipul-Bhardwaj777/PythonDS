def generator():
    yield "cup 1"
    yield "cup 2"
    yield "cup 3"


cups = generator()

# for cup in cups:
#     print(f'{cup}')


def infinite_chai():
    count = 1

    while True:
        yield f"Refill chai {count}"
        count += 1


refill = infinite_chai()

# for _, indx in enumerate(range(6)):
#     print(next(refill))


def chai_customer():
    print("Hii! what chai would you take")

    order = yield

    while True:
        print(f"Preparign: {order}")
        order = yield


stall = chai_customer()

# next(stall)

# stall.send('Masala chai')


def local_chai():
    yield "masala chai"
    yield "ginger chai"


def imported_chai():
    yield "macha"
    yield "oolong"


def full_menu():
    yield from local_chai()
    yield from imported_chai()


# for chai in full_menu():
#     print(chai)


def tea_stall():
    try:
        while True:
            order = yield "Waiting for order"
    except:
        print("Stall closed")


stall = tea_stall()

print(next(stall))

stall.close()
