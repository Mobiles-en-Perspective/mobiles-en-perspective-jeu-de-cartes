#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'impression de l'affiche de présentation du jeu "Mobiles en Perspective"
Génère une affiche A3 avec logo, présentation, QR codes et licence
"""

import os
import re
import argparse
import requests
from io import BytesIO

from reportlab.lib.pagesizes import A3, portrait
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

import qrcode
from PIL import Image

# Chemins
SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.join(SCRIPT_DIR, '..')
README_PATH = os.path.join(PROJECT_DIR, 'README.md')
IMAGES_DIR = os.path.join(PROJECT_DIR, 'images')
FONTS_DIR = os.path.join(SCRIPT_DIR, 'fonts')
ROBOTO_PATH = os.path.join(FONTS_DIR, 'Roboto-Regular.ttf')
ROBOTO_BOLD_PATH = os.path.join(FONTS_DIR, 'Roboto-Bold.ttf')

# URLs
LOGO_URL = "https://avatars.githubusercontent.com/u/228016686?s=200&v=4"
CC_BY_LOGO_URL = "https://i.creativecommons.org/l/by/4.0/88x31.png"

# Chemins des images téléchargées
LOGO_PATH = os.path.join(IMAGES_DIR, 'logo.png')
CC_BY_LOGO_PATH = os.path.join(IMAGES_DIR, 'cc-by.png')

# Dimensions A3
PAGE_WIDTH, PAGE_HEIGHT = portrait(A3)
MARGIN = 20 * mm
CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN
CONTENT_HEIGHT = PAGE_HEIGHT - 2 * MARGIN

# QR Codes
QR_SIZE = 60 * mm
QR_SPACING_H = 20 * mm
QR_SPACING_V = 20 * mm
QR_LABEL_SPACING = 5 * mm

# Couleurs (mêmes que les groupes de cartes)
COLOR_BLUE = colors.HexColor("#1976d2")
COLOR_GREEN = colors.HexColor("#388e3c")
COLOR_ORANGE = colors.HexColor("#f57c00")
COLOR_PURPLE = colors.HexColor("#7b1fa2")
COLOR_DARK_GRAY = colors.HexColor("#333333")
COLOR_GRAY = colors.HexColor("#666666")


def setup_fonts():
    """Enregistre les polices Roboto pour utilisation dans le PDF"""
    if not os.path.exists(ROBOTO_PATH) or not os.path.exists(ROBOTO_BOLD_PATH):
        raise FileNotFoundError(
            "Les fichiers Roboto-Regular.ttf et Roboto-Bold.ttf doivent être présents dans src/fonts."
        )
    pdfmetrics.registerFont(TTFont('Roboto', ROBOTO_PATH))
    pdfmetrics.registerFont(TTFont('Roboto-Bold', ROBOTO_BOLD_PATH))


def download_image(url, save_path):
    """
    Télécharge une image depuis une URL et la sauvegarde localement
    
    Args:
        url: URL de l'image à télécharger
        save_path: Chemin où sauvegarder l'image
    
    Returns:
        True si le téléchargement a réussi, False sinon
    """
    try:
        print(f"Téléchargement de {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Créer le dossier images s'il n'existe pas
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Sauvegarder l'image
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Image sauvegardée dans {save_path}")
        return True
    except Exception as e:
        print(f"[ERREUR] Impossible de télécharger {url}: {e}")
        return False


def read_presentation():
    """
    Lit la section "Présentation du jeu" depuis le README.md
    
    Returns:
        Le texte de présentation ou None si introuvable
    """
    try:
        with open(README_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraire la section "Présentation du jeu"
        match = re.search(
            r'## Présentation du jeu\s*\n\s*\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL
        )
        
        if match:
            presentation = match.group(1).strip()
            return presentation
        else:
            print("[ERREUR] Section 'Présentation du jeu' introuvable dans README.md")
            return None
    except Exception as e:
        print(f"[ERREUR] Impossible de lire {README_PATH}: {e}")
        return None


def generate_qr_code(url, size_mm):
    """
    Génère un QR code pour une URL donnée
    
    Args:
        url: URL à encoder dans le QR code
        size_mm: Taille du QR code en millimètres
    
    Returns:
        ImageReader du QR code ou None si erreur
    """
    try:
        # Calculer la taille en pixels (300 DPI pour impression)
        size_pixels = int(size_mm * 300 / 25.4)
        
        qr = qrcode.QRCode(
            version=None,  # Automatique
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # Haute correction d'erreur
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((size_pixels, size_pixels), Image.LANCZOS)
        
        return ImageReader(img)
    except Exception as e:
        print(f"[ERREUR] Impossible de générer le QR code pour {url}: {e}")
        return None


def wrap_text(text, font_name, font_size, max_width):
    """
    Découpe le texte en lignes qui tiennent dans la largeur max
    
    Args:
        text: Texte à découper
        font_name: Nom de la police
        font_size: Taille de la police
        max_width: Largeur maximale en points
    
    Returns:
        Liste de lignes
    """
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


def draw_header(c, y_start):
    """
    Dessine l'en-tête avec logo, titre et sous-titre
    
    Args:
        c: Canvas ReportLab
        y_start: Position Y de départ
    
    Returns:
        Position Y après l'en-tête
    """
    y = y_start
    
    # Logo
    if os.path.exists(LOGO_PATH):
        try:
            logo = ImageReader(LOGO_PATH)
            logo_size = 80 * mm
            x_logo = MARGIN + (CONTENT_WIDTH - logo_size) / 2
            c.drawImage(logo, x_logo, y - logo_size, width=logo_size, height=logo_size, preserveAspectRatio=True, mask='auto')
            y -= logo_size + 10 * mm
        except Exception as e:
            print(f"[ERREUR] Impossible d'afficher le logo: {e}")
    else:
        print(f"[AVERTISSEMENT] Logo introuvable à {LOGO_PATH}")
    
    # Titre principal
    c.setFont('Roboto-Bold', 28)
    c.setFillColor(colors.black)
    c.drawCentredString(PAGE_WIDTH / 2, y, "Mobiles en Perspective")
    y -= 35
    
    # Sous-titre
    c.setFont('Roboto', 18)
    c.setFillColor(COLOR_DARK_GRAY)
    subtitle = "Quels impacts sociaux et environnementaux ont nos smartphones ?"
    
    # Word wrap du sous-titre si nécessaire
    subtitle_lines = wrap_text(subtitle, 'Roboto', 18, CONTENT_WIDTH - 40 * mm)
    for line in subtitle_lines:
        c.drawCentredString(PAGE_WIDTH / 2, y, line)
        y -= 22
    
    y -= 10 * mm
    return y


def draw_presentation(c, y_start, presentation_text):
    """
    Dessine le texte de présentation
    
    Args:
        c: Canvas ReportLab
        y_start: Position Y de départ
        presentation_text: Texte de la présentation
    
    Returns:
        Position Y après le texte
    """
    if not presentation_text:
        return y_start
    
    y = y_start
    c.setFont('Roboto', 12)
    c.setFillColor(colors.black)
    
    # Marges internes pour le texte
    text_margin = 15 * mm
    text_width = CONTENT_WIDTH - 2 * text_margin
    
    # Diviser en paragraphes
    paragraphs = presentation_text.split('\n\n')
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        # Gérer les listes à puces
        if para.startswith('*'):
            # Liste à puces
            items = [item.strip()[1:].strip() for item in para.split('\n') if item.strip().startswith('*')]
            for item in items:
                lines = wrap_text(item, 'Roboto', 12, text_width - 10 * mm)
                for i, line in enumerate(lines):
                    if i == 0:
                        c.drawString(MARGIN + text_margin, y, "•")
                        c.drawString(MARGIN + text_margin + 5 * mm, y, line)
                    else:
                        c.drawString(MARGIN + text_margin + 5 * mm, y, line)
                    y -= 16
            y -= 5  # Espace après la liste
        else:
            # Paragraphe normal
            lines = wrap_text(para, 'Roboto', 12, text_width)
            for line in lines:
                c.drawString(MARGIN + text_margin, y, line)
                y -= 16
            y -= 8  # Espace entre paragraphes
    
    return y


def draw_qr_codes(c, y_start):
    """
    Dessine la grille de 4 QR codes avec leurs labels
    
    Args:
        c: Canvas ReportLab
        y_start: Position Y de départ (coin supérieur gauche du premier QR)
    
    Returns:
        Position Y après les QR codes
    """
    qr_codes_data = [
        {
            'url': 'https://openfeedback.io/devfestnantes2025/2025-10-16/mobilesenperspectivequelsimpactssociauxetenvironnementauxontnoss',
            'label': 'Donnez-nous votre feedback !',
            'color': COLOR_BLUE
        },
        {
            'url': 'https://github.com/Mobiles-en-Perspective/mobiles-en-perspective-jeu-de-cartes',
            'label': 'Consulter le code source',
            'color': COLOR_GREEN
        },
        {
            'url': 'https://framaforms.org/contribuer-au-jeu-de-cartes-mobiles-en-perspective-1757966394',
            'label': 'Contribuer au projet',
            'color': COLOR_ORANGE
        },
        {
            'url': 'https://github.com/Mobiles-en-Perspective/mobiles-en-perspective-jeu-de-cartes/releases/latest',
            'label': 'Télécharger le jeu',
            'color': COLOR_PURPLE
        }
    ]
    
    # Calculer l'espacement pour centrer les QR codes
    total_qr_width = 2 * QR_SIZE + QR_SPACING_H
    x_start = MARGIN + (CONTENT_WIDTH - total_qr_width) / 2
    
    y = y_start
    
    for i, qr_data in enumerate(qr_codes_data):
        row = i // 2
        col = i % 2
        
        x = x_start + col * (QR_SIZE + QR_SPACING_H)
        y_qr = y - row * (QR_SIZE + QR_LABEL_SPACING + 15 + QR_SPACING_V)
        
        # Générer et dessiner le QR code
        qr_img = generate_qr_code(qr_data['url'], QR_SIZE / mm)
        if qr_img:
            c.drawImage(qr_img, x, y_qr - QR_SIZE, width=QR_SIZE, height=QR_SIZE)
        else:
            # Fallback: dessiner un rectangle si le QR code ne peut pas être généré
            c.setStrokeColor(colors.red)
            c.setLineWidth(2)
            c.rect(x, y_qr - QR_SIZE, QR_SIZE, QR_SIZE, fill=0, stroke=1)
        
        # Label
        c.setFont('Roboto-Bold', 11)
        c.setFillColor(qr_data['color'])
        label_y = y_qr - QR_SIZE - QR_LABEL_SPACING - 4
        c.drawCentredString(x + QR_SIZE / 2, label_y, qr_data['label'])
    
    # Retourner la position Y après tous les QR codes
    y_after = y - 2 * (QR_SIZE + QR_LABEL_SPACING + 15 + QR_SPACING_V) + QR_SPACING_V
    return y_after


def draw_footer(c):
    """
    Dessine le pied de page avec le logo de licence CC BY 4.0 et le texte
    
    Args:
        c: Canvas ReportLab
    """
    y = 8 * mm
    
    # Texte de licence
    license_text = "Ce jeu est sous licence CC BY 4.0"
    c.setFont('Roboto', 9)
    c.setFillColor(COLOR_GRAY)
    
    # Calculer les dimensions
    text_width = stringWidth(license_text, 'Roboto', 9)
    logo_width = 22 * mm
    logo_height = 7.75 * mm
    spacing = 3 * mm
    
    total_width = logo_width + spacing + text_width
    x_start = (PAGE_WIDTH - total_width) / 2
    
    # Logo CC BY 4.0
    if os.path.exists(CC_BY_LOGO_PATH):
        try:
            cc_logo = ImageReader(CC_BY_LOGO_PATH)
            c.drawImage(cc_logo, x_start, y - logo_height / 2, width=logo_width, height=logo_height, preserveAspectRatio=True)
        except Exception as e:
            print(f"[ERREUR] Impossible d'afficher le logo CC BY: {e}")
    else:
        print(f"[AVERTISSEMENT] Logo CC BY introuvable à {CC_BY_LOGO_PATH}")
    
    # Texte
    c.drawString(x_start + logo_width + spacing, y, license_text)


def generate_affiche(output_path):
    """
    Génère l'affiche A3 complète
    
    Args:
        output_path: Chemin du fichier PDF de sortie
    """
    print("=" * 60)
    print("Génération de l'affiche de présentation")
    print("=" * 60)
    
    # Setup
    setup_fonts()
    
    # Télécharger les images si nécessaires
    if not os.path.exists(LOGO_PATH):
        download_image(LOGO_URL, LOGO_PATH)
    
    if not os.path.exists(CC_BY_LOGO_PATH):
        download_image(CC_BY_LOGO_URL, CC_BY_LOGO_PATH)
    
    # Lire la présentation
    presentation = read_presentation()
    if not presentation:
        print("[ERREUR] Impossible de continuer sans la présentation")
        return
    
    # Créer le canvas
    c = canvas.Canvas(output_path, pagesize=portrait(A3))
    
    # Position Y initiale (haut de page)
    y = PAGE_HEIGHT - MARGIN
    
    # Dessiner les sections
    y = draw_header(c, y)
    y = draw_presentation(c, y, presentation)
    
    # Espace avant les QR codes
    y -= 15 * mm
    
    draw_qr_codes(c, y)
    draw_footer(c)
    
    # Sauvegarder
    c.save()
    print("=" * 60)
    print(f"✅ Affiche générée : {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Génère l'affiche A3 de présentation du jeu 'Mobiles en Perspective'."
    )
    parser.add_argument(
        "-o", "--output",
        default="affiche-presentation.pdf",
        help="Chemin du PDF de sortie (défaut: affiche-presentation.pdf)"
    )
    
    args = parser.parse_args()
    output_path = os.path.abspath(args.output)
    
    generate_affiche(output_path)
