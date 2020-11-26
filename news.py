import requests
from bs4 import BeautifulSoup
from commands import communicator
from threading import Thread
from global_vars import Message
import time 
import pandas 
from storage import storage


class Postman:
    def __init__(self, channel):
        self.channel = channel
    
    def start(self): 
        self.update_thread = Thread(target=self.update)
        self.update_thread.start()

    def toparticle(self):
        html = requests.get('https://news.ycombinator.com/news?p=1').text
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.findAll("a", {"class": "storylink"})[0]
        if not self.isposted(article):
            storage.insert_new_article(article.attrs['href'])
            return article
        else: 
            False

    def isposted(self, article):
        for article_ in storage.articles: 
            if article_.href.val == article.attrs['href']:
                return True
        return False

    def update(self): 
        while True:
            article = self.toparticle()
            if article: 
                communicator.append(Message(content=article.attrs['href'], channel=self.channel))
            time.sleep(0.5)

    
    