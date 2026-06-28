class BaseClass:
    def __init__(self, type_):
        self.type = type_

    def prepare(self):
        return f"Preparing {self.type} chai...."


class MasalaChai(BaseClass):
    def add_spices(self):
        print("Adding ginger, cardamom, cloves...")


# order = MasalaChai('Masala')


class ChaiShop:
    chai_cls = BaseClass

    def __init__(self):
        self.chai = self.chai_cls("Ginger")

    def serve(self):
        print(f"{self.chai.prepare()}")


# order = ChaiShop()
# order.serve()


class FanceChaiShop(ChaiShop):
    chai_cls = MasalaChai


fancy = FanceChaiShop()
fancy.chai.add_spices()
