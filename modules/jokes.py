from bs4 import BeautifulSoup as BS
import requests, random


def get_jokes():
    jokeurl = 'http://www.santabanta.com/jokes/'
    res = requests.get(jokeurl)
    soup = BS(res.text, 'html.parser')
    result = soup.find_all('td')
    return random.choice(result).text


def get_memes():
    memeurl = 'http://www.quickmeme.com/'
    res = requests.get(memeurl)
    soup = BS(res.text,'html.parser')
    result = [x['src'] for x in soup.findAll('img', {'class': 'post-image'})]
    file = open('meme.png','wb')
    res = requests.get(random.choice(result))
    for i in res.iter_content(1000):
        file.write(i)
    file.close()
    return "done"