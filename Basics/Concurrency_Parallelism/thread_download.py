import threading
import time
import requests

def download(url):
    print(f'Started downloading from {url}')
    res = requests.get(url)
    print(f'Finished downloading from {url}, size: {len(res.content)} bytes')

urls = [
    'https://picsum.photos/100',
    'https://picsum.photos/200',
    'https://picsum.photos/300',
]


start_time = time.time()
threads = [threading.Thread(target=download, args=(url, )) for url in urls]

for t in threads:
    t.start()

for t in threads:
    t.join()

end_time = time.time()


print(f'Downloading images done in {end_time - start_time:.2f}')
