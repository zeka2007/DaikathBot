from random import randint, choice
from bs4 import BeautifulSoup
import requests
from PIL import Image

def parse_meme(type = None, search = None):
    result = False
    work = True
    while work:
        try:
            if type == 'trands':
                url = 'https://memepedia.ru/category/memes/trends/page/' + str(randint(1, 25)) + '/'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 YaBrowser/20.12.3.138 Yowser/2.5 Safari/537.36'
                }
                response = requests.get(url, headers = headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                meme = choice(soup.findAll('li', class_ = 'post-item post-item-four-column')) # post-item post-item-masonry-boxed

                url = meme.find('a').get('href')
                response = requests.get(url, headers = headers)
                soup = BeautifulSoup(response.content, 'html.parser')


                meme = choice(soup.findAll('div', class_ = 'single post s-post-main mb-md bb-mb-el has-post-thumbnail bb-card-item'))
                img = choice(meme.findAll('img')[1:-1]).get('src')
                work = False
            elif search != None:
                result = True
                text = search.replace(' ', '+')
                url = 'https://memepedia.ru/?s=' + text
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 YaBrowser/20.12.3.138 Yowser/2.5 Safari/537.36'
                }
                response = requests.get(url, headers = headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                if soup.findAll('li', class_ = 'post-item post-item-list2') == []:
                    return False
                    break
                meme = soup.findAll('li', class_ = 'post-item post-item-list2')[0]
                url = meme.find('a').get('href')
                response = requests.get(url, headers = headers)
                soup = BeautifulSoup(response.content, 'html.parser')


                meme = choice(soup.findAll('div', class_ = 'single post s-post-main mb-md bb-mb-el has-post-thumbnail bb-card-item'))
                img = choice(meme.findAll('img')[1:-1]).get('src')
                work = False
            else:
                url = 'https://memepedia.ru/memoteka/page/' + str(randint(1, 114)) + '/'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 YaBrowser/20.12.3.138 Yowser/2.5 Safari/537.36'
                }
                response = requests.get(url, headers = headers)
                soup = BeautifulSoup(response.content, 'html.parser')

                meme = choice(soup.findAll('li', class_ = 'post-item post-item-masonry-boxed'))

                url = meme.find('a').get('href')
                response = requests.get(url, headers = headers)
                soup = BeautifulSoup(response.content, 'html.parser')


                meme = choice(soup.findAll('div', class_ = 'js-mediator-article s-post-content s-post-small-el bb-mb-el'))
                img = choice(meme.findAll('img')[:-1]).get('src')
                work = False
        except Exception as e:
            print(str(e) + '\nreload...')
            work = True
    response = requests.get(img, stream = True).raw
    meme_image = Image.open(response)
    meme_image.save('meme.png')
    file = open('meme.png', 'rb')
    return [file, url]
