import threading
import time

def take_orders():
    for i in range(1,4):
        print(f'Taking order for #{i}')
        time.sleep(3)

def brew_chai():
    for i in range(1,4):
        print(f'Brewing chai for #{i}')
        time.sleep(4)

orders_thread = threading.Thread(target=take_orders)
brew_thread = threading.Thread(target=brew_chai)

orders_thread.start()
brew_thread.start()

orders_thread.join()
brew_thread.join()

print('Chai shop closed for the day!')