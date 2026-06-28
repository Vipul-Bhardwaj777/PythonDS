# Chai price calculator

user_input = input("Please enter your order size: ").strip().lower()

price_dic = {"Small": 10, "Medium": 15, "Large": 20}

price_dic = {key.lower(): value for key, value in price_dic.items()}

if user_input in price_dic:
    print(f"Thanks for ordering! Your bill is ₹ {price_dic.get(user_input)}")
else:
    print(f"Sorry, unknown cup size!")
