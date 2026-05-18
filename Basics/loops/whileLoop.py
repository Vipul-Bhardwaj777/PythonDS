# while loop

# temp = 10

# while temp < 100:
#     print(f"Temprature is {temp}")
#     temp += 15

# print('Tea is boiling')

flavours = ['ginger','out of stock','discontinued', 'tulsi']

for flavour in flavours:
    if flavour == 'out of stock':
        continue
    if flavour == 'discontinued':
        print(f'{flavour} flavour found')
        break

    print(f'{flavour} found')
