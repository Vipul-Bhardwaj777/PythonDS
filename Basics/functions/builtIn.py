# Built in fns

# __doc is called Dunder double underscore - dunder doc dunder name etc
#  we use """ """ for doc of a fn


def calculate_bill():
    """
    This fn calculates the chai bill
    """
    print("Calculating chai bill!!")


print(f"{calculate_bill.__doc__}")
