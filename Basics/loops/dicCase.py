users = [
    {'name':'Aman','total_bill':3009,'coupon':'P20'},
    {'name':'Sandeep','total_bill':389,'coupon':'FF10'},
    {'name':'Vipul','total_bill':399,'coupon':'P50'},
]

discounts = {
    'P20':(0.2,0),
    'FF10':(0.15,0),
    'P50':(0.28,0)
}

for user in users:
    disc_percent, flat_disc = discounts.get(user.get('coupon'),(0,0))

    total_discount = user.get('total_bill') * disc_percent / 100 + flat_disc

    print(f'{user.get('name')} payed {user.get('total_bill')} and got a discount of {total_discount:.2f}')