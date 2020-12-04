import discord
import os 
from PIL import Image, ImageDraw, ImageFont
from image_processing.standard import scale, number
from global_vars import Food as FoodCats
from global_vars import Possession as PossessionCats

class Item: 
    def __init__(self, objId, price, image_file, image_url, info): 
        self.objId = objId
        self.price = price
        self.image_file = image_file
        self.image_url=image_url
        self.info = info
    
    def get_image(self, num=None):
        cwd = os.getcwd() + '/' 
        image = Image.open(cwd+self.image_file)
        image = scale(image)
        print(num)
        if num or num == 0: 
            image = number(image, num)
        return image
    
    def get_name(self): 
        return {
            FoodCats.BANANA: 'Banane',
            FoodCats.CORN_DOG: 'Corn Dog',
            FoodCats.HAMBURGER: 'Hamburger', 
            FoodCats.CRAZY_HAMBURGER: 'Crazy Hamburger',
            FoodCats.KEBAP: 'Kebap',
            FoodCats.HOTDOG: 'Hotdog',
            FoodCats.ROASTED_ALMONDS: 'Gebrannte Mandeln',
            FoodCats.CHILDREN_TEA: 'Kinder Punsch',
            FoodCats.BAKED_APPLE: 'Bratapfel',
            FoodCats.CANDIED_APPLE: 'Kandierter Apfel'
        }.get(self.objId, 'Penis')
    
    def get_info(self): 
        pass 


class Food(Item): 
    def __init__(self, objId, price, image_file, image_url, info, effectivity): 
        super().__init__(objId, price, image_file, image_url, info)
        self.effectivity = effectivity
        self.icon = '🍔'
    
    def get_info(self): 
        embed=discord.Embed(color=0xffc800)
        embed.set_thumbnail(url=self.image_url)
        embed.add_field(name=self.get_name(), value=self.info, inline=False)
        embed.add_field(name="Effektivität", value=self.effectivity, inline=True)
        embed.add_field(name="Preis", value=f'{self.price}$', inline=True)
        return embed


class Banana(Food): 
    def __init__(self): 
        super().__init__(
            objId=FoodCats.BANANA,
            price=5, 
            image_file='food_images/banana.jpg',
            image_url='https://cdn.discordapp.com/attachments/781530450577457193/783389781890433074/image.png',
            info='wohlschmeckende, längliche, gelbe Frucht einer baumähnlichen tropischen Staude',
            effectivity=5)
        self.name = 'Banane'

class Corndog(Food): 
    def __init__(self): 
        super().__init__(
            objId=FoodCats.CORN_DOG,
            price=5, 
            image_file='food_images/corndog.jpg',
            image_url='https://cdn.discordapp.com/attachments/781530450577457193/783389811301417050/image.png',
            info='Ein Corn Dog ist ein US-amerikanischer Imbiss. Er besteht aus einem Würstchen, das von einer\nMaisteighülle umgeben ist und in heißem Öl\nfrittiert wird.',
            effectivity=5)
        self.name = 'Corn Dog'

class Hamburger(Food): 
    def __init__(self): 
        super().__init__(
            objId=FoodCats.HAMBURGER,
            price=5, 
            image_file='food_images/hamburger.jpg',
            image_url='https://cdn.discordapp.com/attachments/781530450577457193/783389848890638376/image.png',
            info='Ein Hamburger ist ein weltweit verbreitetes Sandwich, das aus einem speziellen Brötchen, dem Bun besteht, das mit verschiedenen Belägen, hauptsächlich jedoch einer gegrillten Scheibe aus Rinderhackfleisch, belegt wird.',
            effectivity=5)
        self.name = 'Hamburger'

class CrazyHamburger(Food): 
    def __init__(self): 
        super().__init__(
            objId=FoodCats.CRAZY_HAMBURGER,
            price=1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, 
            image_file='food_images/crazyhamburger.jpg',
            image_url='https://cdn.discordapp.com/attachments/781530450577457193/783389780049264700/image.png',
            info='dasselbe wie ein hamburger aber crazy',
            effectivity=5000000000000000000000)
        self.name = 'Crazy Hamburger'

class Kebap(Food): 
    def __init__(self): 
        super().__init__(
            objId=FoodCats.KEBAP,
            price=4.99, 
            image_file='food_images/kebap.jpg',
            image_url='https://cdn.discordapp.com/attachments/781530450577457193/783391231098224640/image.png',
            info='Der Döner Kebab, kurz Döner, ist eines der\nbekanntesten Gerichte der türkischen Küche. Er ist dem griechischen Gyros ähnlich. Es besteht aus mit Marinade gewürzten Fleischscheiben, die schichtweise auf einen senkrecht stehenden Drehspieß gesteckt und seitlich gegrillt werden.',
            effectivity=5)
        self.name = 'Kebap'

class Hotdog(Food): 
    def __init__(self): 
        super().__init__(
            objId=FoodCats.HOTDOG,
            price=8.99, 
            image_file='food_images/hotdog.jpg',
            image_url='https://cdn.discordapp.com/attachments/781530450577457193/783389813985378314/image.png',
            info='Der Hotdog ist ein Fast-Food-Gericht, das aus einer warmen Brühwurst mit weiteren Zutaten in einem weichen Weizenbrötchen besteht.',
            effectivity=5)
        self.name = 'Hotdog'

class RoastedAlmonds(Food): 
    def __init__(self): 
        super().__init__(
            objId=FoodCats.ROASTED_ALMONDS,
            price=2.99,
            image_file='food_images/roastedalmonds.jpg',
            image_url='https://cdn.discordapp.com/attachments/768869575314898964/783454521774964746/image.png',
            info='Gebrannte Mandeln sind eine Süßware, die – neben Zuckerwatte und Magenbrot – besonders häufig auf Jahrmärkten sowie Volksfesten (Kirmes) verkauft wird.',
            effectivity=10)
        self.name = 'Gebrannte Mandeln'

class ChildrenTea(Food): 
    def __init__(self): 
        super().__init__(
            objId=FoodCats.CHILDREN_TEA,
            price=1.50, 
            image_file='food_images/childrentea.jpg',
            image_url='https://cdn.discordapp.com/attachments/783405443409379380/783463109024022568/image.png',
            info='Als Punsch (nach Hindi पांच pāñč „fünf“) wird ein alkoholisches, meist heißes Mischgetränk bezeichnet, das ursprünglich aus Indien stammt und aus fünf Zutaten (daher der Name) besteht. Die traditionellen Zutaten sind Arrak, Zucker, Zitronen und Tee oder Wasser mit Gewürzen.',
            effectivity=5)
        self.name = 'Kinderpunsch'

class BakedApple(Food): 
    def __init__(self): 
        super().__init__(
            objId=FoodCats.BAKED_APPLE, 
            price=2, 
            image_file='food_images/bratapfel.jpg',
            image_url='https://cdn.discordapp.com/attachments/783405443409379380/783467560338849842/image.png',
            info='Bratäpfel sind eine einfache Süßspeise aus im Ofen gebackenen Äpfeln. Sie werden traditionell im Winter zur Weihnachtszeit aus lagerfähigen, festen und säuerlichen Apfelsorten wie Boskoop zubereitet.',
            effectivity=7)
        self.name = 'Bratapfel'

class CandiedApple(Food): 
    def __init__(self): 
        super().__init__(
            objId=FoodCats.CANDIED_APPLE, 
            price=2,
            image_file='food_images/kandierterapfel.jpg',
            image_url='https://cdn.gutekueche.de/upload/rezept/2217/kandierte-aepfel.jpg',
            info='Kandieren (auch Konfieren) ist eine Konservierungsmethode für frische, essbare Pflanzenteile (meist Früchte und Obst), bei denen der Zuckergehalt der Früchte auf mindestens 70 Prozent erhöht und der Wassergehalt reduziert wird.',
            effectivity=6)
        self.name = 'kandierter Apfel'

    
class Possession(Item): 
    def __init__(self, objId, price, image_file, image_url, info, user_id):
        super().__init__(objId, price, image_file, image_url, info)
        self.user_id = user_id
        self.icon = '🏠'

class House(Possession): 
    def __init__(self, item): 
        super().__init__(
            objId=PossessionCats.HOUSE,
            price=5,
            image_file='food_images/haus.jpg',
            image_url='https://www.hanse-haus.de/fileadmin/_processed_/7/b/csm_fertighaus-bauen-startseiten-bild_d13e0ec91d.jpg',
            info='Als Haus bezeichnet man ein Gebäude in der Regel, wenn dessen vorrangiger Zweck ist, Menschen regelmäßig als Unterkunft zu dienen, insbesondere zum Wohnen, Arbeiten oder für Zusammenkünfte.',
            user_id=item.user_id.val)
        self.name = 'Haus'