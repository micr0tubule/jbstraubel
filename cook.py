from global_vars import Food
import random
from PIL import Image, ImageDraw, ImageFont
import discord 
import io
import os 


class Cook: 
    def __init__(self): 
        pass     

    def image(self, food, index):
        filename = {
            Food.CORN_DOG: 'food_images//corndog.jpg',
            Food.BANANA: 'food_images//banana.jpg',
            Food.HAMBURGER: 'food_images//hamburger.jpg',
            Food.CRAZY_HAMBURGER: 'food_images//crazyhamburger.jpg',
            Food.KEBAP: 'food_images//kebap.jpg',
            Food.HOTDOG: 'food_images//hotdog.jpg'
        }.get(food)

        image = Image.open(filename)
        w, h = image.size
        ratio = 100 / w if 100 / h < 101 else 100 / h
        w = int(ratio * w)
        h = int(ratio * h)
        image.thumbnail((w, h))
        image = image.convert('RGBA')

        txt = Image.new('RGBA', image.size, (255, 255, 255, 0))

        file = open('standard.ttf', 'rb')
        font_bytes = io.BytesIO(file.read())
        file.close()
        font = ImageFont.truetype(font_bytes, 40)
        draw = ImageDraw.Draw(txt)
        wtxt, htxt = draw.textsize(str(index), font=font)
        draw.text(((w-wtxt)/2 + 40/47, (h-htxt)/2 + 40/47), str(index), font=font, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))

        image = Image.alpha_composite(image, txt)

        return image

    def name(self, food, kasus, bestimmter_artikel):
        if not bestimmter_artikel:
            if kasus == 'akkusativ':
                return { 
                    Food.CORN_DOG: 'einen Corn Dog',
                    Food.BANANA: 'eine Banane',
                    Food.HAMBURGER: 'einen Hamburger',
                    Food.CRAZY_HAMBURGER: 'einen Crazy Hamburger',
                    Food.KEBAP: 'einen Kebap',
                    Food.HOTDOG: 'einen Hot Dog'
                }.get(food)


    def effect(self, food): 
        return { 
                Food.CORN_DOG: 3,
                    Food.BANANA: 2,
                    Food.HAMBURGER: 4,
                    Food.CRAZY_HAMBURGER: 100,
                    Food.KEBAP: 5,
                    Food.HOTDOG: 5
        }.get(food)

    
    def description(self, food): 
        return {
            Food.CORN_DOG: 'Ein Corn Dog ist ein US-amerikanischer Imbiss.\nEr besteht aus einem Würstchen, das von einer\nMaisteighülle umgeben ist und in heißem Öl\nfrittiert wird.',
            Food.BANANA: 'wohlschmeckende, längliche, gelbe Frucht einer\nbaumähnlichen tropischen Staude',
            Food.HAMBURGER: 'Ein Hamburger ist ein weltweit verbreitetes Sandwich,\ndas aus einem speziellen Brötchen, dem Bun besteht,\ndas mit verschiedenen Belägen, hauptsächlich jedoch einer gegrillten Scheibe aus Rinderhackfleisch, belegt wird.',
            Food.CRAZY_HAMBURGER: 'dasselbe wie ein hamburger aber crazy',
            Food.KEBAP: 'Der Döner Kebab, kurz Döner, ist eines der\nbekanntesten Gerichte der türkischen Küche.\nEr ist dem griechischen Gyros ähnlich. Es besteht\naus mit Marinade gewürzten Fleischscheiben,\ndie schichtweise auf einen senkrecht stehenden\nDrehspieß gesteckt und seitlich gegrillt werden.',
            Food.HOTDOG: 'Der Hotdog ist ein Fast-Food-Gericht, das aus\neiner warmen Brühwurst mit weiteren Zutaten in\neinem weichen Weizenbrötchen besteht.'
        }.get(food)


    def price(self, food): 
        return {
            Food.CORN_DOG: 5,
            Food.BANANA: 2,
            Food.HAMBURGER: 10,
            Food.CRAZY_HAMBURGER: 1000,
            Food.KEBAP: 7,
            Food.HOTDOG: 7
        }.get(food)

    
    def info(self, food): 
        return self.price(food), self.description(food), self.effect(food)
        

    def get_random_food(self, index):
        food = random.choice(list(Food.__dict__.values())[1:-3])
        image = self.image(food, index) 
        return food, image

