# Alert system

device_status = "active"
temp = 3

if device_status == "active" and temp > 35:
    print(f"Warning!! High temprature")
elif device_status == "off":
    print(f"Device is offline")
else:
    print("Temprature is normal!")
