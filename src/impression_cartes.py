# Script d'impression des cartes du jeu
# Génère un PDF prêt à imprimer selon les spécifications du projet

import yaml
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import requests

# Chemins


CARTES_YML = os.path.join(os.path.dirname(__file__), '..', 'cartes.yml')
IMAGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'images')
FONTS_DIR = os.path.join(os.path.dirname(__file__), 'fonts')
ROBOTO_PATH = os.path.join(FONTS_DIR, 'Roboto-Regular.ttf')
ROBOTO_BOLD_PATH = os.path.join(FONTS_DIR, 'Roboto-Bold.ttf')

# Palette de couleurs par groupe
GROUP_COLORS = {
    "Groupe 1": colors.HexColor("#1976d2"),   # Bleu
    "Groupe 2": colors.HexColor("#388e3c"),   # Vert
    "Groupe 3": colors.HexColor("#f57c00"),   # Orange
    "Groupe 4": colors.HexColor("#7b1fa2"),   # Violet
    "Événements": colors.HexColor("#757575"),  # Gris
}

# Dimensions
PAGE_WIDTH, PAGE_HEIGHT = A4
CARD_WIDTH = (PAGE_WIDTH - 40*mm) / 2  # 2 colonnes, marges
CARD_HEIGHT = (PAGE_HEIGHT - 40*mm) / 2  # 2 lignes, marges
CARD_MARGIN_X = 10*mm
CARD_MARGIN_Y = 10*mm
IMAGE_HEIGHT = 50*mm  # Hauteur uniforme pour les images


# Enregistrement des polices locales
def setup_fonts():
    if not os.path.exists(ROBOTO_PATH) or not os.path.exists(ROBOTO_BOLD_PATH):
        raise FileNotFoundError("Les fichiers Roboto-Regular.ttf et Roboto-Bold.ttf doivent être présents dans src/fonts.")
    pdfmetrics.registerFont(TTFont('Roboto', ROBOTO_PATH))
    pdfmetrics.registerFont(TTFont('Roboto-Bold', ROBOTO_BOLD_PATH))

# Lecture des cartes exportables
def read_cartes():
    with open(CARTES_YML, 'r', encoding='utf-8') as f:
        cartes = yaml.safe_load(f)
    return [c for c in cartes if c.get('export', False)]

# Retailler et centrer l'image pour une hauteur uniforme
def process_image(image_path, carte_titre):
    try:
        img = Image.open(image_path)
        w, h = img.size
        scale = IMAGE_HEIGHT / h
        new_w = int(w * scale)
        img = img.resize((new_w, int(IMAGE_HEIGHT)), Image.LANCZOS)
        # Rogner les côtés si trop large
        if new_w > CARD_WIDTH - 20:
            left = (new_w - (CARD_WIDTH - 20)) // 2
            img = img.crop((left, 0, left + int(CARD_WIDTH - 20), int(IMAGE_HEIGHT)))
        return ImageReader(img)
    except Exception as e:
        print(f"[ERREUR IMAGE] Carte '{carte_titre}' : {image_path} -- {e}")
        return None

# Dessiner une carte recto

def draw_recto(c, carte, x, y):
    color = GROUP_COLORS.get(carte['groupe'], colors.black)
    # Fond blanc
    c.setFillColor(colors.white)
    c.rect(x, y, CARD_WIDTH, CARD_HEIGHT, fill=1, stroke=0)
    # Titre
    c.setFont('Roboto-Bold', 16)
    c.setFillColor(color)
    c.drawCentredString(x + CARD_WIDTH/2, y + CARD_HEIGHT - 20, carte['titre'])
    # Image
    img_path = os.path.join(IMAGES_DIR, carte.get('image', ''))
    img = None
    if carte.get('image') and os.path.isfile(img_path):
        img = process_image(img_path, carte['titre'])
    if img:
        c.drawImage(img, x + (CARD_WIDTH - (CARD_WIDTH - 20))/2, y + CARD_HEIGHT/2 - IMAGE_HEIGHT/2, width=CARD_WIDTH-20, height=IMAGE_HEIGHT, preserveAspectRatio=True, mask='auto')
    else:
        print(f"[CARTE IGNORÉE] Carte '{carte['titre']}' : image manquante ou invalide.")
        # Optionnel : dessiner un cadre vide ou une icône placeholder
        c.setStrokeColor(colors.red)
        c.rect(x + (CARD_WIDTH-20)/2, y + CARD_HEIGHT/2 - IMAGE_HEIGHT/2, CARD_WIDTH-20, IMAGE_HEIGHT, fill=0, stroke=1)
    # Groupe
    c.setFont('Roboto-Bold', 14)
    c.setFillColor(color)
    c.drawCentredString(x + CARD_WIDTH/2, y + 25, carte['groupe'])

# Dessiner une carte verso

def draw_verso(c, carte, x, y):
    color = GROUP_COLORS.get(carte['groupe'], colors.black)
    c.setFillColor(colors.white)
    c.rect(x, y, CARD_WIDTH, CARD_HEIGHT, fill=1, stroke=0)
    # Titre
    c.setFont('Roboto-Bold', 16)
    c.setFillColor(color)
    c.drawCentredString(x + CARD_WIDTH/2, y + CARD_HEIGHT - 20, carte['titre'])
    # Description centrée ligne par ligne
    c.setFont('Roboto', 12)
    c.setFillColor(colors.black)
    desc_lines = carte['description'].split('\n')
    start_y = y + CARD_HEIGHT - 50
    line_height = 15
    for i, line in enumerate(desc_lines):
        c.drawCentredString(x + CARD_WIDTH/2, start_y - i * line_height, line)

# Générer le PDF

def generate_pdf(output_path):
    setup_fonts()
    cartes = read_cartes()
    c = canvas.Canvas(output_path, pagesize=A4)
    # Pages recto
    for i in range(0, len(cartes), 4):
        for idx in range(4):
            if i + idx >= len(cartes):
                break
            carte = cartes[i + idx]
            col = idx % 2
            row = idx // 2
            x = CARD_MARGIN_X + col * (CARD_WIDTH + CARD_MARGIN_X)
            y = PAGE_HEIGHT - CARD_MARGIN_Y - (row + 1) * CARD_HEIGHT - row * CARD_MARGIN_Y
            draw_recto(c, carte, x, y)
        c.showPage()
    # Pages verso
    for i in range(0, len(cartes), 4):
        for idx in range(4):
            if i + idx >= len(cartes):
                break
            carte = cartes[i + idx]
            col = idx % 2
            row = idx // 2
            x = CARD_MARGIN_X + col * (CARD_WIDTH + CARD_MARGIN_X)
            y = PAGE_HEIGHT - CARD_MARGIN_Y - (row + 1) * CARD_HEIGHT - row * CARD_MARGIN_Y
            draw_verso(c, carte, x, y)
        c.showPage()
    c.save()
    print(f"PDF généré : {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Génère le PDF d'impression des cartes du jeu.")
    parser.add_argument("-o", "--output", default="cartes-impression.pdf", help="Chemin du PDF de sortie")
    args = parser.parse_args()
    output_path = os.path.abspath(args.output)
    generate_pdf(output_path)
