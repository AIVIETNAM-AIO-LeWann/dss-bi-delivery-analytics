"""Create the submission report from its verified Markdown content."""
from pathlib import Path
import re
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'Bao_cao_TV5_Hoai_Phu_10-11.docx'
doc=Document();sec=doc.sections[0]
sec.page_width=Cm(21);sec.page_height=Cm(29.7)
sec.top_margin=Cm(1.9);sec.bottom_margin=Cm(1.8)
sec.left_margin=Cm(2);sec.right_margin=Cm(2)
sec.footer_distance=Cm(.8)
styles=doc.styles
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3','List Bullet','Caption']:
    st=styles[name];st.font.name='Times New Roman';st.font.color.rgb=RGBColor(0,0,0)
    st.element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'Times New Roman')
styles['Normal'].font.size=Pt(12)
styles['Normal'].paragraph_format.line_spacing=1.12
styles['Normal'].paragraph_format.space_after=Pt(5)
for name,size in [('Title',19),('Heading 1',14),('Heading 2',12.5),('Heading 3',12)]:
    styles[name].font.size=Pt(size);styles[name].font.bold=True
    styles[name].paragraph_format.space_before=Pt(11 if name!='Title' else 0)
    styles[name].paragraph_format.space_after=Pt(5)
    styles[name].paragraph_format.keep_with_next=True
styles['Caption'].font.size=Pt(10.5);styles['Caption'].font.italic=True
styles['Caption'].paragraph_format.space_after=Pt(7)
doc.core_properties.title='Đề xuất cam kết giao hàng và phương án đội xe'
doc.core_properties.author='Hoài Phú'
doc.core_properties.subject='Chủ đề 18 Phân tích đề xuất hạn 10 tháng 11 năm 2026'
doc.core_properties.keywords='DHL, DataCo, Solomon, Logistics, TV5'

def link(p,label,url):
    h=OxmlElement('w:hyperlink');h.set(qn('r:id'),p.part.relate_to(url,RT.HYPERLINK,is_external=True))
    r=OxmlElement('w:r');pr=OxmlElement('w:rPr');col=OxmlElement('w:color');col.set(qn('w:val'),'1F4E79');pr.append(col)
    r.append(pr);t=OxmlElement('w:t');t.text=label;r.append(t);h.append(r);p._p.append(h)

def inline(p,text,size=None):
    # Word links keep long external URLs from overflowing the text column.
    pattern=r'(\*\*.*?\*\*|`[^`]+`|\[[^\]]+\]\(https?://[^)]+\)|https?://[^\s]+)'
    for token in re.split(pattern,text):
        if not token:continue
        match=re.fullmatch(r'\[([^\]]+)\]\((https?://[^)]+)\)',token)
        if match:link(p,match[1],match[2]);continue
        if token.startswith('http'):
            url=token.rstrip('.;');label='doi.org' if 'doi.org' in url else re.sub(r'^https?://','',url).split('/')[0]
            link(p,label,url);continue
        r=p.add_run(token.strip('`') if token.startswith('`') else token[2:-2] if token.startswith('**') else token)
        if token.startswith('**'):r.bold=True
        if size:r.font.size=Pt(size)

def table(rows):
    # Compact repeated numeric records without squeezing narrative columns.
    heads=rows[0];body=rows[1:]
    if len(heads)==8 and heads[0]=='Instance':
        rows=[['Instance và cấu hình','Phương pháp','K / Q','Xe dùng','Quãng đường (đv benchmark)']]
        for x in body:
            rows.append([x[0]+' / '+x[1], 'Điểm gần nhất' if x[2]=='nearest_feasible' else 'OR-Tools',x[3]+' / '+x[4],x[5],x[6] if len(x)==7 else x[7]])
        # The Markdown routing table has 7 columns in this version.
    elif len(heads)==7 and heads[0]=='Instance':
        rows=[['Instance và cấu hình','Phương pháp','K / Q','Xe dùng','Quãng đường (đv benchmark)']]
        for x in body:rows.append([x[0]+' / '+x[1], 'Điểm gần nhất' if x[2]=='nearest_feasible' else 'OR-Tools',x[3]+' / '+x[4],x[5],x[6]])
    heads=rows[0];n=len(heads)
    if n==5:widths=[5.6,2.9,2.8,2.8,2.9] if heads[0]=='Kịch bản' else [4.8,3.2,2.5,2,4.5] if heads[0]=='Instance và cấu hình' else [3.4,2,5,3.1,3.5]
    elif n==6:widths=[4,1.8,1.3,2.2,2.4,5.3]
    elif n==3:widths=[1.2,7,8.8]
    else:widths=[17/n]*n
    factor=17/sum(widths);widths=[w*factor for w in widths]
    t=doc.add_table(rows=0,cols=n);t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    for c,w in zip(t.columns,widths):c.width=Cm(w)
    for i,values in enumerate(rows):
        row=t.add_row();trpr=row._tr.get_or_add_trPr()
        cant=OxmlElement('w:cantSplit');trpr.append(cant)
        if i==0:repeat=OxmlElement('w:tblHeader');trpr.append(repeat)
        for j,(c,value) in enumerate(zip(row.cells,values)):
            if i>0:
                if re.fullmatch(r'\d+\.\d+%?',value):
                    pct=value.endswith('%');num=float(value.rstrip('%'))
                    value=f'{num:,.2f}'.replace(',','_').replace('.',',').replace('_','.')+('%' if pct else '')
                elif re.fullmatch(r'\d{4,}',value):
                    value=f'{int(value):,}'.replace(',','.')
            c.width=Cm(widths[j]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            pr=c._tc.get_or_add_tcPr()
            borders=OxmlElement('w:tcBorders')
            for side in ['top','left','bottom','right']:
                edge=OxmlElement('w:'+side);edge.set(qn('w:val'),'single');edge.set(qn('w:sz'),'4');edge.set(qn('w:color'),'D9D9D9');borders.append(edge)
            pr.append(borders)
            margins=OxmlElement('w:tcMar')
            for side in ['top','bottom','left','right']:
                m=OxmlElement('w:'+side);m.set(qn('w:w'),'85');m.set(qn('w:type'),'dxa');margins.append(m)
            pr.append(margins)
            shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'DCE6F1' if i==0 else 'FFFFFF' if i%2 else 'F5F7FA');pr.append(shade)
            p=c.paragraphs[0];p.paragraph_format.line_spacing=1.02;p.paragraph_format.space_after=Pt(0)
            p.alignment=WD_ALIGN_PARAGRAPH.CENTER if i==0 or (j>0 and n!=3) else WD_ALIGN_PARAGRAPH.LEFT
            inline(p,value,10.5)
            if i==0:
                for r in p.runs:r.bold=True
    doc.add_paragraph().paragraph_format.space_after=Pt(1)

def route_figures():
    for name in ['c101_nearest_feasible','c101_ortools']:
        p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(ROOT/'figures'/f'{name}.png'),width=Cm(8.1))
        p.paragraph_format.keep_with_next=True
        p.paragraph_format.space_after=Pt(0)
    doc.add_paragraph('Sơ đồ C101 trong hệ tọa độ benchmark. Trên: điểm gần nhất khả thi, 21 xe. Dưới: OR-Tools, 10 xe. Đây không phải bản đồ đường bộ.',style='Caption')

doc.add_paragraph('Đề xuất cam kết giao hàng và phương án đội xe',style='Title')
doc.add_paragraph('Chủ đề 18 Giao hàng đúng hẹn và tối ưu tuyến đường',style='Subtitle')
p=doc.add_paragraph();inline(p,'**Hoài Phú   |   Thành viên 5   |   Hạn nộp 10/11/2026**')
doc.add_paragraph('Bối cảnh DHL Supply Chain North America. Người nhận Giám đốc Logistics. Hoàn thành ngày 06/11/2026.')
text=(ROOT/'evidence/noi_dung_bao_cao.md').read_text()
lines=text.splitlines();i=0;start=False
while i<len(lines):
    line=lines[i].strip()
    if line.startswith('## 1.'):start=True
    if not start:i+=1;continue
    if not line:i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?',x or 'x') for x in cells):rows.append(cells)
            i+=1
        table(rows);continue
    if line.startswith('#'):
        m=re.match(r'^(#+)\s+(.*)',line);level=len(m[1])-1
        title=m[2]
        # Descriptive headings use words, numbers and spaces.
        title=re.sub(r'[.?:“”"—–/()]',' ',title)
        title=re.sub(r'\s+',' ',title).strip()
        if title.startswith('Nguồn nội bộ'):title='Tài liệu tham khảo và bằng chứng'
        doc.add_paragraph(title,style='Heading '+str(min(max(level,1),3)))
        i+=1;continue
    p=doc.add_paragraph(style='List Bullet' if line.startswith('- ') else 'Normal')
    inline(p,line[2:] if line.startswith('- ') else line)
    if line.startswith('Trên C101 cơ sở,'):
        route_figures()
    i+=1

# Page fields remain editable in Word; no decorative header.
p=sec.footer.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run();f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');r._r.addnext(f)
for st in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3']:
    pr=styles[st].element.find(qn('w:pPr'))
    if pr is not None:
        for b in list(pr.findall(qn('w:pBdr'))):pr.remove(b)
doc.save(TARGET)
print(TARGET)
