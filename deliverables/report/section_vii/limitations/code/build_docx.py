"""Tạo bản Word của mục 7.1 từ section_vii_limitations.md.

Chạy từ gốc repo:
    python deliverables/report/section_vii/limitations/code/build_docx.py

Định dạng theo bản 7.2 của Hoài Phú: khổ Letter, Times New Roman 13, chữ đen.
Bảng nhiều cột dùng cỡ 11 để vừa khổ dọc. Markdown là nguồn duy nhất của nội dung.
"""

import argparse
import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

HERE = Path(__file__).resolve().parent
FONT = 'Times New Roman'
TOKEN = re.compile(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[[^\]]+\]\([^)]+\))')


def set_font(run, size=None):
    run.font.name = FONT
    run.font.color.rgb = RGBColor(0, 0, 0)
    if size:
        run.font.size = Pt(size)
    rpr = run._element.get_or_add_rPr()
    fonts = rpr.get_or_add_rFonts()
    for key in ['ascii', 'hAnsi', 'cs', 'eastAsia']:
        fonts.set(qn('w:' + key), FONT)


def hyperlink(paragraph, label, url, size=None):
    rel = paragraph.part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
    link = OxmlElement('w:hyperlink')
    link.set(qn('r:id'), rel)
    run = OxmlElement('w:r')
    rpr = OxmlElement('w:rPr')
    fonts = OxmlElement('w:rFonts')
    for key in ['ascii', 'hAnsi', 'cs', 'eastAsia']:
        fonts.set(qn('w:' + key), FONT)
    rpr.append(fonts)
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '000000')
    rpr.append(color)
    underline = OxmlElement('w:u')
    underline.set(qn('w:val'), 'single')
    rpr.append(underline)
    if size:
        sz = OxmlElement('w:sz')
        sz.set(qn('w:val'), str(int(size * 2)))
        rpr.append(sz)
    run.append(rpr)
    text = OxmlElement('w:t')
    text.text = label
    text.set(qn('xml:space'), 'preserve')
    run.append(text)
    link.append(run)
    paragraph._p.append(link)


def inline(paragraph, text, size=None, bold=False):
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith('**'):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        elif part.startswith('`'):
            run = paragraph.add_run(part[1:-1])
            run.bold = True if bold else None
        elif part.startswith('['):
            label, url = re.match(r'\[([^\]]+)\]\(([^)]+)\)', part).groups()
            hyperlink(paragraph, label.replace('`', ''), url, size)
            continue
        elif part.startswith('*'):
            run = paragraph.add_run(part[1:-1])
            run.italic = True
            run.bold = True if bold else None
        else:
            run = paragraph.add_run(part)
            run.bold = True if bold else None
        set_font(run, size)


def configure(doc):
    section = doc.sections[0]
    section.page_width, section.page_height = Inches(8.5), Inches(11)
    section.top_margin = section.bottom_margin = Inches(0.7)
    section.left_margin = section.right_margin = Inches(0.85)
    section.footer_distance = Inches(0.28)
    for name in ['Normal', 'Title', 'Heading 1', 'Heading 2', 'List Bullet']:
        style = doc.styles[name]
        style.font.name = FONT
        style.font.size = Pt(13)
        style.font.color.rgb = RGBColor(0, 0, 0)
        fonts = style.element.get_or_add_rPr().get_or_add_rFonts()
        for key in list(fonts.attrib):
            del fonts.attrib[key]
        for key in ['ascii', 'hAnsi', 'cs', 'eastAsia']:
            fonts.set(qn('w:' + key), FONT)
        for border in list(style.element.findall('.//' + qn('w:pBdr'))):
            border.getparent().remove(border)
        style.paragraph_format.widow_control = True
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.line_spacing = 1.1
    for name in ['Title', 'Heading 1', 'Heading 2']:
        style = doc.styles[name]
        style.font.bold = True
        style.font.italic = False
        style.paragraph_format.keep_with_next = True
        style.paragraph_format.space_before = Pt(10)
    doc.styles['Title'].font.size = Pt(16)
    doc.styles['Heading 1'].font.size = Pt(14)
    doc.styles['Heading 2'].font.size = Pt(13)
    # Số trang ở chân trang.
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer.add_run()
    for kind, text in [('begin', None), (None, 'PAGE'), ('end', None)]:
        if kind:
            el = OxmlElement('w:fldChar')
            el.set(qn('w:fldCharType'), kind)
        else:
            el = OxmlElement('w:instrText')
            el.set(qn('xml:space'), 'preserve')
            el.text = text
        run._r.append(el)
    set_font(run, 11)


WIDTHS = {
    5: {'Ưu tiên': [1.35, 1.75, 1.55, 1.55, 0.6], 'Hạn chế': [1.85, 0.95, 1.4, 1.75, 0.85]},
    3: [2.9, 2.9, 1.0],
}


def column_widths(header):
    if len(header) == 5:
        return WIDTHS[5]['Ưu tiên' if header[-1] == 'Ưu tiên' else 'Hạn chế']
    return WIDTHS[len(header)]


def cell_margins(cell):
    tc = cell._tc.get_or_add_tcPr()
    margins = OxmlElement('w:tcMar')
    for edge in ['top', 'bottom', 'start', 'end']:
        m = OxmlElement('w:' + edge)
        m.set(qn('w:w'), '60')
        m.set(qn('w:type'), 'dxa')
        margins.append(m)
    tc.append(margins)


def repeat_header(row):
    trpr = row._tr.get_or_add_trPr()
    el = OxmlElement('w:tblHeader')
    el.set(qn('w:val'), 'true')
    trpr.append(el)


def no_split(row):
    trpr = row._tr.get_or_add_trPr()
    trpr.append(OxmlElement('w:cantSplit'))


def add_table(doc, lines):
    data = [[c.strip() for c in line.strip().strip('|').split('|')] for line in lines]
    header, body = data[0], data[2:]
    widths = column_widths(header)
    table = doc.add_table(rows=len(body) + 1, cols=len(header))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    size = 11
    for r, values in enumerate([header] + body):
        row = table.rows[r]
        no_split(row)
        if r == 0:
            repeat_header(row)
        for c, value in enumerate(values):
            cell = row.cells[c]
            cell.width = Inches(widths[c])
            cell_margins(cell)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            inline(p, value, size=size, bold=(r == 0))
    for c, w in enumerate(widths):
        table.columns[c].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def build(markdown, output):
    doc = Document()
    configure(doc)
    lines = markdown.read_text(encoding='utf-8').splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('|'):
            block = []
            while i < len(lines) and lines[i].startswith('|'):
                block.append(lines[i])
                i += 1
            add_table(doc, block)
            continue
        if not line.strip():
            i += 1
            continue
        if line.startswith('# '):
            inline(doc.add_paragraph(style='Title'), line[2:])
        elif line.startswith('## '):
            inline(doc.add_paragraph(style='Heading 1'), line[3:])
        elif line.startswith('- '):
            p = doc.add_paragraph(style='List Bullet')
            inline(p, line[2:])
        elif line.startswith('**') and line.endswith('**') and line.count('**') == 2:
            p = doc.add_paragraph(style='Heading 2')
            inline(p, line[2:-2])
            if line.startswith('**Bảng'):
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.space_after = Pt(4)
        else:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            inline(p, line)
        i += 1
    for style in doc.styles:
        if hasattr(style, 'font') and style.font is not None:
            style.font.color.rgb = RGBColor(0, 0, 0)
    doc.core_properties.title = '7.1 Hạn chế và dữ liệu cần bổ sung'
    doc.core_properties.author = 'Ngọc Quang'
    doc.save(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--markdown', default=str(HERE.parent / 'section_vii_limitations.md'))
    parser.add_argument('--output', default=str(HERE.parent / 'section_vii_limitations.docx'))
    args = parser.parse_args()
    build(Path(args.markdown), Path(args.output))
    print('Đã tạo', args.output)


if __name__ == '__main__':
    main()
