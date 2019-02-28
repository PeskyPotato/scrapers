import requests
import json
from multiprocessing import Pool
import os

def scrap(image):
    while (1):
        if image == 404:
            image += 1
        print(image)
        
        data = requests.get('https://xkcd.com/{}/info.0.json'.format(image))
        try:
            data = data.json()
        except json.decoder.JSONDecodeError:
            break
        with open('comics/{}-{}.{}'.format(data['num'], data['safe_title'], data['img'].split(".")[-1]), 'wb') as i:
            i.write(requests.get(data['img']).content)

        with open('json/{}-{}.json'.format(data['num'], data['safe_title']), 'w') as f:
            json.dump(data, f)

        image += 1

def findEnd():
    image = 2117
    while(1):
        try:
            requests.get('https://xkcd.com/{}/info.0.json'.format(image)).json()
        except json.decoder.JSONDecodeError:
            return image
        image += 1


if not os.path.exists('comics/'):
    os.makedirs('comics/')
if not os.path.exists('json/'):
    os.makedirs('json/')

images = []
images.extend(range(1,findEnd() + 1))

with Pool(processes = 5) as pool:
    pool.map(scrap, images, 3)