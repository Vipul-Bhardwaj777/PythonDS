from functools import wraps


def my_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Logging before {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Logging after {func.__name__}")
        return result

    return wrapper


@my_logger
def brew_chai(type, milk="no"):
    print(f"Brewing {type} chai, and milk status is {milk}")


brew_chai("Masala")
