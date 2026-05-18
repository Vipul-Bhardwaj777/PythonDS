#Dictionary

newDict = dict(type = 'cofee', ingredient = 'milk', sugar = 0)
newDict2 = {"type":'chai','ingredient':'ginger','sugar':2}

newDict2['base'] = 'milk'

del newDict2['sugar']
# print(f'{newDict2['base']}')
print(f'{newDict2.keys()}')
print(f'{newDict2.values()}')
print(f'{newDict2.items()}')

# newDict.update(newDict2)
# print(f'{newDict2.get('sugar','Sugarfree!!')}')