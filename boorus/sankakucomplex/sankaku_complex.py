from time import strftime, gmtime, sleep, time
from os import makedirs, getcwd, unlink, path
from urllib.parse import urlencode
from re import findall as regex
from html import unescape
from json import loads
import requests, sys

host_headers = {
    'Host': 'chan.sankakucomplex.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Cookie': 'locale=en; auto_page=0; hide-news-ticker=1',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1'
}

image_headers = {
    'Host': 'cs.sankakucomplex.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'TE': 'Trailers'
}

class Settings(object):
    timeout = 5
    counter = 0
    stream  = True
    
    def inc_counter(self):
        self.counter += 1
        
    def set_timeout(self, value):
        self.timeout = value
        self.counter = 0
        
    def set_stream(self, value):
        self.stream = True \
            if str(type(value)).split('\'')[1] != 'bool' \
            else value

settings = Settings()

def safe_name(name):
    output = ""
    for char in name:
        if char not in '\\/<>:"|?*':
            output = f'{output}{char}'

    return output

def download(url, folder, filename):
    try:
        filepath = path.join(folder, f'{settings.counter}_{filename}')
        if not path.exists(folder):
            makedirs(folder)
            
        if path.isfile(filepath):
            return None
            
        sleep(settings.timeout)
        r = requests.get(f'https:{unescape(url)}', stream=settings.stream, headers=image_headers)
        
        if r.status_code > 399:
            raise Exception(f'{r.status_code}: {r.reason}')
        
        with open(filepath, 'wb') as f:
            total_length = int(r.headers.get('content-length')) if not None else 0
            download = 1

            if total_length == 0:
                f.write(r.content)

            else:
                for chunk in r.iter_content(1024):
                    download += len(chunk)
                    f.write(chunk)

                    done = int(50 * download / total_length)
                    print(f"\r[{'=' * done}{' ' * (50 - done)}] {(download / 1048576.0):.02f} MiB of {(total_length / 1048576.0):.02f} MiB", end="")
                    sys.stdout.flush()
        
        settings.inc_counter()
    except Exception as ex:
        sys.stderr.write(f'download: {ex}\n')

def get_image(link, query):
    try:
        sleep(settings.timeout)
        r = requests.get(f'https://chan.sankakucomplex.com{link}', headers=host_headers)
        
        if r.status_code > 399:
            raise Exception(f'{r.status_code}: {r.reason}')
        
        images = regex(r'\<li\>Original\: \<a href\=\"(.*?)\" id\=highres', r.text)
        for image in images:
            folder = path.join(getcwd(), 'Images', safe_name(query.replace('+', ' & ')))
            filename = image.split('/')[-1].split('?')[0]
            download(image, folder, filename)

    except Exception as ex:
        sys.stderr.write(f'get_image: {ex}\n')
        
def get_next(image, query):
    try:
        sleep(settings.timeout)
        r1 = requests.get(f'https://chan.sankakucomplex.com/post/index.content?next={image}&tags={query}', headers=host_headers)
        
        if r1.status_code > 399:
            raise Exception(f'{r1.status_code}: {r1.reason}')
            
        links  = regex(r'\<a href\=\"(.*?)\" onclick\=\"', r1.text)
        nextid = get_latest(query, links[-1].split('/')[-1])
        
        sleep(settings.timeout)
        r2 = requests.get(f'https://chan.sankakucomplex.com/post/index.content?next={nextid}&tags={query}', headers=host_headers)
        
        if r2.status_code > 399:
            raise Exception(f'{r2.status_code}: {r2.reason}')
            
        lonks = regex(r'\<a href\=\"(.*?)\" onclick\=\"', r2.text)
        for link in lonks:
            get_image(link, query)
        
        get_next(nextid, query)
    
    except Exception as ex:
        sys.stderr.write(f'get_next: {ex}\n')
        
def get_latest(query, image):
    try:
        sleep(settings.timeout)
        r = requests.get(f'https://chan.sankakucomplex.com/post/index.content?next={image}&tags={query}', headers=host_headers)
        
        if r.status_code > 399:
            raise Exception(f'{r.status_code}: {r.reason}')
            
        links = regex(r'\<a href\=\"(.*?)\" onclick\=\"', r.text)
        return links[1].split('/')[-1]
        
    except Exception as ex:
        sys.stderr.write(f'get_latest: {ex}\n')
        
def search(name, series=None):
    try:
        settings.counter = 0
        query = f'{name.lower()}' if series is None else f'{name.lower()}_({series.lower().replace(" ", "_")})'
        
        sleep(settings.timeout)
        r = requests.get(f'https://chan.sankakucomplex.com/post/index.content?tags={query}', headers=host_headers)
        
        if r.status_code > 399:
            raise Exception(f'{r.status_code}: {r.reason}')
            
        links = regex(r'\<a href\=\"(.*?)\" onclick\=\"', r.text)
        for link in links:
            get_image(link, query)
        
        get_next(links[0].split('/')[-1], query)
        
    except Exception as ex:
        sys.stderr.write(f'search: {ex}\n')