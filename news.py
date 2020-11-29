from commands import communicator
from threading import Thread
from global_vars import Message
from global_vars import NEWS_TIME
from storage import storage
from bs4 import BeautifulSoup
import time 
import discord
import pandas 
import requests

class Postman:
    def __init__(self, client):
        self.client_reference = client
    
    def start(self): 
        self.channel = discord.utils.get(self.client_reference.guilds[0].channels, name='hacker-news')
        self.update_thread = Thread(target=self.update)
        self.update_thread.start()
        print('postman is posting..')


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
            time.sleep(NEWS_TIME)

    
    