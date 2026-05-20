#Print order

def python_function():
    print('Hii this is first function')
    
# python_function()

orders =[100,300,399,398]

gstPercent = 10

def calculateBill(price):
    return price + price * (18/100)

for price in orders:
    bill = calculateBill(price)
    print(f'Your bill is {bill}')

