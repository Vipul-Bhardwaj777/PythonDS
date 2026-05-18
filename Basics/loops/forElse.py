# For else loop

# data = [('Amit', 15), ('Arun', 18),("Deepak",14)]

# for name,age in data:
#     if age >= 18:
#         print(f'{name} is an adult')
#         break

# else:
#     print(f'No one is an adult!')

# value = 13

# if(remainder := value % 5):
#     print(f'Not divisible! the remainder is {remainder}')

falavours = ['ginger','lemon','mint']

while(input_flavour := input('Enter your chai flavour: ')) not in falavours:
    print(f'Sorry flavour {input_flavour} is not available!')

print(f'Your chose {input_flavour} chai!')
    
