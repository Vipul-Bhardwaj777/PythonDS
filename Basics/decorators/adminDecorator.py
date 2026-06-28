from functools import wraps


def admin_decorator(func):
    wraps(func)

    def wrapper(user_role):
        if user_role != "admin":
            print("Access denied: Only for admins!!")
            return None

        else:
            return func(user_role)

    return wrapper


@admin_decorator
def access_data(role):
    print("Access Granted for data!!")


access_data("user")
access_data("admin")
