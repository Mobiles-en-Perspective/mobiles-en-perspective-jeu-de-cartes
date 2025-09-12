# Découpe une ligne en segments (texte normal/gras) selon les balises **...**
import re

# Permet le gras sur plusieurs lignes (contexte persistant)
def parse_bold_segments_multiline(lines):
    # lines: liste de lignes (word-wrappées)
    # Retourne une liste de listes de segments (texte, is_bold) pour chaque ligne
    segments_per_line = []
    bold_open = False
    for line in lines:
        segs = []
        i = 0
        buf = ''
        while i < len(line):
            if line[i:i+2] == '**':
                if buf:
                    segs.append((buf, bold_open))
                    buf = ''
                bold_open = not bold_open
                i += 2
            else:
                buf += line[i]
                i += 1
        if buf or not segs:
            segs.append((buf, bold_open))
        segments_per_line.append(segs)
    return segments_per_line
from reportlab.pdfbase.pdfmetrics import stringWidth
# Utilitaire pour couper le texte en lignes qui tiennent dans la largeur max
def wrap_text(text, font_name, font_size, max_width):
    words = text.split()
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + (' ' if current_line else '') + word
        if stringWidth(test_line, font_name, font_size) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines
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
    carte_type = carte.get('type')
    if carte_type == 'question':
        # Bordure extérieure couleur du groupe
        c.setStrokeColor(color)
        c.setLineWidth(4)
        c.rect(x, y, CARD_WIDTH, CARD_HEIGHT, fill=1, stroke=1)
        # Titre centré, police plus grande, word wrap
        c.setFont('Roboto-Bold', 22)
        c.setFillColor(color)
        title_lines = wrap_text(carte['titre'], 'Roboto-Bold', 22, CARD_WIDTH-30)
        title_y = y + CARD_HEIGHT/2 + 30
        for line in title_lines:
            c.drawCentredString(x + CARD_WIDTH/2, title_y, line)
            title_y -= 26
        # Texte de la question (si présent, word wrap)
        if carte.get('question'):
            c.setFont('Roboto', 14)
            c.setFillColor(colors.black)
            question_lines = wrap_text(carte['question'], 'Roboto', 14, CARD_WIDTH-30)
            q_y = title_y - 10
            for line in question_lines:
                c.drawCentredString(x + CARD_WIDTH/2, q_y, line)
                q_y -= 18
        # Groupe en bas
        c.setFont('Roboto-Bold', 14)
        c.setFillColor(color)
        c.drawCentredString(x + CARD_WIDTH/2, y + 25, carte.get('groupe', ''))
    elif carte_type in ('jeu', 'reponse'):
        # Rendu classique (ex-action)
        c.rect(x, y, CARD_WIDTH, CARD_HEIGHT, fill=1, stroke=0)
        # Titre word wrap
        c.setFont('Roboto-Bold', 16)
        c.setFillColor(color)
        title_lines = wrap_text(carte['titre'], 'Roboto-Bold', 16, CARD_WIDTH-30)
        title_y = y + CARD_HEIGHT - 20
        for line in title_lines:
            c.drawCentredString(x + CARD_WIDTH/2, title_y, line)
            title_y -= 18
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
    else:
        # Type inconnu : on affiche un cadre rouge
        c.setStrokeColor(colors.red)
        c.setLineWidth(2)
        c.rect(x, y, CARD_WIDTH, CARD_HEIGHT, fill=0, stroke=1)
        c.setFont('Roboto-Bold', 14)
        c.setFillColor(colors.red)
        c.drawCentredString(x + CARD_WIDTH/2, y + CARD_HEIGHT/2, f"Type inconnu: {carte_type}")

# Dessiner une carte verso

def draw_verso(c, carte, x, y):
    color = GROUP_COLORS.get(carte.get('groupe', ''), colors.black)
    c.setFillColor(colors.white)
    carte_type = carte.get('type')
    if carte_type == 'question':
        # Bordure extérieure couleur du groupe
        c.setStrokeColor(color)
        c.setLineWidth(4)
        c.rect(x, y, CARD_WIDTH, CARD_HEIGHT, fill=1, stroke=1)
        # Grand point d'interrogation centré, couleur du groupe
        question_mark = "?"
        # Taille dynamique : occupe ~60% de la hauteur de la carte
        font_size = int(CARD_HEIGHT * 0.6)
        c.setFont('Roboto-Bold', font_size)
        c.setFillColor(color)
        # Mesure la largeur du ? pour centrage
        qm_width = stringWidth(question_mark, 'Roboto-Bold', font_size)
        qm_x = x + (CARD_WIDTH - qm_width) / 2
        qm_y = y + (CARD_HEIGHT - font_size) / 2 + font_size * 0.15  # ajustement vertical
        c.drawString(qm_x, qm_y, question_mark)
        # Groupe en bas
        c.setFont('Roboto-Bold', 14)
        c.setFillColor(color)
        c.drawCentredString(x + CARD_WIDTH/2, y + 25, carte.get('groupe', ''))
    elif carte_type in ('jeu', 'reponse'):
        c.rect(x, y, CARD_WIDTH, CARD_HEIGHT, fill=1, stroke=0)
        # Titre word wrap
        c.setFont('Roboto-Bold', 16)
        c.setFillColor(color)
        title_lines = wrap_text(carte['titre'], 'Roboto-Bold', 16, CARD_WIDTH-30)
        title_y = y + CARD_HEIGHT - 20
        for line in title_lines:
            c.drawCentredString(x + CARD_WIDTH/2, title_y, line)
            title_y -= 18
        # Description word wrap, centrée verticalement et alignée à gauche
        c.setFont('Roboto', 12)
        c.setFillColor(colors.black)
        # Gestion multilignes et gras Markdown (**...**)
        desc = carte.get('description', '')
        # Découpe en paragraphes puis en lignes wrap (en gardant les **)
        desc_lines = []
        for para in desc.split('\n'):
            para = para.strip()
            if not para:
                desc_lines.append('')
                continue
            lines = wrap_text(para, 'Roboto', 12, CARD_WIDTH-30)
            desc_lines.extend(lines)
        line_height = 15
        max_lines = int((CARD_HEIGHT - 70) // line_height)
        desc_lines = desc_lines[:max_lines]
        block_height = len(desc_lines) * line_height
        # Centrage vertical
        start_y = y + (CARD_HEIGHT - block_height) / 2 + block_height - line_height/2
        # Nouveau : parsing bold multi-ligne
        segments_per_line = parse_bold_segments_multiline(desc_lines)
        for i, segs in enumerate(segments_per_line):
            y_pos = start_y - i * line_height
            x_pos = x + 15
            for text, is_bold in segs:
                if not text:
                    continue
                font = 'Roboto-Bold' if is_bold else 'Roboto'
                c.setFont(font, 12)
                c.drawString(x_pos, y_pos, text)
                x_pos += stringWidth(text, font, 12)
    else:
        # Type inconnu : cadre rouge
        c.setStrokeColor(colors.red)
        c.setLineWidth(2)
        c.rect(x, y, CARD_WIDTH, CARD_HEIGHT, fill=0, stroke=1)
        c.setFont('Roboto-Bold', 14)
        c.setFillColor(colors.red)
        c.drawCentredString(x + CARD_WIDTH/2, y + CARD_HEIGHT/2, f"Type inconnu: {carte_type}")

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
