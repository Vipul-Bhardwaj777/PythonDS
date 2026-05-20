#Scopes

txt = 'Whiskey'

def outer_fn():
    txt = 'Chai'
    def inner_fn():
        global txt
        txt = 'Holy cow!!'
        print(f'inner text {txt}')
    
    inner_fn()
    print(f'Outer text {txt} ')

outer_fn()

print(f'Global text {txt}')