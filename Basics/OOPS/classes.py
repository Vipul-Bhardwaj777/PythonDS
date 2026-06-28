class Chai:
    is_hot = True

    def describe(self):
        return f"This cup is hot ? : {'Yes' if self.is_hot else 'NO'}"


masala_chai = Chai()

# print(masala_chai.describe())

ice_tea = Chai()

ice_tea.is_hot = False

# print(ice_tea.describe())

print(Chai.describe(masala_chai))
print(Chai.describe(ice_tea))
