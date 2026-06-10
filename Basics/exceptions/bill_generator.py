class InvalidChaiError(Exception): pass

def generate_bill(flavour, cups):
    menu = {'masala': 20, 'ginger': 40}
    try:
        if flavour not in menu:
            raise InvalidChaiError('Chai flavour not available!')
        
        if not isinstance(cups, int):
            raise TypeError('Cups should be in integer!')
    
    except Exception as e:
        print(f'Error: {e}')

    else: 
        bill = menu[flavour] * cups
        print(f'Your bill for {cups} cups of {flavour} chai is : {bill}')
    finally:
        print('Thanks for visiting Chai Shop!')

generate_bill('lemon', 2)
generate_bill('masala', 'five')
generate_bill('ginger', 3)