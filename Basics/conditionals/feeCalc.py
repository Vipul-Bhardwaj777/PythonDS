# Fees calculator

user_order_input = input('Plese enter your order amount: ').strip()

if user_order_input.isdigit():
    user_order_input = int(user_order_input)
    delivery_fees = 0 if user_order_input > 300 else 40 
    print(f'Delivery fees is: {delivery_fees}')

else:
    print(f'Invalid input!!')
    