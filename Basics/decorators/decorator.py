from functools import wraps


def my_decorator(fun):

    @wraps(fun)
    def wrapper():
        print("Before the fn")
        fun()
        print("After the fn")

    return wrapper


@my_decorator
def greet():
    print("Hii")


greet()

print(greet.__name__)
