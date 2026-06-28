# Types of functions


def pure_fn(cups):
    return cups * 2


chai_cups = 10


def impure_fn():
    global chai_cups
    chai_cups += 10
    return chai_cups


def recursive_fn(n):
    print(f"{n}")
    if n == 0:
        print("All iterations over!")
        return

    return recursive_fn(n - 1)


res_pure = pure_fn(10)
res_impure = impure_fn()


print(f"Pure fn: {res_pure}, Impure fn: {impure_fn}")

recursive_fn(3)
