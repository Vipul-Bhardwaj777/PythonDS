# Range and for loop

# for token in range(1,11):
#     print(f'Serving chai to token #{token}')

name_list = ['Hitesh', 'Vipul', 'Aman']
bills = [20,39,49]
# for name in name_list:
#     print(f'Order ready for name {name}')

# for idx, name in enumerate(name_list,start = 1):
#     print(f"{idx} : {name}'s chai")

for name, amount in zip(name_list,bills):
    print(f'{name} payed {amount} rupees')