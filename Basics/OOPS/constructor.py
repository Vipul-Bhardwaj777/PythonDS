class Chai:
    def __init__(self, flavour, size):
        self.flavour = flavour
        self.size = size

    def describe(self):
        return f"{self.size}ml of {self.flavour} chai!"


order = Chai("giner", 200)

order_two = Chai("masala", 100)

print(order.describe())
print(order_two.describe())
