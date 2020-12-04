from PIL import Image, ImageDraw, ImageFont
import io
import pathlib

def scale(image): 
    w, h = image.size
    ratio = 100 / w if 100 / h < 101 else 100 / h
    w = int(ratio * w)
    h = int(ratio * h)
    image.thumbnail((w, h))
    return image

def number(image, num):
    path = str(pathlib.Path(__file__).parent.absolute()) + '/'
    w, h = image.size
    image = image.convert('RGBA')
    font_file = open(path+'standard.ttf', 'rb')
    font_bytes = io.BytesIO(font_file.read())
    font_file.close()
    txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
    font = ImageFont.truetype(font_bytes, 40)
    draw = ImageDraw.Draw(txt)
    wtxt, htxt = draw.textsize(str(num), font=font)
    draw.text(((w-wtxt)/2 + 40/47, (h-htxt)/2 + 40/47), str(num), font=font, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
    image = Image.alpha_composite(image, txt)
    return image


