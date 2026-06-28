# Lists or Arrays

spices = ["ginger", "pepper", "cardamom"]
liquids = ["milk", "water"]

spices.extend(liquids)

spices.insert(2, "lassi")
print(f"{spices}")

array = [1, 2, 3, 4, 5, 4, 7, 8]

print(f"{spices + array}")

bytarr = bytearray(b"cinnamon")

bytearr2 = bytarr.replace(b"cinn", b"card")

# print(f'{bytearr2}')
