# Snack System

user_input = input('Enter your preffered snack: ').lower()

if user_input == 'samosa' or user_input == 'cookies':
    print(f'Great choice! We will server you {user_input}')
else:
    print(f'Sorry, we only serve cookies and samosa with chai!')

