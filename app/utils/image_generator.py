from PIL import Image, ImageDraw, ImageFont
import random
import os

def generate_random_image(width=600, height=400, filename='generated.jpg'):
    """Generate a random colorful image"""
    colors = [
        (52, 165, 224),   # Light blue
        (2, 132, 199),    # Medium blue
        (14, 165, 233),   # Sky blue
        (30, 58, 138),    # Dark blue
        (59, 130, 246),   # Vibrant blue
        (147, 51, 234),   # Purple
        (168, 85, 247),   # Light purple
        (236, 72, 153),   # Pink
        (249, 115, 22),   # Orange
        (34, 197, 94),    # Green
    ]
    
    bg_color = random.choice(colors)
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    for _ in range(random.randint(10, 20)):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = x1 + random.randint(50, 200)
        y2 = y1 + random.randint(50, 200)
        shape_color = random.choice(colors)
        draw.rectangle([x1, y1, x2, y2], fill=shape_color, outline=None)
    
    path = os.path.join('static', 'images', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    return f'/static/images/{filename}'

def generate_cleaning_image(service_type='general', filename='cleaning.jpg'):
    """Generate service-specific cleaning images"""
    width, height = 600, 400
    
    service_colors = {
        'chantier': [(52, 165, 224), (149, 165, 166), (108, 117, 125)],
        'fin_chantier': [(14, 165, 233), (79, 172, 254), (191, 219, 254)],
        'entretien': [(34, 197, 94), (134, 239, 172), (220, 252, 231)],
        'villa': [(236, 72, 153), (245, 158, 194), (253, 205, 225)],
        'appartement': [(59, 130, 246), (147, 197, 253), (219, 234, 254)],
        'vitres': [(168, 85, 247), (217, 70, 239), (245, 158, 211)],
    }
    
    colors = service_colors.get(service_type, service_colors['general'])
    
    img = Image.new('RGB', (width, height), color=colors[0])
    draw = ImageDraw.Draw(img)
    
    for i in range(5):
        x = i * (width // 5)
        y = random.randint(0, height // 2)
        draw.rectangle([x, y, x + width // 6, y + height // 3], fill=colors[1 % len(colors)], outline=None)
    
    draw.ellipse([width // 4, height // 4, 3 * width // 4, 3 * height // 4], fill=colors[2 % len(colors)])
    
    path = os.path.join('static', 'images', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    return f'/static/images/{filename}'
