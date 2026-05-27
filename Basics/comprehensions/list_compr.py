menu = [
    'masala chai',
    'ginger chai',
    'iced ginger chai',
    'iced tea',
    'iced peach tea',
    'iced lemon tea',
    'iced tea',
    'masala chai'
]

filtered_menu = [item for item in menu if 'chai' in item]

# print(f'{filtered_menu}')

unique_orders = {item for item in menu}

# print(f'{unique_orders}')

recepies = {
    'milk tea':['milk','water','tea','sugar'],
    'black tea':['water','tea','sugar'],
    'elaichi tea':['water','tea','sugar','milk','elaichi'],
    'spicy tea':['water','tea','sugar','milk','elaichi','ginger','black pepper'],
}


unique_ingredients = {item for ingred in recepies.values() for item in ingred}

# print(f'{unique_ingredients}')


chai_prices = {
    'ginger chai': 40,
    'masala chai':80,
    'elaichi chai':90,
    'green tea':90,
}

chai_prices_usd = {tea:price/95 for tea, price in chai_prices.items()}

# print(f'{chai_prices_usd}')

daily_sales = [3,4,5,23,66,34,57,8,3]

sum_good_sales = sum(sale for sale in daily_sales if sale > 5 )

print(f'{sum_good_sales}')