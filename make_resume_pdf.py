"""Generate KevinAudrain_Resume.pdf from README.md.

Run this script from the repository root:
    python make_resume_pdf.py

It reads README.md and writes KevinAudrain_Resume.pdf in the same folder.
"""

import re

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
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

i = 0
while i < len(lines):
    raw = lines[i]
    if raw.startswith('# '):
        text = format_text(raw[2:].strip())
        story.append(Paragraph(text, styles['MyHeading1']))
        i += 1
        continue
    if raw.startswith('## '):
        text = format_text(raw[3:].strip())
        story.append(Paragraph(text, styles['MyHeading2']))
        i += 1
        continue
    if raw.startswith('### '):
        # Keep the heading with the following bullet (if present) to avoid orphaned job titles
        text = format_text(raw[4:].strip())
        heading = Paragraph(text, styles['MyHeading2'])
        # find next non-empty line
        j = i + 1
        while j < len(lines) and lines[j].strip() == '':
            j += 1
        # If next line is a bold role line (starts with '**'), and the following non-empty line is a bullet,
        # keep heading + role + first bullet together.
        if j < len(lines) and lines[j].lstrip().startswith('**'):
            role_text = format_text(lines[j].strip())
            role_para = Paragraph(role_text, styles['MyBodyText'])
            k = j + 1
            while k < len(lines) and lines[k].strip() == '':
                k += 1
            if k < len(lines) and (lines[k].startswith('* ') or lines[k].startswith('- ')):
                bullet = format_text(lines[k][2:].strip())
                bullet_para = Paragraph(bullet, styles['MyList'], bulletText='•')
                story.append(KeepTogether([heading, role_para, bullet_para]))
                i = k + 1
                continue
            else:
                story.append(KeepTogether([heading, role_para]))
                i = j + 1
                continue
        # Otherwise, if next non-empty line is a bullet, keep heading + first bullet together
        if j < len(lines) and (lines[j].startswith('* ') or lines[j].startswith('- ')):
            bullet = format_text(lines[j][2:].strip())
            bullet_para = Paragraph(bullet, styles['MyList'], bulletText='•')
            story.append(KeepTogether([heading, bullet_para]))
            i = j + 1
            continue
        else:
            story.append(heading)
            i += 1
            continue
    if raw.startswith('* ') or raw.startswith('- '):
        bullet = format_text(raw[2:].strip())
        story.append(Paragraph(bullet, styles['MyList'], bulletText='•'))
        i += 1
        continue
    if raw.startswith('---'):
        story.append(Spacer(1, 8))
        i += 1
        continue
    if raw.strip() == '':
        story.append(Spacer(1, 6))
        i += 1
        continue
    text = format_text(raw)
    story.append(Paragraph(text, styles['MyBodyText']))
    i += 1

cleaned = []
for item in story:
    if isinstance(item, Spacer) and cleaned and isinstance(cleaned[-1], Spacer):
        continue
    cleaned.append(item)

pdf = SimpleDocTemplate(out_path, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=26, bottomMargin=26)
pdf.build(cleaned)
print(f'Created {out_path}')
