#sets 

newSet = {'ginger', 'cloves', 'cardamom'}
newSet2 = {'black pepper', 'lassi','cloves'}

union = newSet | newSet2
intersection = newSet & newSet2
differences = newSet2 - newSet

print(f'{union}')
print(f'{intersection}')
print(f'{differences}')