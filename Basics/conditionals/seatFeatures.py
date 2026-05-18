# Train seat features

seat_type = input('Enter your seat: ').strip().lower()

match seat_type:
    case 'sleeper':
        print('Non Ac, no food')
    case 'ac':
        print('Ac, food')
    case 'luxury':
        print('With AC, food, drinks')
    case _:
        print('Sorry no seat found!')