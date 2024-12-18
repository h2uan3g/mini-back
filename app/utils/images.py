import random

from PIL import Image, ImageFont, ImageDraw, ImageFilter


def get_random_color():
    return random.randint(0, 255), \
        random.randint(0, 255), random.randint(0, 255)


def generate_image(length):
    code_ku = 'abcdefg1234567890ABCDEFG'
    image = Image.new('RGB', (120, 60), color=get_random_color())
    font = ImageFont.load_default(size=35)
    draw = ImageDraw.Draw(image)
    code = ''
    for i in range(length):
        c = random.choice(code_ku)
        code += c
        draw.text((5 + random.randint(4, 7) + 25 * i, random.randint(4, 7)),
                  text=c, fill=get_random_color(), font=font)
    image = image.filter(ImageFilter.EDGE_ENHANCE)
    return image, code
