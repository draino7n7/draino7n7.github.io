"""Generate KevinAudrain_Resume.pdf from README.md.

Run this script from the repository root:
    python make_resume_pdf.py

It reads README.md and writes KevinAudrain_Resume.pdf in the same folder.
"""

import re

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

input_path = 'README.md'
out_path = 'KevinAudrain_Resume.pdf'

with open(input_path, 'r', encoding='utf-8') as f:
    lines = [line.rstrip() for line in f]

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='MyHeading1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=22, spaceAfter=10, leading=26))
styles.add(ParagraphStyle(name='MyHeading2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, spaceAfter=6, leading=16))
styles.add(ParagraphStyle(name='MyBodyText', parent=styles['BodyText'], fontName='Helvetica', fontSize=10, leading=13, spaceAfter=4))
styles.add(ParagraphStyle(name='MyItalic', parent=styles['BodyText'], fontName='Helvetica-Oblique', fontSize=10, leading=13, textColor=colors.HexColor('#9aa3ad')))
styles.add(ParagraphStyle(name='MyList', parent=styles['BodyText'], leftIndent=22, bulletIndent=12, bulletFontName='Helvetica', bulletFontSize=10, leading=13, bulletOffsetY=2, spaceAfter=1))


def format_text(text):
    text = text.strip()
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text

story = []

for raw in lines:
    if raw.startswith('# '):
        text = format_text(raw[2:].strip())
        story.append(Paragraph(text, styles['MyHeading1']))
    elif raw.startswith('## '):
        text = format_text(raw[3:].strip())
        story.append(Paragraph(text, styles['MyHeading2']))
    elif raw.startswith('### '):
        text = format_text(raw[4:].strip())
        story.append(Paragraph(text, styles['MyHeading2']))
    elif raw.startswith('* ') or raw.startswith('- '):
        bullet = format_text(raw[2:].strip())
        story.append(Paragraph(bullet, styles['MyList'], bulletText='•'))
    elif raw.startswith('---'):
        story.append(Spacer(1, 8))
    elif raw.strip() == '':
        story.append(Spacer(1, 6))
    else:
        text = format_text(raw)
        story.append(Paragraph(text, styles['MyBodyText']))

cleaned = []
for item in story:
    if isinstance(item, Spacer) and cleaned and isinstance(cleaned[-1], Spacer):
        continue
    cleaned.append(item)

pdf = SimpleDocTemplate(out_path, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=26, bottomMargin=26)
pdf.build(cleaned)
print(f'Created {out_path}')
