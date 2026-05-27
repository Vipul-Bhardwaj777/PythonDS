# Params 

def make_chai(*ingredients,**extras):
    print(f'Ingredients: {ingredients}, Extras: {extras}')

make_chai('ginger','cinnamon','cardamom',milk='full cream')


def empty_param(array=None):
    if array is None: return
    array.append('Hii')
    print(f'{array}')

# empty_param()
# empty_param()