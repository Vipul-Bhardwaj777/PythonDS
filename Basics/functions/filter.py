# Filter with Lambda fns

array = ["Amit", "Arun", "Karan", "Kunal", "Amit"]

filter_arr = list(filter(lambda name: name != "Amit", array))

print(f"{filter_arr}")
