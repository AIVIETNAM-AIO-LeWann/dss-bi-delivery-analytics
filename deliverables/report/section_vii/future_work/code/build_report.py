"""Build TV5 future-work tables, figures, Markdown and Word from frozen handoffs.

From the shared repository root, run:
    python -m pip install matplotlib==3.10.8 python-docx==1.2.0
    python deliverables/report/section_vii/future_work/code/build_report.py

Optional --source-root reads another repository copy. --output-root writes to a
separate package directory. Source CSVs are read without modification.
"""

import argparse
import csv
from pathlib import Path
import re

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.shared import Inches, Pt, RGBColor


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def number(value, decimals=0):
    return f'{float(value):,.{decimals}f}'.translate(str.maketrans(',.', '.,'))


def percent(value):
    return number(float(value) * 100, 2)


def md_table(headers, rows):
    return '\n'.join([
        '| ' + ' | '.join(headers) + ' |',
        '| ' + ' | '.join('---' for _ in headers) + ' |',
        *['| ' + ' | '.join(map(str, row)) + ' |' for row in rows],
    ])


def configure_plot_fonts():
    candidates = [
        Path('/System/Library/Fonts/Supplemental'),
        Path('C:/Windows/Fonts'),
    ]
    for folder in candidates:
        if folder.exists():
            for path in folder.glob('*.ttf'):
                if 'times new roman' in path.name.lower() or path.name.lower().startswith('times'):
                    font_manager.fontManager.addfont(str(path))
    font_manager.findfont('Times New Roman', fallback_to_default=False)
    plt.rcParams.update({
        'font.family': 'Times New Roman',
        'font.size': 13,
        'text.color': '#000000',
        'axes.labelcolor': '#000000',
        'xtick.color': '#000000',
        'ytick.color': '#000000',
        'axes.labelsize': 13,
        'xtick.labelsize': 13,
        'ytick.labelsize': 13,
        'legend.fontsize': 13,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.linewidth': 0.6,
        'savefig.dpi': 300,
    })


def draw_figures(report, promises, fleet):
    configure_plot_fonts()
    folder = report / 'figures'
    folder.mkdir(parents=True, exist_ok=True)
    ordered = sorted(promises, key=lambda row: float(row['proposed_exceedance_rate']), reverse=True)
    fig, ax = plt.subplots(figsize=(6.8, 2.75))
    values = [float(row['proposed_exceedance_rate']) * 100 for row in ordered]
    positions = np.arange(len(ordered))
    ax.barh(positions, values, height=0.5, color='#3D566E')
    for y, row, value in zip(positions, ordered, values):
        label = f"{number(value, 2)}% ({number(row['proposed_exceedance_count'])} đơn)"
        ax.text(value + 1.8, y, label, va='center', fontsize=13)
        if value == 0:
            ax.plot(0, y, 'o', color='#3D566E', markersize=3)
    ax.set_yticks(positions, [row['shipping_mode'] for row in ordered])
    ax.invert_yaxis()
    ax.set_xlim(0, 110)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_xlabel('Tỷ lệ vượt hẹn còn lại (%)')
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, color='#DDDDDD', linewidth=0.5)
    ax.tick_params(axis='y', length=0)
    fig.subplots_adjust(left=0.22, right=0.99, top=0.96, bottom=0.24)
    fig.savefig(folder / 'future_work_promise_residual.png')
    plt.close(fig)

    base = [row for row in fleet if row['scenario'] == 'base']
    assert all(int(row['vehicle_capacity']) == 200 for row in base)
    fig, ax = plt.subplots(figsize=(6.8, 2.85))
    x = np.arange(len(base))
    lower = [int(row['capacity_lower_bound']) for row in base]
    feasible = [int(row['feasible_vehicles_used']) for row in base]
    bars_a = ax.bar(x - 0.18, lower, 0.34, label='Cận dưới từ tải', color='#D8D8D8', edgecolor='#555555', linewidth=0.6, hatch='///')
    bars_b = ax.bar(x + 0.18, feasible, 0.34, label='Xe trong lời giải khả thi', color='#3D566E')
    for bars in [bars_a, bars_b]:
        ax.bar_label(bars, padding=3, fontsize=13)
    ax.set_xticks(x, [row['instance'].upper() for row in base])
    ax.set_yticks([0, 5, 10, 15, 20, 25])
    ax.set_ylim(0, 26)
    ax.set_ylabel('Số xe')
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#DDDDDD', linewidth=0.5)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.28), ncol=2, frameon=False, handlelength=1.1, columnspacing=1)
    fig.subplots_adjust(left=0.1, right=0.99, bottom=0.15, top=0.77)
    fig.savefig(folder / 'future_work_fleet_bounds.png')
    plt.close(fig)


def create_markdown(report, promises, summary, model, fleet):
    current = next(row for row in summary if row['partition'] == 'test' and row['policy'] == 'current')
    proposed = next(row for row in summary if row['partition'] == 'test' and row['policy'] == 'bounded_plus1_keep_same_day')
    promise_table = md_table(
        ['Phương thức', 'Số đơn', 'Cam kết cũ → mới (ngày)', 'Vượt hẹn cũ (%)', 'Vượt hẹn mới (%)'],
        [[row['shipping_mode'], number(row['n']), f"{row['current_days']} → {row['proposed_days']}", percent(row['current_late_rate']), percent(row['proposed_exceedance_rate'])] for row in promises],
    )
    tp, fp, fn, tn = [int(model[name]) for name in ['tp', 'fp', 'fn', 'tn']]
    alert_table = md_table(
        ['Kết quả cảnh báo', 'Thực tế trễ', 'Thực tế không trễ', 'Tổng'],
        [['Có cảnh báo', number(tp), number(fp), number(tp + fp)], ['Không cảnh báo', number(fn), number(tn), number(fn + tn)], ['Tổng', number(tp + fn), number(fp + tn), number(model['n'])]],
    )
    chosen = [row for row in fleet if row['scenario'] != 'fleet10']
    fleet_table = md_table(
        ['Instance và Q', 'Cận dưới tải', 'Xe khả thi', 'Số xe tối thiểu'],
        [[f"{row['instance'].upper()} / {row['vehicle_capacity']}", row['capacity_lower_bound'], row['feasible_vehicles_used'], 'Đã chứng minh' if row['minimum_fleet_certified'] == 'True' else 'Chưa chứng minh'] for row in chosen],
    )
    extra_days = float(proposed['mean_proposed_days']) - float(current['mean_proposed_days'])
    text = f'''# 7.2 Hướng phát triển phân tích giao hàng và tối ưu đội xe

Kết quả ở Phần VI đặt ra ba hướng nghiên cứu tiếp theo cho Giám đốc Logistics, gồm kiểm chứng cam kết theo dịch vụ, ưu tiên cảnh báo theo nguồn lực và hoàn thiện quyết định số xe cùng thứ tự điểm dừng. Nghiên cứu đội xe tập trung vào số xe tối thiểu, mục tiêu chi phí và khả năng áp dụng cho một ngày giao thực tế. Mỗi hướng cần được kiểm chứng theo vấn đề còn lại trong kết quả hiện có.

## 7.2.1 Kiểm chứng cam kết theo từng dịch vụ

Trên {number(current['n'])} đơn test, phương án cộng tối đa một ngày và giữ Same Day bằng 0 làm tỷ lệ vượt hẹn tính lại giảm từ {percent(current['current_late_rate'])}% xuống {percent(proposed['proposed_exceedance_rate'])}%. Cam kết trung bình tăng {number(extra_days, 2)} ngày trong khi thời gian giao nguồn được giữ nguyên. Bảng 7.1 thể hiện sự khác biệt giữa các dịch vụ.

**Bảng 7.1 Kết quả hồi cứu của phương án cam kết giới hạn**

{promise_table}

Các tỷ lệ dùng số đơn của từng phương thức làm mẫu số.

![Hình 7.1 Tỷ lệ và số đơn vượt hẹn còn lại trong kịch bản cam kết giới hạn](figures/future_work_promise_residual.png)

Hình 7.1 dùng cùng tập test và kịch bản của Bảng 7.1. Nhãn cạnh thanh ghi tỷ lệ và số đơn vượt hẹn.

Second Class cần được ưu tiên nghiên cứu vì còn vượt hẹn 60,52%, tương ứng 1.565 đơn. Standard Class có tỷ lệ thấp hơn nhưng còn 1.546 đơn, gần bằng Second Class về khối lượng. Vì vậy, lựa chọn nhóm thí điểm cần xét đồng thời tỷ lệ và số đơn chịu ảnh hưởng. Same Day cần xác minh thời điểm khách thực nhận trước khi đề xuất cách giữ lời hứa giao trong ngày.

Nghiên cứu tiếp theo nên so sánh chính sách ứng viên với chính sách hiện hành trên đơn phát sinh sau khi chốt thiết kế. Nếu các đơn dùng chung xe hoặc nhân sự, có thể phân nhóm ngẫu nhiên theo ca hoặc khu vực để hạn chế ảnh hưởng giữa nhóm thử nghiệm và đối chứng. Theo dõi tỷ lệ vượt hẹn, thời gian giao thực, số ngày cam kết, hủy đơn và khiếu nại. Cỡ mẫu được xác định từ mức cải thiện cần phát hiện và đặc điểm phân nhóm. Quyết định mở rộng cần dựa trên khoảng tin cậy và mức đánh đổi thương mại đã thống nhất.

## 7.2.2 Phân bổ cảnh báo theo công suất và hiệu quả can thiệp

Baseline của TV4 tạo bốn mức xác suất theo phương thức. Tại ngưỡng 0,50, kết quả trên cùng {number(model['n'])} đơn test được tổng hợp ở Bảng 7.2.

**Bảng 7.2 Cảnh báo và kết quả thực tế trên tập test**

{alert_table}

Xác suất áp dụng cho cam kết cũ và mẫu không hủy trong dữ liệu lịch sử.

Precision đạt {percent(model['precision'])}% nhưng recall đạt {percent(model['recall'])}%, với {number(fn)} đơn trễ bị bỏ sót. Nghiên cứu tiếp theo cần xác định đội vận hành xử lý được bao nhiêu cảnh báo mỗi ngày, rồi đánh giá số đơn trễ tìm được trong giới hạn đó. Mô hình có khả năng xếp hạng trong từng phương thức có thể được so sánh trên giai đoạn validation và test mới, theo tiêu chí phù hợp công suất.

Hiệu quả xử lý cần được đo bằng thử nghiệm một hành động cụ thể, chẳng hạn rà soát đơn hoặc liên hệ điều phối sớm. Có thể dùng EVᵢ = pᵢ × eᵢ × Lᵢ − Cᵢ để đánh giá giá trị kỳ vọng. Trong đó pᵢ là xác suất vượt cam kết, eᵢ là tỷ lệ ngăn trễ khi can thiệp vào đơn vốn sẽ trễ, Lᵢ là tổn thất tránh được và Cᵢ là chi phí hành động. Hiệu quả can thiệp và chi phí cần được ước lượng từ thử nghiệm và kế toán. Khi đổi cam kết, xác suất pᵢ cũng cần được đánh giá lại theo lời hứa mới.

Đầu ra cần đạt là phương án ưu tiên vừa đáp ứng công suất vừa có bằng chứng về tác động. Thử nghiệm cần phân biệt ảnh hưởng của cảnh báo với ảnh hưởng của việc đổi cam kết. Nếu mở rộng sang mọi đơn mới, việc đánh giá phải bao quát quá trình hủy đơn từ thời điểm đặt hàng.

## 7.2.3 Hoàn thiện quyết định số xe và tuyến giao

Kết quả hiện tại đã trả lời chắc chắn bài toán số xe cho một cấu hình cụ thể. Với C101, sức chở Q = 200 và mỗi xe chạy một tuyến, tổng nhu cầu 1.810 đơn vị tạo cận dưới ceil(1.810 / 200) = 10 xe. Lời giải khả thi dùng đúng 10 xe đạt cận này. Các cấu hình khác còn khoảng cách giữa cận dưới tải và số xe đã tìm được, như Bảng 7.3.

**Bảng 7.3 Mức độ chứng minh số xe theo cấu hình**

{fleet_table}

Q là sức chở theo đơn vị benchmark. Mỗi xe chạy một tuyến. C101 ở cấu hình K = 10, Q = 200 cho cùng kết luận 10 xe nên được trình bày chung với C101 / 200.

![Hình 7.2 Cận dưới từ tải và số xe trong lời giải khả thi của ba instance cơ sở](figures/future_work_fleet_bounds.png)

Hình 7.2 dùng cấu hình cơ sở có Q = 200 và tối đa 25 xe. Cận dưới chỉ xét tổng tải, còn lời giải khả thi đã được kiểm tra tải và khung giờ.

Hình 7.2 cho thấy số xe tối thiểu được xác định ở C101, còn R101 và RC101 cần nghiên cứu thêm. Khoảng cách giữa hai cột phụ thuộc cả chất lượng lời giải và độ chặt của cận dưới. Nghiên cứu cần cải thiện hai phía trước khi kết luận còn giảm được bao nhiêu xe. Quãng đường 828,94 đơn vị của lời giải C101 là một kết quả khả thi đã lưu.

**Ưu tiên mục tiêu và kiểm tra độ ổn định**

Lượt giải hiện tại tối thiểu hóa quãng đường dưới giới hạn số xe. Bước phát triển tiếp theo cần chốt mục tiêu nghiệp vụ. Khi ưu tiên đội xe, có thể tìm số xe khả thi nhỏ nhất rồi tối ưu quãng đường trong cấu hình đó. Khi ưu tiên tổng chi phí, cần bổ sung chi phí sử dụng xe và chi phí di chuyển vào hàm mục tiêu. Thứ tự mục tiêu phải được xác định trước khi so sánh kết quả.

Trên benchmark, nên mở rộng tập instance và chạy nhiều lần với ngân sách thời gian thống nhất. Mỗi lần chạy lưu số xe, quãng đường, thời gian tính và trạng thái khả thi. Kết quả cần được kiểm tra phục vụ đủ khách, sức chở, khung giờ và thời điểm về kho. Với R101 và RC101, có thể bổ sung đối chứng khả thi tốt hơn để đánh giá chất lượng tuyến. Cận dưới có xét khung giờ cũng giúp thu hẹp khoảng chưa xác định về số xe tối thiểu.

**Kiểm chứng trên ca giao thực tế**

Một đợt chạy song song có thể dùng cùng danh sách khách, đội xe và khung giờ để so tuyến do bộ giải lập với tuyến của điều phối viên. Đánh giá ban đầu xác nhận đủ điểm dừng và không vi phạm ràng buộc cứng. Tuyến đủ điều kiện sau đó được đưa vào thí điểm có giám sát để ghi nhận km đường bộ, thời gian phục vụ, số xe và nhiên liệu thực đo.

Mô hình có thể mở rộng sang xe nhiều loại, giới hạn thể tích, nhiều chuyến và thời gian đường bộ thay đổi theo giờ khi có dữ liệu tương ứng. Với nhiều chuyến, cần gắn từng chuyến vào lịch sử dụng xe. Khi đó, cận dưới từ tổng nhu cầu chia sức chở phải được xét lại theo lịch chuyến và số xe vật lý.

Đánh giá kinh tế cần tính chi phí ca xe, tài xế, làm thêm, giao lại và nhiên liệu. Chi phí cố định và chi phí theo tuyến phải được xác định riêng để tránh tính trùng lợi ích. Các phương án được so trên cùng yêu cầu phục vụ, đồng thời kiểm tra độ nhạy theo sản lượng và giá nhiên liệu. Đầu ra phục vụ quyết định là số xe, lịch tuyến, tổng chi phí và mức độ đáp ứng dịch vụ cho một ngày giao cụ thể.


**Nguồn của từng bảng và biểu đồ**

| Bảng hoặc hình | File nguồn | Dữ liệu sử dụng |
| --- | --- | --- |
| **Bảng 7.1 và Hình 7.1** | [pilot_by_mode_test.csv](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/4e4fef27ef78499eb1eb891ab40e34d93aad71ed/workstreams/prescriptive/results/pilot_by_mode_test.csv) của TV5 | Số đơn, cam kết trước/sau và số đơn vượt hẹn theo phương thức |
| **Bảng 7.2** | [model_comparison.csv](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/4e4fef27ef78499eb1eb891ab40e34d93aad71ed/workstreams/forecasting/results/model_comparison.csv) của Ngọc Quang | Dòng `mode_baseline`, tập `test`, ngưỡng `0.5`. Tổng hàng/cột được tính bằng mã |
| **Bảng 7.3 và Hình 7.2** | [fleet_sizing_bounds.csv](https://github.com/AIVIETNAM-AIO-LeWann/dss-bi-delivery-analytics/blob/4e4fef27ef78499eb1eb891ab40e34d93aad71ed/workstreams/prescriptive/results/fleet_sizing_bounds.csv) của TV5 | Cận dưới tải, số xe khả thi và trạng thái chứng minh số xe tối thiểu |

'''
    path = report / 'section_vii_future_work.md'
    path.write_text(text.rstrip() + '\n', encoding='utf-8')
    return path


def hyperlink(paragraph, label, url):
    link = OxmlElement('w:hyperlink')
    link.set(qn('r:id'), paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True))
    run = OxmlElement('w:r')
    properties = OxmlElement('w:rPr')
    fonts = OxmlElement('w:rFonts')
    for key in ['ascii', 'hAnsi', 'eastAsia', 'cs']:
        fonts.set(qn('w:' + key), 'Times New Roman')
    properties.append(fonts)
    size = OxmlElement('w:sz')
    size.set(qn('w:val'), '26')
    properties.append(size)
    run.append(properties)
    text = OxmlElement('w:t')
    text.text = label
    run.append(text)
    link.append(run)
    paragraph._p.append(link)


def inline(paragraph, text):
    tokens = re.split(r'(\*\*.*?\*\*|\[[^\]]+\]\(https?://[^)]+\)|`[^`]+`)', text)
    for token in tokens:
        match = re.fullmatch(r'\[([^\]]+)\]\((https?://[^)]+)\)', token)
        if match:
            hyperlink(paragraph, match[1], match[2])
        elif token:
            bold = token.startswith('**') and token.endswith('**')
            code = token.startswith('`') and token.endswith('`')
            run = paragraph.add_run(token[2:-2] if bold else token[1:-1] if code else token)
            if bold:
                run.bold = True


def configure_word(doc):
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = section.bottom_margin = Inches(0.7)
    section.left_margin = section.right_margin = Inches(0.85)
    section.footer_distance = Inches(0.28)
    for name in ['Normal', 'Title', 'Subtitle', 'Heading 1', 'Heading 2', 'Caption']:
        style = doc.styles[name]
        style.font.name = 'Times New Roman'
        style.font.size = Pt(13)
        style.font.color.rgb = RGBColor(0, 0, 0)
        fonts = style.element.get_or_add_rPr().get_or_add_rFonts()
        for key in list(fonts.attrib):
            if 'theme' in key.lower():
                del fonts.attrib[key]
        for key in ['ascii', 'hAnsi', 'eastAsia', 'cs']:
            fonts.set(qn('w:' + key), 'Times New Roman')
        for border in list(style.element.findall('.//' + qn('w:pBdr'))):
            border.getparent().remove(border)
        style.paragraph_format.widow_control = True
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.line_spacing = 1.1
    for name in ['Title', 'Heading 1', 'Heading 2']:
        style = doc.styles[name]
        style.font.bold = True
        style.paragraph_format.keep_with_next = True
        style.paragraph_format.space_before = Pt(10)
    doc.styles['Caption'].font.italic = False
    doc.styles['Caption'].paragraph_format.space_after = Pt(5)
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    field = OxmlElement('w:fldSimple')
    field.set(qn('w:instr'), 'PAGE')
    field_run = OxmlElement('w:r')
    field_text = OxmlElement('w:t')
    field_text.text = '1'
    field_run.append(field_text)
    field.append(field_run)
    footer._p.append(field)
    footer.style = doc.styles['Normal']


def word_table(doc, rows, index):
    widths_by_index = [[1.32, 0.7, 1.65, 1.35, 1.78], [1.95, 1.5, 1.95, 1.4], [1.65, 1.3, 1.3, 2.55], [1.3, 2.25, 3.25]]
    widths = widths_by_index[index]
    table = doc.add_table(rows=0, cols=len(rows[0]))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for col, width in zip(table.columns, widths):
        col.width = Inches(width)
    for i, values in enumerate(rows):
        row = table.add_row()
        properties = row._tr.get_or_add_trPr()
        properties.append(OxmlElement('w:cantSplit'))
        if i == 0:
            properties.append(OxmlElement('w:tblHeader'))
        for column_index, (cell, value, width) in enumerate(zip(row.cells, values, widths)):
            cell.width = Inches(width)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if column_index == 0 or index == 3 else WD_ALIGN_PARAGRAPH.CENTER
            inline(p, value)
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(13)
                run.bold = i == 0
            tc = cell._tc.get_or_add_tcPr()
            margins = OxmlElement('w:tcMar')
            for edge in ['top', 'left', 'bottom', 'right']:
                margin = OxmlElement('w:' + edge)
                margin.set(qn('w:w'), '75')
                margin.set(qn('w:type'), 'dxa')
                margins.append(margin)
            tc.append(margins)
            borders = OxmlElement('w:tcBorders')
            for edge in ['top', 'left', 'bottom', 'right']:
                border = OxmlElement('w:' + edge)
                for key, val in [('val', 'single'), ('sz', '4'), ('color', 'D9D9D9')]:
                    border.set(qn('w:' + key), val)
                borders.append(border)
            tc.append(borders)
            if i == 0:
                fill = OxmlElement('w:shd')
                fill.set(qn('w:fill'), 'EEF1F3')
                tc.append(fill)


def create_word(markdown):
    doc = Document()
    configure_word(doc)
    lines = markdown.read_text(encoding='utf-8').splitlines()
    i = 0
    table_index = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                values = [value.strip() for value in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+', value) for value in values):
                    rows.append(values)
                i += 1
            word_table(doc, rows, table_index)
            table_index += 1
            continue
        image = re.fullmatch(r'!\[([^\]]+)\]\(([^)]+)\)', line)
        if image:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next = True
            drawing = p.add_run().add_picture(str(markdown.parent / image[2]), width=Inches(6.8))
            drawing._inline.docPr.set('descr', image[1])
            caption = doc.add_paragraph(style='Caption')
            caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
            inline(caption, image[1])
            caption.paragraph_format.keep_with_next = True
        elif line.startswith('# '):
            inline(doc.add_paragraph(style='Title'), line[2:])
        elif line.startswith('## '):
            inline(doc.add_paragraph(style='Heading 1'), line[3:])
        else:
            p = doc.add_paragraph()
            inline(p, line)
            p.paragraph_format.keep_together = True
            if line.startswith('**Bảng') or (line.startswith('**') and line.endswith('**')):
                p.paragraph_format.keep_with_next = True
            if line.startswith(('Hình ', 'Các tỷ lệ ', 'Xác suất áp dụng ', 'Q là sức chở ')):
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(8)
            if re.match(r'^\d+\. ', line):
                p.paragraph_format.left_indent = Inches(0.2)
                p.paragraph_format.first_line_indent = Inches(-0.2)
        i += 1
    for style in doc.styles:
        if hasattr(style, 'font'):
            style.font.color.rgb = RGBColor(0, 0, 0)
    for root in [doc.styles.element, doc.element, doc.sections[0].footer._element]:
        for color in root.iter(qn('w:color')):
            color.attrib.clear()
            color.set(qn('w:val'), '000000')
        for run in root.iter(qn('w:r')):
            properties = run.find(qn('w:rPr'))
            if properties is None:
                properties = OxmlElement('w:rPr')
                run.insert(0, properties)
            color = properties.find(qn('w:color'))
            if color is None:
                color = OxmlElement('w:color')
                properties.append(color)
            color.attrib.clear()
            color.set(qn('w:val'), '000000')
    doc.core_properties.author = 'Hoài Phú'
    doc.core_properties.title = 'Hướng phát triển phân tích giao hàng và tối ưu đội xe'
    doc.core_properties.subject = 'Phần VII Chủ đề 18 hạn 24/11/2026'
    doc.core_properties.language = 'vi-VN'
    doc.save(markdown.with_suffix('.docx'))
    assert table_index == 4


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    script = Path(__file__).resolve()
    parser.add_argument('--source-root', type=Path, default=script.parents[5])
    parser.add_argument('--output-root', type=Path, default=script.parents[1])
    args = parser.parse_args()
    source = args.source_root
    report = args.output_root
    report.mkdir(parents=True, exist_ok=True)
    result = source / 'workstreams/prescriptive/results'
    promises = read_csv(result / 'pilot_by_mode_test.csv')
    summary = read_csv(result / 'promise_summary.csv')
    fleet = read_csv(result / 'fleet_sizing_bounds.csv')
    models = read_csv(source / 'workstreams/forecasting/results/model_comparison.csv')
    model = next(row for row in models if row['model'] == 'mode_baseline' and row['partition'] == 'test')
    assert sum(int(row['n']) for row in promises) == int(model['n']) == 13071
    assert sum(int(model[key]) for key in ['tp', 'fp', 'fn', 'tn']) == int(model['n'])
    for row in promises:
        assert abs(int(row['proposed_exceedance_count']) / int(row['n']) - float(row['proposed_exceedance_rate'])) < 1e-12
    for row in fleet:
        lower = (int(row['total_demand']) + int(row['vehicle_capacity']) - 1) // int(row['vehicle_capacity'])
        assert lower == int(row['capacity_lower_bound']) <= int(row['feasible_vehicles_used'])
        assert (row['minimum_fleet_certified'] == 'True') == (lower == int(row['feasible_vehicles_used']))
    write_csv(report / 'tables/future_work_promises.csv', promises)
    write_csv(report / 'tables/future_work_alerts.csv', [{key: model[key] for key in ['model', 'partition', 'n', 'threshold', 'tp', 'fp', 'fn', 'tn', 'precision', 'recall']}])
    write_csv(report / 'tables/future_work_fleet.csv', [row for row in fleet if row['scenario'] != 'fleet10'])
    draw_figures(report, promises, fleet)
    markdown = create_markdown(report, promises, summary, model, fleet)
    create_word(markdown)
    print('Built Markdown, Word, 3 CSV tables and 2 PNG figures.')
    print('All source consistency checks passed. Word font is Times New Roman 13 pt.')


if __name__ == '__main__':
    main()
