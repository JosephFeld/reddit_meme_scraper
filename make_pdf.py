from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# Define styles once
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    name='TitleStyle',
    parent=styles['Normal'],
    alignment=TA_CENTER,
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=16,
)
caption_style = ParagraphStyle(
    name='CaptionStyle',
    parent=styles['Normal'],
    alignment=TA_CENTER,
    fontName='Helvetica',
    fontSize=10,
    leading=12,
)

def get_canvas(output_pdf):
    page_width, page_height = landscape(A4)
    c = canvas.Canvas(output_pdf, pagesize=(page_width, page_height))
    return c

def draw_page(c, images, titles, captions):
    image_left, image_right = images
    title_left, title_right = titles
    caption_left, caption_right = captions

    # Page and layout setup
    page_width, page_height = landscape(A4)
    margin = 0.5 * inch
    column_width = (page_width - 2 * margin) / 2
    image_height = 4 * inch
    vertical_gap = 0.2 * inch

    # Y position for top of titles
    y_top = page_height - margin

    def draw_image_block(img_path, title, caption, x_left):
        # Title
        title_para = Paragraph(title, style=title_style)
        title_width, title_height = title_para.wrap(column_width, 2 * inch)
        title_para.drawOn(c, x_left, y_top - title_height)

        # Image
        img_y = y_top - title_height - vertical_gap
        if "." in img_path:
            c.drawImage(
                img_path,
                x_left,
                img_y - image_height,
                width=column_width,
                height=image_height,
                preserveAspectRatio=True,
                anchor='n'
            )

        # Caption
        caption_para = Paragraph(caption, style=caption_style)
        caption_width, caption_height = caption_para.wrap(column_width, 2 * inch)
        caption_y = img_y - image_height - caption_height - vertical_gap
        caption_para.drawOn(c, x_left, caption_y)

    # Draw both sides
    draw_image_block(image_left, title_left, caption_left, margin)
    draw_image_block(image_right, title_right, caption_right, margin + column_width)

    c.showPage()

def save_pdf(c):
    c.save()
