class Chai:
    def __init__(self, type_, strength):
        self.type = type_
        self.strength = strength

class MasalaChai(Chai):
    def __init__(self, type_, strength, milk):
        super().__init__(type_, strength)
        self.milk = milk