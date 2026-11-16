"""Presentation system for the native delivery decision report."""
from __future__ import annotations

import csv
import hashlib
import shutil

from .powerbi_model import MEASURES, ROOT, OUT, REPORT, SCHEMA, write, literal, color

INK = '#142D3B'
TEAL = '#087E7C'
AMBER = '#AE6A3C'
MUTED = '#627780'
PAPER = '#F3F6F6'
BORDER = '#DFE7E7'
NAV = '#142D3B'
WHITE = '#FFFFFF'
PAGE_NAMES = {'overview': 'Tổng quan', 'risk': 'Rủi ro', 'promises': 'Cam kết',
              'routing': 'Tuyến giao', 'routing_detail': 'Lịch trình tuyến'}


def identifier(name: str) -> str:
    return hashlib.sha256(name.encode()).hexdigest()[:20]


def field(table, prop, measure=False, display=None):
    labels = {'shipping_mode': 'Phương thức', 'model_label': 'Mô hình', 'policy_label': 'Phương án',
              'method_label': 'Phương pháp', 'vehicle': 'Xe', 'sequence': 'Thứ tự',
              'node': 'Điểm dừng', 'x': 'Tọa độ X', 'y': 'Tọa độ Y', 'month_start': 'Tháng',
              'Số đơn': 'Số đơn', 'Chênh lệch cam kết': 'Chênh cam kết'}
    return {'field': {'Measure' if measure else 'Column': {'Expression': {'SourceRef': {'Entity': table}}, 'Property': prop}},
            'queryRef': f'{table}.{prop}', 'nativeQueryRef': prop,
            **({'displayName': display or labels[prop]} if display or prop in labels else {})}


def state_object(properties, state='default'):
    return {'selector': {'id': state}, 'properties': properties}


def selected_filter(table, column, value):
    expression = {'Column': {'Expression': {'SourceRef': {'Source': 's'}}, 'Property': column}}
    value = "'" + value.replace("'", "''") + "'" if isinstance(value, str) else str(value)+'D'
    return {'filter': {'Version': 2, 'From': [{'Name': 's', 'Entity': table, 'Type': 0}],
                       'Where': [{'Condition': {'In': {'Expressions': [expression], 'Values': [[{'Literal': {'Value': value}}]]}}}]}}


class Page:
    def __init__(self, key, title, scope, hidden=False):
        self.key = key
        self.path = REPORT/'definition/pages'/identifier(key)
        self.count = 0
        write(self.path/'page.json', {
            '$schema': SCHEMA+'item/report/definition/page/1.4.0/schema.json',
            'name': identifier(key), 'displayName': PAGE_NAMES[key], 'displayOption': 'FitToPage',
            'height': 936 if key == 'promises' else 884, 'width': 1440,
            **({'visibility': 'HiddenInViewMode'} if hidden else {}),
            'objects': {'background': [{'properties': {'color': color(PAPER), 'transparency': literal(0)}}]},
        })
        self.text('', 0, 0, 1440, 72, background=NAV, decorative=True)
        self.text('DELIVERY INSIGHTS', 28, 22, 400, 36, 17, WHITE, bold=True)
        self.navigator()
        self.text(title, 28, 90, 1000, 48, 26, INK, bold=True)
        self.text(scope, 1092, 92, 320, 48, 10, MUTED)

    def add(self, kind, x, y, width, height, *, title='', subtitle=None, roles=None,
            objects=None, background=WHITE, border=True, padding=16, title_color=INK,
            decorative=False, extra=None):
        self.count += 1
        name = identifier(self.path.name+str(self.count))
        chrome = {
            'title': [{'properties': {'show': literal(bool(title)), 'text': literal(title),
                'fontFamily': literal('Segoe UI'), 'fontSize': literal(13), 'bold': literal(True),
                'fontColor': color(title_color), 'titleWrap': literal(True)}}],
            'background': [{'properties': {'show': literal(background is not None),
                'color': color(background or WHITE), 'transparency': literal(0)}}],
            'border': [{'properties': {'show': literal(border), 'color': color(BORDER), 'radius': literal(10)}}],
            'padding': [{'properties': {key: literal(padding) for key in ['top', 'bottom', 'left', 'right']}}],
            'visualHeader': [{'properties': {'show': literal(False)}}],
        }
        if subtitle:
            chrome['subTitle'] = [{'properties': {'show': literal(True), 'text': literal(subtitle),
                'fontSize': literal(10), 'fontColor': color(MUTED), 'titleWrap': literal(True)}}]
        visual = {'visualType': kind, 'drillFilterOtherVisuals': True, 'visualContainerObjects': chrome}
        if roles:
            visual['query'] = {'queryState': {key: {'projections': value} for key, value in roles.items()}}
        if objects:
            visual['objects'] = objects
        if extra:
            visual.update(extra)
        data = {'$schema': SCHEMA+'item/report/definition/visualContainer/2.1.0/schema.json',
                'name': name, 'position': {'x': x, 'y': y, 'z': self.count, 'width': width,
                'height': height, 'tabOrder': self.count}, 'visual': visual}
        if decorative:
            data['annotations'] = [{'name': 'designRole', 'value': 'background'}]
        write(self.path/'visuals'/name/'visual.json', data)
        return data

    def text(self, value, x, y, width, height, size=12, fill=INK, background=None, bold=False, decorative=False):
        paragraphs = [{'textRuns': [{'value': line, 'textStyle': {'fontFamily': 'Segoe UI',
                       'fontSize': f'{size}pt', 'color': fill, **({'fontWeight': 'bold'} if bold else {})}}]}
                      for line in value.split('\n')]
        return self.add('textbox', x, y, width, height, padding=0, border=False, background=background,
                        objects={'general': [{'properties': {'paragraphs': paragraphs}}]}, decorative=decorative)

    def navigator(self):
        objects = {
            'layout': [{'properties': {'orientation': literal(0), 'columnCount': literal(4), 'cellPadding': literal(8)}}],
            'pages': [{'properties': {'showHiddenPages': literal(False), 'showTooltipPages': literal(False)}}],
            'fill': [state_object({'show': literal(True), 'fillColor': color(NAV)}),
                     state_object({'show': literal(True), 'fillColor': color('#244551')}, 'hover'),
                     state_object({'show': literal(True), 'fillColor': color(TEAL)}, 'selected')],
            'outline': [state_object({'show': literal(False)})],
            'shape': [{'properties': {'roundEdge': literal(8)}}, state_object({'tileShape': literal('rectangleRounded')})],
            'text': [state_object({'show': literal(True), 'fontFamily': literal('Segoe UI'), 'fontSize': literal(12),
                                  'fontColor': color('#D5E2E5'), 'horizontalAlignment': literal('center')}),
                     state_object({'show': literal(True), 'fontColor': color(WHITE), 'bold': literal(True)}, 'selected')],
        }
        self.add('pageNavigator', 604, 14, 808, 44, border=False, padding=0, background=None, objects=objects)

    def panel(self, x, y, width, height, background=WHITE):
        return self.add('textbox', x, y, width, height, background=background,
                        padding=0, decorative=True,
                        objects={'general': [{'properties': {'paragraphs': [{'textRuns': [{'value': ''}]}]}}]})

    def slicer(self, title, table, column, x, width, *, default=None, sync=None, y=148):
        # Explicit regions keep native dropdown controls away from their headings.
        self.panel(x, y, width, 80)
        self.text(title, x+12, y+6, width-24, 22, 12, INK, bold=True)
        objects = {'data': [{'properties': {'mode': literal('Dropdown')}}],
                   'header': [{'properties': {'show': literal(False)}}],
                   'items': [{'properties': {'textSize': literal(11), 'fontColor': color(INK)}}],
                   'selection': [{'properties': {'singleSelect': literal(True)}}]}
        if default is not None:
            objects['general'] = [{'properties': {'filter': selected_filter(table, column, default)}}]
        self.add('slicer', x+4, y+30, width-8, 48, roles={'Values': [field(table, column)]},
                 background=None, border=False, padding=8, objects=objects,
                 extra={'syncGroup': {'groupName': sync, 'fieldChanges': True, 'filterChanges': True}} if sync else None)

    def hidden_slicer(self, table, column, group):
        visual = self.add('slicer', 0, 0, 1, 1,
            roles={'Values': [field(table, column)]},
            extra={'syncGroup': {'groupName': group, 'fieldChanges': True, 'filterChanges': True}})
        visual['isHidden'] = True
        write(self.path/'visuals'/visual['name']/'visual.json', visual)

    def metric(self, title, table, measure, x, width, *, y=244, height=124, primary=False,
               detail=None, value_size=30, value_color=None):
        # Title, definition and value have fixed, disjoint rectangles.
        # A transparent native card only draws the value, so auto layout cannot
        # place the value over a title or subtitle.
        self.panel(x, y, width, height, NAV if primary else WHITE)
        self.text(title, x+16, y+12, width-32, 24, 12,
                  '#C7DFE0' if primary else MUTED, bold=True)
        if detail:
            self.text(detail, x+16, y+38, width-32, 20, 10,
                      '#C7DFE0' if primary else MUTED)
        return self.add('card', x+16, y+60, width-32, 60,
             roles={'Values': [field(table, 'Thẻ ' + measure if any(item[0] == 'Thẻ ' + measure for item in MEASURES[table]) else measure, True)]},
             background=None, border=False, padding=0,
             objects={'labels': [{'properties': {'fontFamily': literal('Segoe UI'),
                 'fontSize': literal(value_size), 'labelDisplayUnits': literal(1),
                 'color': color(WHITE if primary else value_color or INK)}}],
                 'categoryLabels': [{'properties': {'show': literal(False)}}]})

    def metric_row(self, values):
        for (x, width), (title, table, measure, detail) in zip([(28, 376), (420, 320), (756, 320), (1092, 320)], values):
            self.metric(title, table, measure, x, width, primary=x == 28, detail=detail,
                        value_size=34 if x == 28 else 30)

    def bar(self, title, table, column, measures, x, y, width, height, *, stacked=False, subtitle=None, percentage=False):
        objects = {
            'labels': [{'properties': {'show': literal(True), 'fontSize': literal(11),
                'color': color(INK), 'labelPosition': literal('InsideCenter' if stacked else 'OutsideEnd'),
                'labelOverflow': literal(False), 'labelDisplayUnits': literal(1), 'labelPrecision': literal(3 if table == 'ModelMetrics' else 1 if percentage else 0)}}],
            'categoryAxis': [{'properties': {'fontSize': literal(11), 'labelColor': color(MUTED), 'maxMarginFactor': literal(45), 'showAxisTitle': literal(False)}}],
            'valueAxis': [{'properties': {'fontSize': literal(10), 'labelColor': color(MUTED), 'showAxisTitle': literal(False),
                'gridlineColor': color('#E7EEEE'), 'start': literal(0), **({'end': literal(1.12)} if percentage else {})}}],
            'legend': [{'properties': {'show': literal(len(measures) > 1), 'fontSize': literal(10), 'position': literal('Top')}}],
        }
        visual = self.add('barChart' if stacked else 'clusteredBarChart', x, y, width, height, title=title,
                 subtitle=subtitle, roles={'Category': [field(table, column)],
                 'Y': [field(t, m, True, label) for t, m, label in measures]}, objects=objects)
        visual['visual']['query']['sortDefinition'] = {'sort': [{'field': field(measures[0][0], measures[0][1], True)['field'], 'direction': 'Descending'}], 'isDefaultSort': False}
        write(self.path/'visuals'/visual['name']/'visual.json', visual)

    def table(self, title, fields, x, y, width, height, *, subtitle=None):
        # Allocate the full content width; native fit-to-content leaves large
        # unused areas and can change widths after refresh.
        first = fields[0][1]
        weights = {'shipping_mode': [0.25]+[0.75/(len(fields)-1)]*(len(fields)-1),
                   'model_label': [0.40, 0.20, 0.20, 0.20],
                   'policy_label': [0.52, 0.24, 0.24],
                   'method_label': [0.46, 0.18, 0.36],
                   'vehicle': [0.16, 0.16, 0.20, 0.24, 0.24]}[first]
        widths = [round((width-40)*weight, 1) for weight in weights]
        self.add('tableEx', x, y, width, height, title=title, subtitle=subtitle,
                 roles={'Values': [field(*item) for item in fields]},
                 objects={'columnWidth': [
                    {'selector': {'metadata': f'{item[0]}.{item[1]}'}, 'properties': {'value': literal(w)}}
                    for item, w in zip(fields, widths)],
                    'grid': [{'properties': {'textSize': literal(11), 'rowPadding': literal(9 if first == 'policy_label' else 5 if first == 'model_label' else 3),
                    'gridVertical': literal(False), 'gridHorizontal': literal(True), 'gridHorizontalColor': color('#EBEFEF')}}],
                    'columnHeaders': [{'properties': {'fontSize': literal(10), 'fontColor': color(MUTED),
                        'backColor': color(WHITE), 'wordWrap': literal(False),
                        'autoSizeColumnWidth': literal(False), 'columnAdjustment': literal('fixedWidth'),
                        'customColumnWidth': literal(True)}},
                        *[{'selector': {'metadata': f'{item[0]}.{item[1]}'}, 'properties': {
                            'alignment': literal('Left' if item[1] in {'shipping_mode', 'model_label', 'policy_label', 'method_label', 'vehicle', 'Trạng thái đối chiếu'} else 'Right')}} for item in fields]],
                    'values': [{'properties': {'fontColorPrimary': color(INK), 'backColorPrimary': color(WHITE),
                        'fontColorSecondary': color(INK), 'backColorSecondary': color('#F3F7F7'), 'wordWrap': literal(False)}}],
                    'total': [{'properties': {'totals': literal(False)}}]})

    def button(self, text, x, y, width, *, destination=None, clear=False):
        objects = {
            'shape': [{'properties': {'roundEdge': literal(8)}}, state_object({'tileShape': literal('rectangleRounded')})],
            'fill': [{'properties': {'show': literal(True)}}, state_object({'fillColor': color(WHITE)}),
                     state_object({'fillColor': color('#E3F0EF')}, 'hover')],
            'outline': [{'properties': {'show': literal(False)}}],
            'icon': [{'properties': {'show': literal(False)}}],
            'text': [{'properties': {'show': literal(True)}},
                     state_object({'text': literal(text), 'fontSize': literal(11), 'fontColor': color(TEAL),
                                   'bold': literal(True), 'horizontalAlignment': literal('center')}),
                     state_object({'fontColor': color(TEAL)}, 'hover'),
                     state_object({'fontColor': color(MUTED)}, 'disabled')],
        }
        data = self.add('actionButton', x, y, width, 44, border=False, padding=0, background=None, objects=objects)
        action = {'show': literal(True), 'type': literal('ClearAllSlicers' if clear else 'PageNavigation')}
        if destination:
            action['navigationSection'] = literal(identifier(destination))
        data['visual']['visualContainerObjects']['visualLink'] = [{'properties': action}]
        write(self.path/'visuals'/data['name']/'visual.json', data)


def report():
    pages_folder = (REPORT/'definition/pages').resolve()
    if pages_folder.exists():
        assert pages_folder.is_relative_to((ROOT/'dashboards/powerbi').resolve())
        shutil.rmtree(pages_folder)
    write(OUT/'delivery_dashboard.pbip', {'$schema': SCHEMA+'pbip/pbipProperties/1.0.0/schema.json',
          'version': '1.0', 'artifacts': [{'report': {'path': 'Delivery.Report'}}], 'settings': {'enableAutoRecovery': True}})
    write(REPORT/'definition.pbir', {'$schema': SCHEMA+'item/report/definitionProperties/2.0.0/schema.json',
          'version': '4.0', 'datasetReference': {'byPath': {'path': '../Delivery.SemanticModel'}}})
    write(REPORT/'definition/version.json', {'$schema': SCHEMA+'item/report/definition/versionMetadata/1.0.0/schema.json', 'version': '2.0.0'})
    write(REPORT/'definition/report.json', {'$schema': SCHEMA+'item/report/definition/report/2.1.0/schema.json',
          'themeCollection': {'customTheme': {'name': 'delivery_theme.json', 'reportVersionAtImport': '5.59', 'type': 'RegisteredResources'}},
          'resourcePackages': [{'name': 'RegisteredResources', 'type': 'RegisteredResources',
              'items': [{'name': 'delivery_theme.json', 'path': 'delivery_theme.json', 'type': 'CustomTheme'}]}],
          'settings': {'useStylableVisualContainerHeader': True, 'exportDataMode': 'AllowSummarized'}})
    write(REPORT/'StaticResources/RegisteredResources/delivery_theme.json', {'name': 'delivery_theme.json',
          'dataColors': [TEAL, '#BC935F', '#BC6156', '#6D88A0', '#91ADA2'],
          'background': WHITE, 'foreground': INK, 'tableAccent': TEAL,
          'textClasses': {'title': {'fontFace': 'Segoe UI', 'fontSize': 13},
                         'label': {'fontFace': 'Segoe UI', 'fontSize': 11}, 'callout': {'fontFace': 'Segoe UI', 'fontSize': 32}}})
    write(REPORT/'definition/pages/pages.json', {'$schema': SCHEMA+'item/report/definition/pagesMetadata/1.0.0/schema.json',
          'pageOrder': [identifier(key) for key in PAGE_NAMES], 'activePageName': identifier('overview')})

    p = Page('overview', 'Hiệu suất giao hàng', 'DataCo, đơn không hủy\n01/2015 đến 01/2018')
    p.slicer('Phương thức giao', 'Orders', 'shipping_mode', 28, 376, sync='shipping_mode')
    p.slicer('Thị trường', 'Orders', 'market', 420, 320, sync='market')
    p.slicer('Vùng giao', 'Orders', 'order_region', 756, 456, sync='region')
    p.button('Xóa bộ lọc', 1228, 166, 184, clear=True)
    p.metric_row([('Tỷ lệ giao trễ', 'Orders', 'Tỷ lệ trễ', None),
                  ('Số đơn phân tích', 'Orders', 'Số đơn', None),
                  ('Giao thực tế', 'Orders', 'Thực tế TB', None),
                  ('Chênh cam kết', 'Orders', 'Chênh lệch cam kết', 'Thực tế trừ cam kết')])
    p.bar('Tỷ lệ trễ theo phương thức', 'Orders', 'shipping_mode', [('Orders', 'Tỷ lệ trễ', 'Giao trễ')],
          28, 388, 844, 248, percentage=True)
    p.add('lineChart', 892, 388, 520, 248, title='Tỷ lệ trễ theo tháng',
          roles={'Category': [field('Orders', 'month_start')], 'Y': [field('Orders', 'Tỷ lệ trễ', True)]},
          objects={'categoryAxis': [{'properties': {'axisType': literal('Scalar'), 'fontSize': literal(10), 'showAxisTitle': literal(False)}}],
                   'valueAxis': [{'properties': {'start': literal(0), 'end': literal(1), 'fontSize': literal(10), 'showAxisTitle': literal(False)}}],
                   'legend': [{'properties': {'show': literal(False)}}]})
    p.table('Cam kết và kết quả giao hàng', [('Orders', 'shipping_mode'), ('Orders', 'Số đơn', True),
            ('Orders', 'Tỷ lệ trễ', True), ('Orders', 'Cam kết TB', True), ('Orders', 'Thực tế TB', True)],
            28, 656, 1384, 208)


    p = Page('risk', 'Rủi ro giao trễ', 'Tập kiểm tra\n13.071 đơn, 07/2017 đến 01/2018')
    p.hidden_slicer('Orders', 'market', 'market')
    p.slicer('Ngưỡng cảnh báo', 'RiskThreshold', 'Value', 28, 376, default=0.5)
    p.slicer('Phương thức giao', 'Orders', 'shipping_mode', 420, 320, sync='shipping_mode')
    p.slicer('Vùng giao', 'Orders', 'order_region', 756, 456, sync='region')
    p.button('Xóa bộ lọc', 1228, 166, 184, clear=True)
    p.metric_row([('Độ chính xác cảnh báo', 'Orders', 'Precision theo ngưỡng', 'Tỷ lệ đúng trong số cảnh báo'),
                  ('Độ bao phủ đơn trễ', 'Orders', 'Recall theo ngưỡng', 'Tỷ lệ phát hiện trong số đơn trễ'),
                  ('Đơn được cảnh báo', 'Orders', 'Cảnh báo', None),
                  ('Đơn trễ bị bỏ sót', 'Orders', 'Bỏ sót', None)])
    p.bar('Cảnh báo và bỏ sót theo phương thức', 'Orders', 'shipping_mode', [
          ('Orders', 'Cảnh báo đúng', 'Cảnh báo đúng'), ('Orders', 'Cảnh báo sai', 'Cảnh báo sai'), ('Orders', 'Bỏ sót', 'Bỏ sót')],
          28, 388, 844, 248, stacked=True)
    p.bar('Khả năng xếp hạng của mô hình', 'ModelMetrics', 'model_label', [('ModelMetrics', 'AP ngoài mẫu', 'AP')],
          892, 388, 520, 248, subtitle='AP toàn tập kiểm tra, không đổi theo vùng')
    p.table('Chất lượng trên tập kiểm tra', [('ModelMetrics', 'model_label'),
            ('ModelMetrics', 'AUC ngoài mẫu', True, 'ROC-AUC'), ('ModelMetrics', 'AP ngoài mẫu', True, 'AP'),
            ('ModelMetrics', 'Log loss ngoài mẫu', True, 'Log loss')], 28, 656, 1384, 208)


    p = Page('promises', 'Phương án cam kết', 'Mô phỏng, 13.071 đơn kiểm tra\nGiữ nguyên thời gian giao thực tế')
    p.hidden_slicer('Orders', 'market', 'market')
    p.slicer('Phương án đang xem', 'PolicySelector', 'policy_label', 28, 376, default='Thêm một ngày')
    p.slicer('Phương thức giao', 'Orders', 'shipping_mode', 420, 320, sync='shipping_mode')
    p.slicer('Vùng giao', 'Orders', 'order_region', 756, 456, sync='region')
    p.button('Xóa bộ lọc', 1228, 166, 184, clear=True)
    p.metric_row([('Tỷ lệ vượt hẹn tính lại', 'PromiseScenarios', 'Vượt hẹn tính lại', None),
                  ('Giảm vượt hẹn', 'PromiseScenarios', 'Giảm vượt hẹn (điểm %)', 'So với hiện tại'),
                  ('Cam kết mới', 'PromiseScenarios', 'Cam kết mới TB', None),
                  ('Khách chờ thêm', 'PromiseScenarios', 'Tăng cam kết TB', None)])
    p.bar('Vượt hẹn theo phương thức', 'Orders', 'shipping_mode', [
          ('PromiseScenarios', 'Trễ hiện trạng test', 'Hiện tại'), ('PromiseScenarios', 'Vượt hẹn tính lại', 'Phương án đang xem')],
          28, 388, 844, 300, percentage=True)
    p.table('So sánh các phương án', [('Policies', 'policy_label'),
            ('PromiseScenarios', 'Vượt hẹn tính lại', True, 'Vượt hẹn'),
            ('PromiseScenarios', 'Cam kết mới TB', True, 'Cam kết')], 892, 388, 520, 300)
    p.table('Cam kết theo phương thức', [('Orders', 'shipping_mode'),
            ('Orders', 'Cam kết TB', True, 'Hiện tại'),
            ('PromiseScenarios', 'Cam kết mới TB', True, 'Phương án mới'),
            ('PromiseScenarios', 'Tăng cam kết TB', True, 'Tăng thêm')], 28, 708, 1384, 208)


    with (ROOT/'data/dashboard/route_cases.csv').open(encoding='utf-8-sig') as stream:
        cases = list(csv.DictReader(stream))
    default_case = next(row['case_label'] for row in cases if row['case_id'] == 'c101|base|ortools')
    p = Page('routing', 'Tuyến giao và nhiên liệu', 'Bộ bài toán Solomon\nPhương án đã tính')
    p.slicer('Phương án tuyến', 'RouteCases', 'case_label', 28, 664, default=default_case, sync='route_case')
    p.slicer('Km trên một đơn vị', 'KmPerUnit', 'Value', 708, 224, default=1, sync='km')
    p.slicer('Lít trên 100 km', 'FuelConsumption', 'Value', 948, 224, default=10, sync='fuel_consumption')
    p.slicer('Giá nhiên liệu (VND/lít)', 'FuelPrice', 'Value', 1188, 224, default=22000, sync='fuel_price')
    p.metric_row([('Nhiên liệu mô phỏng (VND)', 'RouteCases', 'Nhiên liệu mô phỏng', None),
                  ('Xe sử dụng', 'RouteCases', 'Số xe sử dụng', None),
                  ('Quãng đường chuẩn', 'RouteCases', 'Quãng đường benchmark', 'Đơn vị tọa độ Solomon'),
                  ('Giảm quãng đường', 'RouteCases', 'Giảm quãng đường', 'So với điểm gần nhất')])
    p.add('image', 28, 388, 680, 476, title='Sơ đồ tuyến theo xe',
          subtitle='Tọa độ Solomon, không phải đường bộ',
          objects={'image': [{'properties': {'sourceType': literal('imageData'),
              'sourceField': {'expr': field('RouteCases', 'Bản đồ tuyến', True)['field']}, 'fit': literal('Fit'),
              'altText': literal('Các tuyến theo thứ tự phục vụ, bắt đầu và kết thúc tại kho')}}]})
    p.bar('Quãng đường cùng cấu hình', 'RouteMethods', 'method_label', [('RouteCases', 'Quãng đường đối chiếu', 'Quãng đường')],
          728, 388, 684, 218)
    p.table('Đội xe và tính khả thi', [('RouteMethods', 'method_label'), ('RouteCases', 'Xe đối chiếu', True, 'Xe'),
            ('RouteCases', 'Trạng thái đối chiếu', True, 'Kết quả')], 728, 622, 684, 174)
    p.button('Xem lịch trình chi tiết', 728, 816, 684, destination='routing_detail')

    p = Page('routing_detail', 'Lịch trình tuyến', 'Bộ bài toán Solomon\nĐiểm 0 là kho', hidden=True)
    p.slicer('Phương án tuyến', 'RouteCases', 'case_label', 28, 844, default=default_case, sync='route_case')
    p.hidden_slicer('KmPerUnit', 'Value', 'km')
    p.hidden_slicer('FuelConsumption', 'Value', 'fuel_consumption')
    p.hidden_slicer('FuelPrice', 'Value', 'fuel_price')
    p.slicer('Xe', 'RouteStops', 'vehicle', 892, 320)
    p.button('Về trang tuyến', 1228, 166, 184, destination='routing')
    p.metric_row([('Nhiên liệu mô phỏng (VND)', 'RouteCases', 'Nhiên liệu mô phỏng', None),
                  ('Xe sử dụng', 'RouteCases', 'Số xe sử dụng', None),
                  ('Quãng đường chuẩn', 'RouteCases', 'Quãng đường benchmark', 'Đơn vị tọa độ Solomon'),
                  ('Giảm quãng đường', 'RouteCases', 'Giảm quãng đường', 'So với điểm gần nhất')])
    p.table('Thứ tự phục vụ', [('RouteStops', 'vehicle'), ('RouteStops', 'sequence'),
            ('RouteStops', 'node'), ('RouteStops', 'x'), ('RouteStops', 'y')], 28, 388, 680, 476)
    p.add('image', 728, 388, 684, 476, title='Toàn bộ phương án',
          subtitle='Sơ đồ hiển thị mọi xe trong phương án',
          objects={'image': [{'properties': {'sourceType': literal('imageData'),
              'sourceField': {'expr': field('RouteCases', 'Bản đồ tuyến', True)['field']}, 'fit': literal('Fit'),
              'altText': literal('Toàn bộ các tuyến của phương án đang chọn')}}]})


def main():
    report()


if __name__ == '__main__':
    main()
