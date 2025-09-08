# Script d'impression des cartes du jeu
# Génère un PDF prêt à imprimer selon les spécifications du projet

import yaml
import os
from reportlab.lib.pagesizes import A4, landscape
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
PAGE_WIDTH, PAGE_HEIGHT = landscape(A4)
CARD_WIDTH = PAGE_WIDTH / 2
CARD_HEIGHT = PAGE_HEIGHT / 2
CARD_MARGIN_X = 0
CARD_MARGIN_Y = 0
IMAGE_HEIGHT = CARD_HEIGHT * 0.5  # Hauteur uniforme pour les images


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
    color = GROUP_COLORS.get(carte.get('groupe', ''), colors.black)
    c.setFillColor(colors.white)
    # Cartes question : rendu spécifique
    if carte.get('type') == 'question':
        # Bordure extérieure couleur du groupe
        c.setStrokeColor(color)
        c.setLineWidth(4)
        c.rect(x, y, CARD_WIDTH, CARD_HEIGHT, fill=1, stroke=1)
        # Titre centré, police plus grande
        c.setFont('Roboto-Bold', 22)
        c.setFillColor(color)
        c.drawCentredString(x + CARD_WIDTH/2, y + CARD_HEIGHT/2 + 20, carte['titre'])
        # Texte de la question (si présent)
        if carte.get('question'):
            c.setFont('Roboto', 14)
            c.setFillColor(colors.black)
            c.drawCentredString(x + CARD_WIDTH/2, y + CARD_HEIGHT/2 - 10, carte['question'])
        # Groupe en bas
        c.setFont('Roboto-Bold', 14)
        c.setFillColor(color)
        c.drawCentredString(x + CARD_WIDTH/2, y + 25, carte.get('groupe', ''))
    else:
        # Action : rendu classique
        c.rect(x, y, CARD_WIDTH, CARD_HEIGHT, fill=1, stroke=0)
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
            c.setStrokeColor(colors.red)
            c.rect(x + (CARD_WIDTH-20)/2, y + CARD_HEIGHT/2 - IMAGE_HEIGHT/2, CARD_WIDTH-20, IMAGE_HEIGHT, fill=0, stroke=1)
        # Groupe
        c.setFont('Roboto-Bold', 14)
        c.setFillColor(color)
        c.drawCentredString(x + CARD_WIDTH/2, y + 25, carte.get('groupe', ''))

# Dessiner une carte verso

def draw_verso(c, carte, x, y):
    color = GROUP_COLORS.get(carte.get('groupe', ''), colors.black)
    c.setFillColor(colors.white)
    if carte.get('type') == 'question':
        # Bordure extérieure couleur du groupe
        c.setStrokeColor(color)
        c.setLineWidth(4)
        c.rect(x, y, CARD_WIDTH, CARD_HEIGHT, fill=1, stroke=1)
        # Titre centré, police plus grande
        c.setFont('Roboto-Bold', 20)
        c.setFillColor(color)
        c.drawCentredString(x + CARD_WIDTH/2, y + CARD_HEIGHT - 40, carte['titre'])
        # Réponse (si présente)
        if carte.get('reponse'):
            c.setFont('Roboto', 14)
            c.setFillColor(colors.black)
            c.drawCentredString(x + CARD_WIDTH/2, y + CARD_HEIGHT/2, carte['reponse'])
        # Groupe en bas
        c.setFont('Roboto-Bold', 14)
        c.setFillColor(color)
        c.drawCentredString(x + CARD_WIDTH/2, y + 25, carte.get('groupe', ''))
    else:
        c.rect(x, y, CARD_WIDTH, CARD_HEIGHT, fill=1, stroke=0)
        c.setFont('Roboto-Bold', 16)
        c.setFillColor(color)
        c.drawCentredString(x + CARD_WIDTH/2, y + CARD_HEIGHT - 20, carte['titre'])
        c.setFont('Roboto', 12)
        c.setFillColor(colors.black)
        desc_lines = carte.get('description', '').split('\n')
        start_y = y + CARD_HEIGHT - 50
        line_height = 15
        max_lines = int((CARD_HEIGHT - 70) // line_height)
        for i, line in enumerate(desc_lines[:max_lines]):
            max_chars = int(CARD_WIDTH // 7)
            if len(line) > max_chars:
                line = line[:max_chars-3] + '...'
            c.drawCentredString(x + CARD_WIDTH/2, start_y - i * line_height, line)

# Lignes de découpe

def draw_guides(c):
    # Ligne verticale
    c.setStrokeColorRGB(0.5, 0.5, 0.5)
    c.setLineWidth(1)
    c.line(PAGE_WIDTH/2, 0, PAGE_WIDTH/2, PAGE_HEIGHT)
    # Ligne horizontale
    c.line(0, PAGE_HEIGHT/2, PAGE_WIDTH, PAGE_HEIGHT/2)

# Générer le PDF

def generate_pdf(output_path):
    setup_fonts()
    cartes = read_cartes()
    c = canvas.Canvas(output_path, pagesize=landscape(A4))
    # Pages recto/verso enchaînées strictement
    for i in range(0, len(cartes), 4):
        # Rectos (ordre naturel)
        for idx in range(4):
            if i + idx >= len(cartes):
                continue
            carte = cartes[i + idx]
            col = idx % 2
            row = idx // 2
            x = col * CARD_WIDTH
            y = PAGE_HEIGHT - (row + 1) * CARD_HEIGHT
            draw_recto(c, carte, x, y)
        draw_guides(c)
        c.showPage()
        # Versos (inversion des colonnes)
        # Mapping: [0,1,2,3] -> [1,0,3,2]
        verso_order = [1,0,3,2]
        for pos, idx in enumerate(verso_order):
            if i + idx >= len(cartes):
                continue
            carte = cartes[i + idx]
            col = pos % 2
            row = pos // 2
            x = col * CARD_WIDTH
            y = PAGE_HEIGHT - (row + 1) * CARD_HEIGHT
            draw_verso(c, carte, x, y)
        draw_guides(c)
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
