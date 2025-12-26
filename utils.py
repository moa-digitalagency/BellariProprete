from PIL import Image, ImageDraw
import random
import os

def generate_random_image(width=600, height=400, filename='generated.jpg'):
    colors = [
        (52, 165, 224), (2, 132, 199), (14, 165, 233), (30, 58, 138),
        (59, 130, 246), (147, 51, 234), (168, 85, 247), (236, 72, 153),
        (249, 115, 22), (34, 197, 94),
    ]
    
    bg_color = random.choice(colors)
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    for _ in range(random.randint(10, 20)):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = x1 + random.randint(50, 200), y1 + random.randint(50, 200)
        shape_color = random.choice(colors)
        draw.rectangle([x1, y1, x2, y2], fill=shape_color, outline=None)
    
    path = os.path.join('static', 'images', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    return f'/static/images/{filename}'

def get_settings():
    from models import SiteSettings
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        from models import db
        db.session.add(settings)
        db.session.commit()
    return settings
