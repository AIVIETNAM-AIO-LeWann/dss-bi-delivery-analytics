"""Presentation system for the native delivery report: a tactile "control panel".

Raised plates, recessed wells and the kraft-paper conclusion strip are built from
native containers with drop shadows; rings, thermometer, keypad and funnel are SVG
measures (see powerbi_svg.py) so they follow the report filters.
"""
from __future__ import annotations

import csv
import hashlib
import math
import shutil

from .powerbi_model import MEASURES, ROOT, OUT, REPORT, SCHEMA, write, literal, color

# ---- palette: warm paper, slate ink, vermilion (late), petrol teal (on time), brass (caution)
INK = '#1D2A33'
INK2 = '#45545E'
MUTED = '#5E6D76'
BASE = '#E4E0D7'
FACE = '#EAE7DF'
WELL = '#D7D3C8'
EDGE = '#F6F3ED'
RED = '#D2472A'
TEAL = '#0E7C86'
BRASS = '#B8860B'
STEEL = '#8E9AA3'
KRAFT = '#D8C69E'
KRAFT_INK = '#2B2314'
WHITE = '#FFFFFF'
SHADOW = '#686044'
FONT = 'Segoe UI'
LIGHT = 'Segoe UI Light'

CANVAS_W, CANVAS_H = 1440, 1000
X0, WIDTH = 140, 1272
RIGHT = X0 + WIDTH
PAGE_NAMES = {'overview': 'Tổng quan', 'risk': 'Rủi ro', 'promises': 'Cam kết',
              'routing': 'Tuyến giao', 'routing_detail': 'Lịch trình tuyến'}
NAVIGATION = ['overview', 'risk', 'promises', 'routing']


def identifier(name: str) -> str:
    return hashlib.sha256(name.encode()).hexdigest()[:20]


def field(table, prop, measure=False, display=None):
    labels = {'shipping_mode': 'Phương thức', 'model_label': 'Mô hình', 'policy_label': 'Phương án',
              'method_label': 'Phương pháp', 'vehicle': 'Xe', 'sequence': 'Thứ tự',
              'node': 'Điểm dừng', 'x': 'Tọa độ X', 'y': 'Tọa độ Y', 'month_start': 'Tháng',
              'market': 'Thị trường', 'Số đơn': 'Số đơn', 'Chênh lệch cam kết': 'Chênh cam kết'}
    return {'field': {'Measure' if measure else 'Column': {'Expression': {'SourceRef': {'Entity': table}}, 'Property': prop}},
            'queryRef': f'{table}.{prop}', 'nativeQueryRef': prop,
            **({'displayName': display or labels[prop]} if display or prop in labels else {})}


def state_object(properties, state='default'):
    return {'selector': {'id': state}, 'properties': properties}


def selected_filter(table, column, value):
    expression = {'Column': {'Expression': {'SourceRef': {'Source': 's'}}, 'Property': column}}
    value = "'" + value.replace("'", "''") + "'" if isinstance(value, str) else str(value) + 'D'
    return {'filter': {'Version': 2, 'From': [{'Name': 's', 'Entity': table, 'Type': 0}],
                       'Where': [{'Condition': {'In': {'Expressions': [expression], 'Values': [[{'Literal': {'Value': value}}]]}}}]}}


def visual_filter(table, column, value, name):
    body = selected_filter(table, column, value)['filter']
    return {'name': name, 'field': {'Column': {'Expression': {'SourceRef': {'Entity': table}}, 'Property': column}},
            'type': 'Categorical', 'filter': body}


def drop_shadow(shade, angle, distance, blur, transparency, spread=0, position='Outer'):
    return [{'properties': {'show': literal(True), 'preset': literal('Custom'), 'position': literal(position),
                            'color': color(shade), 'transparency': literal(transparency), 'shadowSpread': literal(spread),
                            'shadowBlur': literal(blur), 'angle': literal(angle), 'shadowDistance': literal(distance)}}]


# Light comes from the top-left: a bright shadow up-left, a warm dark shadow down-right.
BIG_LIGHT, BIG_DARK = drop_shadow(WHITE, 225, 8, 16, 8), drop_shadow(SHADOW, 45, 9, 20, 62)
SMALL_LIGHT, SMALL_DARK = drop_shadow(WHITE, 225, 4, 9, 8), drop_shadow(SHADOW, 45, 5, 11, 62)
INSET = drop_shadow(SHADOW, 45, 5, 10, 52, position='Inner')
TAPE_SHADOW = drop_shadow(SHADOW, 90, 4, 9, 62)


class Page:
    def __init__(self, key, title, scope, hidden=False, active=None):
        self.key = key
        self.path = REPORT / 'definition/pages' / identifier(key)
        self.count = 0
        write(self.path / 'page.json', {
            '$schema': SCHEMA + 'item/report/definition/page/1.4.0/schema.json',
            'name': identifier(key), 'displayName': PAGE_NAMES[key], 'displayOption': 'FitToPage',
            'height': CANVAS_H, 'width': CANVAS_W,
            **({'visibility': 'HiddenInViewMode'} if hidden else {}),
            'objects': {'background': [{'properties': {'color': color(BASE), 'transparency': literal(0)}}]},
        })
        self.rail(active or key)
        self.text(title, X0, 14, 540, 44, 25, INK, bold=True)
        self.text(scope, X0, 58, 540, 24, 10, MUTED)

    # ------------------------------------------------------------------ primitives
    def add(self, kind, x, y, width, height, *, title='', roles=None, objects=None, background=WHITE, border=True,
            padding=16, decorative=False, extra=None, radius=10, border_color=EDGE, shadow=None, filters=None):
        self.count += 1
        name = identifier(self.path.name + str(self.count))
        chrome = {
            'title': [{'properties': {'show': literal(bool(title)), 'text': literal(title), 'fontFamily': literal(FONT),
                                      'fontSize': literal(11), 'bold': literal(True), 'fontColor': color(INK),
                                      'titleWrap': literal(True)}}],
            'background': [{'properties': {'show': literal(background is not None), 'color': color(background or WHITE),
                                           'transparency': literal(0)}}],
            'border': [{'properties': {'show': literal(border), 'color': color(border_color), 'radius': literal(radius)}}],
            'padding': [{'properties': {key: literal(padding) for key in ['top', 'bottom', 'left', 'right']}}],
            'visualHeader': [{'properties': {'show': literal(False)}}],
        }
        if shadow:
            chrome['dropShadow'] = shadow
        visual = {'visualType': kind, 'drillFilterOtherVisuals': True, 'visualContainerObjects': chrome}
        if roles:
            visual['query'] = {'queryState': {key: {'projections': value} for key, value in roles.items()}}
        if objects:
            visual['objects'] = objects
        if extra:
            visual.update(extra)
        data = {'$schema': SCHEMA + 'item/report/definition/visualContainer/2.1.0/schema.json',
                'name': name, 'position': {'x': x, 'y': y, 'z': self.count, 'width': width, 'height': height,
                                           'tabOrder': self.count}, 'visual': visual}
        if filters:
            data['filterConfig'] = {'filters': [visual_filter(t, c, v, identifier(name + c + str(v))) for t, c, v in filters]}
        if decorative:
            data['annotations'] = [{'name': 'designRole', 'value': 'background'}]
        write(self.path / 'visuals' / name / 'visual.json', data)
        return data

    def text(self, value, x, y, width, height, size=12, fill=INK, bold=False, align=None, background=None, radius=0,
             decorative=False, font=FONT, shadow=None, border_color=None):
        height = max(height, math.ceil(size * 1.333 + 8))  # shorter boxes show a scroll thumb in Desktop
        paragraphs = [{'textRuns': [{'value': line, 'textStyle': {'fontFamily': font, 'fontSize': f'{size}pt', 'color': fill,
                                                                 **({'fontWeight': 'bold'} if bold else {})}}],
                       **({'horizontalTextAlignment': align} if align else {})} for line in value.split('\n')]
        return self.add('textbox', x, y, width, height, padding=0, border=background is not None, background=background,
                        radius=radius, border_color=border_color or background or EDGE, shadow=shadow,
                        objects={'general': [{'properties': {'paragraphs': paragraphs}}]}, decorative=decorative)

    def blank(self, x, y, width, height, background, radius, shadow, border_color=None):
        return self.add('textbox', x, y, width, height, padding=0, border=True, background=background, radius=radius,
                        border_color=border_color or background, shadow=shadow, decorative=True,
                        objects={'general': [{'properties': {'paragraphs': [{'textRuns': [{'value': ''}]}]}}]})

    def plate(self, x, y, width, height, radius=18, face=FACE, small=False):
        """Raised plate: a bright shadow layer under a dark shadow layer."""
        light, dark = (SMALL_LIGHT, SMALL_DARK) if small else (BIG_LIGHT, BIG_DARK)
        self.blank(x, y, width, height, face, radius, light)
        self.blank(x, y, width, height, face, radius, dark, border_color=EDGE)

    def well(self, x, y, width, height, radius=14):
        """Recessed well with an inner shadow."""
        self.blank(x, y, width, height, WELL, radius, INSET, border_color=WELL)

    def card(self, x, y, width, height, table, measure, size=20, fill=INK, font=LIGHT, filters=None, formatted=True):
        name = 'Thẻ ' + measure if formatted and any(item[0] == 'Thẻ ' + measure for item in MEASURES[table]) else measure
        return self.add('card', x, y, width, height, roles={'Values': [field(table, name, True)]}, background=None,
                        border=False, padding=0, filters=filters,
                        objects={'labels': [{'properties': {'fontFamily': literal(font), 'fontSize': literal(size),
                                                            'labelDisplayUnits': literal(1), 'color': color(fill)}}],
                                 'categoryLabels': [{'properties': {'show': literal(False)}}]})

    def picture(self, x, y, width, height, table, measure, alt, filters=None):
        return self.add('image', x, y, width, height, background=None, border=False, padding=0, filters=filters,
                        objects={'image': [{'properties': {'sourceType': literal('imageData'),
                                                           'sourceField': {'expr': field(table, measure, True)['field']},
                                                           'fit': literal('Fit'), 'altText': literal(alt)}}]})

    def heading(self, x, y, width, title, sub=None):
        self.text(title, x, y, width, 22, 10.5, INK, bold=True)
        if sub:
            self.text(sub, x, y + 23, width, 18, 8.5, MUTED)

    # ------------------------------------------------------------------ rail, header, conclusion strip
    def rail(self, active):
        self.plate(16, 16, 100, 968, radius=24)
        self.picture(30, 28, 72, 72, 'Orders', 'Logo', 'Logo Delivery Insights')
        self.text('Delivery', 24, 101, 84, 23, 11, INK, bold=True, align='center')
        self.text('INSIGHTS', 24, 124, 84, 16, 8, MUTED, align='center')
        for index, key in enumerate(NAVIGATION):
            y = 160 + index * 64
            if key == active:
                self.well(28, y, 76, 52, radius=14)
                self.text(PAGE_NAMES[key], 30, y + 15, 66, 22, 9.5, INK, bold=True, align='center')
                self.blank(94, y + 8, 6, 6, RED, 3, None)
            else:
                self.plate(28, y, 76, 52, radius=14, small=True)
                self.navigation_button(PAGE_NAMES[key], key, 28, y, 76, 52)
        self.well(28, 424, 76, 548, radius=16)
        self.text('DỮ LIỆU', 28, 436, 76, 14, 7.5, MUTED, bold=True, align='center')
        for index, (measure, label) in enumerate([('Số đơn toàn kỳ', 'đơn'), ('Số tháng toàn kỳ', 'tháng'),
                                                  ('Số thị trường toàn kỳ', 'thị trường')]):
            y = 456 + index * 56
            self.card(32, y, 68, 30, 'Orders', measure, 15, INK)
            self.text(label, 32, y + 30, 68, 14, 8, MUTED, align='center')
        self.picture(46, 630, 44, 250, 'Orders', 'Nhiệt kế toàn kỳ', 'Nhiệt kế tỷ lệ trễ toàn kỳ')
        self.text('trễ toàn kỳ', 28, 886, 76, 19, 8, MUTED, align='center')
        self.card(32, 906, 68, 32, 'Orders', 'Tỷ lệ trễ toàn kỳ', 15, RED)

    def navigation_button(self, text, destination, x, y, width, height):
        objects = {
            'shape': [{'properties': {'roundEdge': literal(14)}}, state_object({'tileShape': literal('rectangleRounded')})],
            'fill': [{'properties': {'show': literal(True)}}, state_object({'fillColor': color(FACE)}),
                     state_object({'fillColor': color('#F2EFE8')}, 'hover')],
            'outline': [{'properties': {'show': literal(False)}}],
            'icon': [{'properties': {'show': literal(False)}}],
            'text': [{'properties': {'show': literal(True)}},
                     state_object({'text': literal(text), 'fontFamily': literal(FONT), 'fontSize': literal(8.5),
                                   'fontColor': color(MUTED), 'bold': literal(False), 'horizontalAlignment': literal('center')}),
                     state_object({'fontColor': color(INK)}, 'hover')],
        }
        data = self.add('actionButton', x, y, width, height, border=False, padding=0, background=None, objects=objects)
        data['visual']['visualContainerObjects']['visualLink'] = [{'properties': {
            'show': literal(True), 'type': literal('PageNavigation'), 'navigationSection': literal(identifier(destination))}}]
        write(self.path / 'visuals' / data['name'] / 'visual.json', data)

    def action_button(self, text, x, y, width, height, *, destination=None, clear=False, tone=RED):
        self.plate(x, y, width, height, radius=14, small=True)
        objects = {
            'shape': [{'properties': {'roundEdge': literal(14)}}, state_object({'tileShape': literal('rectangleRounded')})],
            'fill': [{'properties': {'show': literal(True)}}, state_object({'fillColor': color(FACE)}),
                     state_object({'fillColor': color('#F2EFE8')}, 'hover')],
            'outline': [{'properties': {'show': literal(False)}}],
            'icon': [{'properties': {'show': literal(False)}}],
            'text': [{'properties': {'show': literal(True)}},
                     state_object({'text': literal(text), 'fontFamily': literal(FONT), 'fontSize': literal(10),
                                   'fontColor': color(tone), 'bold': literal(True), 'horizontalAlignment': literal('center')}),
                     state_object({'fontColor': color(tone)}, 'hover')],
        }
        data = self.add('actionButton', x, y, width, height, border=False, padding=0, background=None, objects=objects)
        action = {'show': literal(True), 'type': literal('ClearAllSlicers' if clear else 'PageNavigation')}
        if destination:
            action['navigationSection'] = literal(identifier(destination))
        data['visual']['visualContainerObjects']['visualLink'] = [{'properties': action}]
        write(self.path / 'visuals' / data['name'] / 'visual.json', data)

    def filters(self, specs, reset=True):
        """Right-aligned recessed filter wells; specs are (label, table, column, width, options)."""
        x = RIGHT
        if reset:
            x -= 100
            self.action_button('Xóa bộ lọc', x, 16, 100, 72, clear=True)
            x -= 12
        for label, table, column, width, options in reversed(specs):
            x -= width
            self.slicer(label, table, column, x, width, **options)
            x -= 12

    def slicer(self, label, table, column, x, width, *, default=None, sync=None, y=16):
        self.well(x, y, width, 72)
        self.text(label, x + 14, y + 2, width - 28, 20, 8.5, MUTED)
        objects = {'data': [{'properties': {'mode': literal('Dropdown')}}],
                   'header': [{'properties': {'show': literal(False)}}],
                   'items': [{'properties': {'textSize': literal(11), 'fontColor': color(INK), 'fontFamily': literal(FONT)}}],
                   'selection': [{'properties': {'singleSelect': literal(True)}}]}
        if default is not None:
            objects['general'] = [{'properties': {'filter': selected_filter(table, column, default)}}]
        self.add('slicer', x + 6, y + 22, width - 12, 48, roles={'Values': [field(table, column)]}, background=None,
                 border=False, padding=6, objects=objects,
                 extra={'syncGroup': {'groupName': sync, 'fieldChanges': True, 'filterChanges': True}} if sync else None)

    def hidden_slicer(self, table, column, group):
        visual = self.add('slicer', 0, 0, 1, 1, roles={'Values': [field(table, column)]},
                          extra={'syncGroup': {'groupName': group, 'fieldChanges': True, 'filterChanges': True}})
        visual['isHidden'] = True
        write(self.path / 'visuals' / visual['name'] / 'visual.json', visual)

    def tape(self, table, measure):
        """Kraft-paper label strip carrying a dynamic conclusion."""
        self.blank(X0, 96, WIDTH, 38, KRAFT, 7, TAPE_SHADOW, border_color='#F0E4C8')
        self.blank(X0 + 10, 111, 9, 9, '#8F7F58', 4.5, None)
        self.blank(RIGHT - 19, 111, 9, 9, '#8F7F58', 4.5, None)
        self.text('KẾT LUẬN', X0 + 30, 104, 88, 22, 8, '#E8D9B3', bold=True, align='center', background=KRAFT_INK, radius=3)
        self.card(X0 + 130, 100, WIDTH - 160, 30, table, measure, 10.5, KRAFT_INK, FONT, formatted=False)

    # ------------------------------------------------------------------ charts and tables
    def bar(self, title, table, column, measures, x, y, width, height, *, stacked=False, percentage=False, legend=None):
        objects = {
            'labels': [{'properties': {'show': literal(True), 'fontSize': literal(10), 'fontFamily': literal(FONT),
                                       'color': color(INK), 'labelPosition': literal('InsideCenter' if stacked else 'OutsideEnd'),
                                       'labelOverflow': literal(False), 'labelDisplayUnits': literal(1),
                                       'labelPrecision': literal(3 if table == 'ModelMetrics' else 1 if percentage else 0)}}],
            'categoryAxis': [{'properties': {'fontSize': literal(10.5), 'fontFamily': literal(FONT), 'labelColor': color(INK2),
                                             'maxMarginFactor': literal(45), 'showAxisTitle': literal(False)}}],
            'valueAxis': [{'properties': {'fontSize': literal(9.5), 'labelColor': color(MUTED), 'showAxisTitle': literal(False),
                                          'gridlineColor': color('#CFCABF'), 'start': literal(0),
                                          **({'end': literal(1.12)} if percentage else {})}}],
            'legend': [{'properties': {'show': literal(len(measures) > 1 if legend is None else legend),
                                       'fontSize': literal(10), 'position': literal('Top')}}],
        }
        visual = self.add('barChart' if stacked else 'clusteredBarChart', x, y, width, height, title=title, background=None,
                          border=False, padding=4, roles={'Category': [field(table, column)],
                                                          'Y': [field(t, m, True, label) for t, m, label in measures]},
                          objects=objects)
        visual['visual']['query']['sortDefinition'] = {'sort': [{'field': field(measures[0][0], measures[0][1], True)['field'],
                                                                 'direction': 'Descending'}], 'isDefaultSort': False}
        write(self.path / 'visuals' / visual['name'] / 'visual.json', visual)

    def line(self, x, y, width, height, table, measure, *, compact=False, color_hex=INK):
        axis = {'show': literal(False)} if compact else {'fontSize': literal(9.5), 'fontFamily': literal(FONT),
                                                        'labelColor': color(MUTED), 'showAxisTitle': literal(False)}
        value_axis = dict(axis)
        if not compact:
            value_axis.update({'gridlineColor': color('#CFCABF')})
        else:
            value_axis['gridlineShow'] = literal(False)
        objects = {'categoryAxis': [{'properties': {**axis, **({} if compact else {'axisType': literal('Scalar')})}}],
                   'valueAxis': [{'properties': value_axis}],
                   'legend': [{'properties': {'show': literal(False)}}],
                   'lineStyles': [{'properties': {'strokeWidth': literal(1.6 if compact else 2.2)}}],
                   'dataPoint': [{'properties': {'fill': color(color_hex)}}]}
        return self.add('lineChart', x, y, width, height, background=None, border=False, padding=2,
                        roles={'Category': [field('Orders', 'month_start')], 'Y': [field(table, measure, True)]}, objects=objects)

    def scatter(self, x, y, width, height, category, x_measure, y_measure, size_measure=None, y_end=None):
        roles = {'Category': [field(*category)], 'X': [field(*x_measure, True)], 'Y': [field(*y_measure, True)]}
        if size_measure:
            roles['Size'] = [field(*size_measure, True)]
        objects = {'categoryLabels': [{'properties': {'show': literal(True), 'fontSize': literal(10), 'fontFamily': literal(FONT),
                                                      'color': color(INK)}}],
                   'categoryAxis': [{'properties': {'fontSize': literal(9.5), 'labelColor': color(MUTED), 'showAxisTitle': literal(False),
                                                    'gridlineColor': color('#CFCABF')}}],
                   'valueAxis': [{'properties': {'fontSize': literal(9.5), 'labelColor': color(MUTED), 'showAxisTitle': literal(False),
                                                 'gridlineColor': color('#CFCABF'), **({'end': literal(y_end)} if y_end else {})}}],
                   'legend': [{'properties': {'show': literal(False)}}],
                   'dataPoint': [{'properties': {'defaultColor': color(TEAL)}}]}
        return self.add('scatterChart', x, y, width, height, background=None, border=False, padding=4, roles=roles, objects=objects)

    def table(self, title, fields, x, y, width, height, *, weights=None, row_padding=6):
        first = fields[0][1]
        weights = weights or [0.25] + [0.75 / (len(fields) - 1)] * (len(fields) - 1)
        widths = [round((width - 28) * weight, 1) for weight in weights]
        text_columns = {item[1] for item in fields if len(item) == 2 or item[2] is not True}
        self.add('tableEx', x, y, width, height, title=title, background=None, border=False, padding=4,
                 roles={'Values': [field(*item) for item in fields]},
                 objects={'columnWidth': [{'selector': {'metadata': f'{item[0]}.{item[1]}'}, 'properties': {'value': literal(w)}}
                                          for item, w in zip(fields, widths)],
                          'grid': [{'properties': {'textSize': literal(10.5), 'rowPadding': literal(row_padding),
                                                   'gridVertical': literal(False), 'gridHorizontal': literal(True),
                                                   'gridHorizontalColor': color('#CFCABF')}}],
                          'columnHeaders': [{'properties': {'fontSize': literal(9.5), 'fontColor': color(MUTED), 'backColor': color(FACE),
                                                            'wordWrap': literal(False), 'autoSizeColumnWidth': literal(False),
                                                            'columnAdjustment': literal('fixedWidth'), 'customColumnWidth': literal(True)}},
                                             *[{'selector': {'metadata': f'{item[0]}.{item[1]}'},
                                                'properties': {'alignment': literal('Left' if item[1] in text_columns else 'Right')}}
                                               for item in fields]],
                          'values': [{'properties': {'fontColorPrimary': color(INK), 'backColorPrimary': color(FACE),
                                                     'fontColorSecondary': color(INK), 'backColorSecondary': color('#E5E2D9'),
                                                     'wordWrap': literal(False)}}],
                          'total': [{'properties': {'totals': literal(False)}}]})


# --------------------------------------------------------------------------- page building blocks
MODE_ORDER = ['First Class', 'Second Class', 'Same Day', 'Standard Class']


def mode_tile(p, x, y, mode):
    p.plate(x, y, 450, 137, radius=16, small=True)
    flt = [('Orders', 'shipping_mode', mode)]
    p.text(mode, x + 20, y + 12, 150, 22, 10.5, INK, bold=True)
    p.card(x + 14, y + 34, 150, 58, 'Orders', 'Tỷ lệ trễ', 34, INK, LIGHT, flt)
    p.card(x + 14, y + 96, 150, 22, 'Orders', 'Nhãn so với trung bình', 7.5, INK2, FONT, flt, formatted=False)
    for index, (label, measure) in enumerate([('Cam kết → thực tế', 'Chữ cam kết thực tế'),
                                              ('Đơn / đơn trễ', 'Chữ đơn và đơn trễ'),
                                              ('Chiếm tổng đơn trễ', 'Chiếm đơn trễ')]):
        ly = y + 12 + index * 26
        p.text(label, x + 182, ly, 112, 20, 9, MUTED)
        p.card(x + 296, ly, 138, 20, 'Orders', measure, 9.5, INK, FONT, flt)
    p.picture(x + 182, y + 96, 252, 17, 'Orders', 'Thanh tỷ lệ trễ', f'Tỷ lệ trễ {mode} so với trung bình', flt)


def stat_tile(p, x, y, w, h, name, big, badge, lines, *, table='PromiseScenarios', size=30, good=False, vertical=False, left=150):
    """Generic raised tile: name, big card, badge and (label, card|text) lines."""
    p.plate(x, y, w, h, radius=16, small=True, face=TEAL if good else FACE)
    ink, soft = (WHITE, '#D9ECEE') if good else (INK, MUTED)
    p.text(name, x + 20, y + 12, 160, 22, 10.5, ink, bold=True)
    big_w = 280 if vertical else left
    p.card(x + 14, y + 34, big_w, 60, table, big, size, ink, LIGHT)
    p.text(badge, x + 20, y + 96, left if not vertical else 260, 18, 7.5, soft, bold=True)
    for index, (label, source) in enumerate(lines):
        if vertical:
            lx, ly, lw, vx, vw = x + 18, y + 124 + index * 26, 116, x + 136, 148
        else:
            lx, ly, lw, vx, vw = (x + left + 32, y + 14 + index * 26, 112, x + left + 146, 138) if left == 150 else (x + left + 32, y + 14 + index * 26, 100, x + left + 134, 110)
        p.text(label, lx, ly, lw, 20, 9, soft)
        if isinstance(source, tuple):
            p.card(vx, ly, vw, 20, source[0], source[1], 9.5, ink, FONT)
        else:
            p.text(source, vx, ly, vw, 20, 9.5, ink, align='right')


def report():
    pages_folder = (REPORT / 'definition/pages').resolve()
    if pages_folder.exists():
        assert pages_folder.is_relative_to((ROOT / 'dashboards/powerbi').resolve())
        shutil.rmtree(pages_folder)
    write(OUT / 'delivery_dashboard.pbip', {'$schema': SCHEMA + 'pbip/pbipProperties/1.0.0/schema.json',
                                            'version': '1.0', 'artifacts': [{'report': {'path': 'Delivery.Report'}}],
                                            'settings': {'enableAutoRecovery': True}})
    write(REPORT / 'definition.pbir', {'$schema': SCHEMA + 'item/report/definitionProperties/2.0.0/schema.json',
                                       'version': '4.0', 'datasetReference': {'byPath': {'path': '../Delivery.SemanticModel'}}})
    write(REPORT / 'definition/version.json', {'$schema': SCHEMA + 'item/report/definition/versionMetadata/1.0.0/schema.json',
                                               'version': '2.0.0'})
    write(REPORT / 'definition/report.json', {
        '$schema': SCHEMA + 'item/report/definition/report/2.1.0/schema.json',
        'themeCollection': {'customTheme': {'name': 'delivery_theme.json', 'reportVersionAtImport': '5.59', 'type': 'RegisteredResources'}},
        'resourcePackages': [{'name': 'RegisteredResources', 'type': 'RegisteredResources',
                              'items': [{'name': 'delivery_theme.json', 'path': 'delivery_theme.json', 'type': 'CustomTheme'}]}],
        'settings': {'useStylableVisualContainerHeader': True, 'exportDataMode': 'AllowSummarized'}})
    write(REPORT / 'StaticResources/RegisteredResources/delivery_theme.json', {
        'name': 'delivery_theme.json', 'dataColors': [TEAL, BRASS, RED, STEEL, '#4A6FB5'],
        'background': FACE, 'foreground': INK, 'tableAccent': TEAL,
        'textClasses': {'title': {'fontFace': FONT, 'fontSize': 11}, 'label': {'fontFace': FONT, 'fontSize': 10},
                        'callout': {'fontFace': LIGHT, 'fontSize': 30}}})
    write(REPORT / 'definition/pages/pages.json', {
        '$schema': SCHEMA + 'item/report/definition/pagesMetadata/1.0.0/schema.json',
        'pageOrder': [identifier(key) for key in PAGE_NAMES], 'activePageName': identifier('overview')})

    # ------------------------------------------------------------------ 1. overview
    p = Page('overview', 'Hiệu suất giao hàng', 'DataCo · đơn không hủy · 01/2015 – 01/2018')
    p.filters([('Phương thức', 'Orders', 'shipping_mode', 172, {'sync': 'shipping_mode'}),
               ('Thị trường', 'Orders', 'market', 172, {'sync': 'market'}),
               ('Vùng giao', 'Orders', 'order_region', 200, {'sync': 'region'})])
    p.tape('Orders', 'Kết luận tổng quan')
    y = 150
    p.plate(X0, y, 340, 290)
    p.text('Tỷ lệ giao trễ', X0 + 20, y + 14, 200, 22, 10.5, INK, bold=True)
    p.picture(X0 + 20, y + 44, 300, 214, 'Orders', 'Vòng tỷ lệ trễ', 'Vòng tiến độ tỷ lệ giao trễ')
    p.card(X0 + 20, y + 260, 150, 22, 'Orders', 'Chữ đơn trễ', 10, MUTED, FONT, formatted=False)
    p.card(X0 + 170, y + 260, 150, 22, 'Orders', 'Chữ đơn đúng hạn', 10, MUTED, FONT, formatted=False)
    for index, mode in enumerate(MODE_ORDER):
        mode_tile(p, X0 + 356 + (index % 2) * 466, y + (index // 2) * 153, mode)
    y = 456
    p.plate(X0, y, 600, 290)
    p.heading(X0 + 20, y + 14, 560, 'Nên ưu tiên phương thức nào?', 'Số đơn (ngang) × tỷ lệ trễ (dọc) · cỡ bong bóng là số đơn trễ')
    p.scatter(X0 + 14, y + 58, 572, 224, ('Orders', 'shipping_mode'), ('Orders', 'Số đơn'), ('Orders', 'Tỷ lệ trễ'), ('Orders', 'Số đơn trễ'), y_end=1.1)
    p.plate(X0 + 616, y, 372, 290)
    p.heading(X0 + 636, y + 14, 330, 'Phương thức × thị trường', 'Mỗi hàng gần như một màu: thị trường ít làm đổi kết quả')
    p.picture(X0 + 632, y + 70, 340, 172, 'Orders', 'Bàn phím nhiệt', 'Tỷ lệ trễ theo phương thức và thị trường')
    p.plate(X0 + 1004, y, 268, 290)
    p.heading(X0 + 1024, y + 14, 228, 'Nhịp độ theo tháng', 'trung bình toàn kỳ · đường nhỏ là từng tháng')
    for index, (label, measure, shade) in enumerate([('Đơn mỗi tháng', 'Đơn mỗi tháng', STEEL),
                                                     ('Giao thực tế TB', 'Thực tế TB', TEAL),
                                                     ('Chênh so với cam kết', 'Chênh lệch cam kết', RED)]):
        ry = y + 66 + index * 72
        p.text(label, X0 + 1024, ry, 118, 16, 8.5, MUTED)
        p.card(X0 + 1020, ry + 20, 120, 34, 'Orders', measure, 20, INK)
        p.line(X0 + 1148, ry + 8, 108, 46, 'Orders', measure, compact=True, color_hex=shade)
    y = 762
    p.plate(X0, y, WIDTH, 206)
    p.heading(X0 + 20, y + 14, 520, 'Diễn biến tỷ lệ trễ theo tháng')
    p.text('trục tự co theo dữ liệu, không bắt đầu từ 0', X0 + 700, y + 16, 552, 18, 8.5, MUTED, align='right')
    p.line(X0 + 14, y + 40, WIDTH - 28, 158, 'Orders', 'Tỷ lệ trễ')

    # ------------------------------------------------------------------ 2. risk
    p = Page('risk', 'Rủi ro giao trễ', 'Tập kiểm tra · 13.071 đơn · 07/2017 – 01/2018')
    p.hidden_slicer('Orders', 'market', 'market')
    p.filters([('Ngưỡng cảnh báo', 'RiskThreshold', 'Value', 172, {'default': 0.5}),
               ('Phương thức', 'Orders', 'shipping_mode', 172, {'sync': 'shipping_mode'}),
               ('Vùng giao', 'Orders', 'order_region', 200, {'sync': 'region'})])
    p.tape('Orders', 'Kết luận rủi ro')
    y = 150
    for index, (title, sub, ring, left, right) in enumerate([
            ('Độ chính xác', 'đúng / số cảnh báo', 'Vòng độ chính xác', 'Chữ cảnh báo đúng', 'Chữ cảnh báo'),
            ('Độ bao phủ', 'bắt được / đơn trễ', 'Vòng độ bao phủ', 'Chữ bắt được', 'Chữ đơn trễ test')]):
        x = X0 + index * 332
        p.plate(x, y, 316, 296)
        p.text(title, x + 20, y + 14, 130, 22, 10.5, INK, bold=True)
        p.text(sub, x + 150, y + 16, 146, 18, 8.5, MUTED, align='right')
        p.picture(x + 20, y + 46, 276, 197, 'Orders', ring, f'Vòng tiến độ {title.lower()}')
        p.card(x + 20, y + 256, 128, 22, 'Orders', left, 10, MUTED, FONT, formatted=False)
        p.card(x + 168, y + 256, 128, 22, 'Orders', right, 10, MUTED, FONT, formatted=False)
    p.plate(X0 + 664, y, 608, 296)
    p.heading(X0 + 684, y + 14, 568, 'Phễu phát hiện đơn trễ', 'Từ toàn bộ đơn kiểm tra đến cảnh báo đúng')
    p.picture(X0 + 684, y + 58, 568, 192, 'Orders', 'Phễu phát hiện', 'Phễu phát hiện đơn trễ')
    p.card(X0 + 684, y + 258, 568, 22, 'Orders', 'Chữ cảnh báo sai', 9.5, MUTED, FONT, formatted=False)
    y = 462
    for index, (label, measure, shade) in enumerate([('Cảnh báo đúng', 'Cảnh báo đúng', TEAL), ('Cảnh báo sai', 'Cảnh báo sai', BRASS),
                                                     ('Đơn trễ bị bỏ sót', 'Bỏ sót', RED), ('Đơn trễ thực tế', 'Đơn trễ test', STEEL)]):
        x = X0 + index * 322
        share = ['Cảnh báo đúng trên đơn test', 'Cảnh báo sai trên đơn test', 'Bỏ sót trên đơn test', 'Đơn trễ trên đơn test'][index]
        p.plate(x, y, 306, 92, radius=16, small=True)
        p.blank(x + 14, y + 22, 8, 48, shade, 4, None)
        p.text(label, x + 36, y + 12, 150, 16, 9, MUTED)
        p.card(x + 30, y + 32, 150, 46, 'Orders', measure, 26, INK)
        p.card(x + 196, y + 28, 96, 26, 'Orders', share, 11, INK2, FONT)
        p.text('tổng đơn kiểm tra', x + 196, y + 54, 96, 16, 7.5, MUTED, align='center')
    y = 570
    p.plate(X0, y, 780, 330)
    p.heading(X0 + 20, y + 14, 600, 'Cảnh báo và bỏ sót theo phương thức', 'Số đơn trên tập kiểm tra')
    p.bar('', 'Orders', 'shipping_mode', [('Orders', 'Cảnh báo đúng', 'Cảnh báo đúng'), ('Orders', 'Cảnh báo sai', 'Cảnh báo sai'),
                                          ('Orders', 'Bỏ sót', 'Bỏ sót')], X0 + 14, y + 58, 752, 262, stacked=True)
    p.plate(X0 + 796, y, 476, 330)
    p.heading(X0 + 816, y + 14, 436, 'Chất lượng mô hình', 'Toàn tập kiểm tra, không đổi theo bộ lọc vùng')
    p.table('', [('ModelMetrics', 'model_label'), ('ModelMetrics', 'AUC ngoài mẫu', True, 'ROC-AUC'),
                 ('ModelMetrics', 'AP ngoài mẫu', True, 'AP'), ('ModelMetrics', 'Log loss ngoài mẫu', True, 'Log loss')],
            X0 + 812, y + 64, 444, 200, weights=[0.37, 0.21, 0.21, 0.21])

    # ------------------------------------------------------------------ 3. promises
    p = Page('promises', 'Phương án cam kết', 'Mô phỏng · 13.071 đơn kiểm tra · giữ nguyên thời gian giao thực tế')
    p.hidden_slicer('Orders', 'market', 'market')
    p.filters([('Phương án đang xem', 'PolicySelector', 'policy_label', 210, {'default': 'Thêm một ngày'}),
               ('Phương thức', 'Orders', 'shipping_mode', 172, {'sync': 'shipping_mode'}),
               ('Vùng giao', 'Orders', 'order_region', 200, {'sync': 'region'})])
    p.tape('PromiseScenarios', 'Kết luận cam kết')
    y = 150
    p.plate(X0, y, 340, 282)
    p.text('Tỷ lệ vượt hẹn tính lại', X0 + 20, y + 14, 176, 22, 10.5, INK, bold=True)
    p.card(X0 + 198, y + 16, 126, 18, 'PromiseScenarios', 'Chính sách đang xem', 8.5, MUTED, FONT, formatted=False)
    p.picture(X0 + 30, y + 40, 280, 200, 'PromiseScenarios', 'Vòng vượt hẹn', 'Vòng tiến độ tỷ lệ vượt hẹn tính lại')
    p.card(X0 + 20, y + 248, 148, 22, 'PromiseScenarios', 'Chữ hiện tại', 10, MUTED, FONT, formatted=False)
    p.card(X0 + 172, y + 248, 148, 22, 'PromiseScenarios', 'Chữ đơn vượt hẹn', 10, MUTED, FONT, formatted=False)
    tx, ty, tw, th = X0 + 356, y, 450, 133
    stat_tile(p, tx, ty, tw, th, 'Giảm vượt hẹn', 'Giảm vượt hẹn (điểm %)', '▼ SO VỚI HIỆN TẠI',
              [('Hiện tại', ('PromiseScenarios', 'Trễ hiện trạng test')), ('Phương án', ('PromiseScenarios', 'Vượt hẹn tính lại')),
               ('Hết vượt hẹn', ('PromiseScenarios', 'Đơn hết vượt hẹn'))], size=22, good=True, left=190)
    stat_tile(p, tx + 466, ty, tw, th, 'Cam kết mới (TB)', 'Cam kết mới TB', '▲ TĂNG CAM KẾT',
              [('Hiện tại', ('PromiseScenarios', 'Cam kết hiện tại TB')), ('Phương án', ('PromiseScenarios', 'Cam kết mới TB')),
               ('Dùng dự phòng', ('PromiseScenarios', 'Dự phòng'))], size=26, left=190)
    stat_tile(p, tx, ty + 149, tw, th, 'Khách chờ thêm', 'Tăng cam kết TB', '▲ CHI PHÍ CỦA PHƯƠNG ÁN',
              [('Giao thực tế', 'không đổi'), ('Nhóm cao nhất', ('PromiseScenarios', 'Nhóm cần rà soát cam kết')),
               ('Vượt hẹn nhóm', ('PromiseScenarios', 'Vượt hẹn nhóm cao nhất'))], size=26, left=190)
    stat_tile(p, tx + 466, ty + 149, tw, th, 'Đơn trễ thực tế', 'Đơn trễ test', 'TẬP KIỂM TRA',
              [('Giai đoạn', '07/2017 – 01/2018'), ('Vượt hẹn hiện tại', ('PromiseScenarios', 'Trễ hiện trạng test')),
               ('Đơn mô phỏng', ('PromiseScenarios', 'Đơn kịch bản'))], size=30, table='Orders', left=190)
    y = 448
    p.plate(X0, y, 540, 288)
    p.heading(X0 + 20, y + 14, 500, 'Đánh đổi giữa vượt hẹn và ngày chờ thêm', 'Mỗi bong bóng là một phương án · càng sang phải khách càng chờ lâu')
    p.scatter(X0 + 14, y + 58, 512, 222, ('Policies', 'policy_label'), ('PromiseScenarios', 'Tăng cam kết TB'),
              ('PromiseScenarios', 'Vượt hẹn tính lại'))
    p.plate(X0 + 556, y, 716, 288)
    p.heading(X0 + 576, y + 14, 676, 'So sánh các phương án', 'Luôn hiện đủ năm phương án; thẻ và biểu đồ đi theo lựa chọn đang xem')
    p.table('', [('Policies', 'policy_label'), ('PromiseScenarios', 'Vượt hẹn tính lại', True, 'Vượt hẹn'),
                 ('PromiseScenarios', 'Cam kết mới TB', True, 'Cam kết'), ('PromiseScenarios', 'Tăng cam kết TB', True, 'Tăng thêm')],
            X0 + 572, y + 60, 684, 216, weights=[0.40, 0.20, 0.20, 0.20])
    y = 752
    p.plate(X0, y, WIDTH, 236)
    p.heading(X0 + 20, y + 14, 700, 'Cam kết theo phương thức', 'Tăng cam kết không có nghĩa là giao nhanh hơn')
    p.table('', [('Orders', 'shipping_mode'), ('PromiseScenarios', 'Trễ hiện trạng test', True, 'Vượt hẹn hiện tại'),
                 ('PromiseScenarios', 'Vượt hẹn tính lại', True, 'Vượt hẹn phương án'),
                 ('PromiseScenarios', 'Cam kết hiện tại TB', True, 'Cam kết hiện tại'),
                 ('PromiseScenarios', 'Cam kết mới TB', True, 'Cam kết mới'),
                 ('PromiseScenarios', 'Tăng cam kết TB', True, 'Tăng thêm')],
            X0 + 16, y + 58, WIDTH - 32, 170, weights=[0.20, 0.16, 0.16, 0.16, 0.16, 0.16], row_padding=3)

    # ------------------------------------------------------------------ 4. routing
    with (ROOT / 'data/dashboard/route_cases.csv').open(encoding='utf-8-sig') as stream:
        cases = list(csv.DictReader(stream))
    default_case = next(row['case_label'] for row in cases if row['case_id'] == 'c101|base|ortools')
    p = Page('routing', 'Tuyến giao và nhiên liệu', 'Bộ bài toán Solomon · phương án đã tính')
    p.filters([('Phương án tuyến', 'RouteCases', 'case_label', 300, {'default': default_case, 'sync': 'route_case'}),
               ('Km / đơn vị', 'KmPerUnit', 'Value', 112, {'default': 1, 'sync': 'km'}),
               ('Lít / 100 km', 'FuelConsumption', 'Value', 112, {'default': 10, 'sync': 'fuel_consumption'}),
               ('VND / lít', 'FuelPrice', 'Value', 136, {'default': 22000, 'sync': 'fuel_price'})], reset=False)
    p.tape('RouteCases', 'Kết luận tuyến')
    y = 150
    p.plate(X0, y, 640, 462)
    p.heading(X0 + 20, y + 14, 300, 'Sơ đồ tuyến theo xe')
    p.text('tọa độ Solomon, không phải đường bộ', X0 + 320, y + 16, 300, 18, 8.5, MUTED, align='right')
    p.well(X0 + 12, y + 44, 616, 408, radius=14)
    p.picture(X0 + 16, y + 48, 608, 400, 'RouteCases', 'Bản đồ tuyến', 'Các tuyến theo thứ tự phục vụ, bắt đầu và kết thúc tại kho')
    rx = X0 + 656
    stat_tile(p, rx, y, 300, 223, 'Nhiên liệu mô phỏng', 'Nhiên liệu mô phỏng', 'VND · GIẢ ĐỊNH, KHÔNG PHẢI SỐ ĐO',
              [('Tiêu hao', ('RouteCases', 'Chữ tiêu hao')), ('Giá nhiên liệu', ('RouteCases', 'Chữ giá nhiên liệu')),
               ('Quy đổi', ('RouteCases', 'Chữ quy đổi'))], table='RouteCases', size=30, vertical=True)
    stat_tile(p, rx + 316, y, 300, 223, 'Xe sử dụng', 'Số xe sử dụng', 'XE TRONG PHƯƠNG ÁN',
              [('Tải trọng', ('RouteCases', 'Chữ tải trọng')), ('Giới hạn', ('RouteCases', 'Chữ xe tối đa'))],
              table='RouteCases', size=30, vertical=True)
    stat_tile(p, rx, y + 239, 300, 223, 'Quãng đường chuẩn', 'Quãng đường benchmark', 'ĐƠN VỊ TỌA ĐỘ SOLOMON',
              [('Lưu ý', 'không phải km đường bộ')], table='RouteCases', size=30, vertical=True)
    stat_tile(p, rx + 316, y + 239, 300, 223, 'Giảm quãng đường', 'Giảm quãng đường', '▼ SO VỚI ĐIỂM GẦN NHẤT',
              [('Đối chứng', 'cùng cấu hình')], table='RouteCases', size=30, good=True, vertical=True)
    y = 628
    p.plate(X0, y, 420, 330)
    p.heading(X0 + 20, y + 14, 380, 'Quãng đường cùng cấu hình', 'Đơn vị tọa độ · chỉ so sánh khi có lời giải khả thi')
    p.bar('', 'RouteMethods', 'method_label', [('RouteCases', 'Quãng đường đối chiếu', 'Quãng đường')], X0 + 14, y + 58, 392, 260, legend=False)
    p.plate(X0 + 436, y, 836, 330)
    p.heading(X0 + 456, y + 14, 700, 'Đội xe và tính khả thi')
    p.table('', [('RouteMethods', 'method_label'), ('RouteCases', 'Xe đối chiếu', True, 'Xe'),
                 ('RouteCases', 'Trạng thái đối chiếu', True, 'Kết quả')], X0 + 452, y + 50, 804, 200, weights=[0.40, 0.20, 0.40])
    p.action_button('Xem lịch trình chi tiết  ›', X0 + 452, y + 266, 804, 46, destination='routing_detail', tone=TEAL)

    # ------------------------------------------------------------------ 5. route detail (hidden)
    p = Page('routing_detail', 'Lịch trình tuyến', 'Bộ bài toán Solomon · điểm 0 là kho', hidden=True, active='routing')
    p.hidden_slicer('KmPerUnit', 'Value', 'km')
    p.hidden_slicer('FuelConsumption', 'Value', 'fuel_consumption')
    p.hidden_slicer('FuelPrice', 'Value', 'fuel_price')
    x = RIGHT - 100
    p.action_button('Về trang tuyến', x, 16, 100, 72, destination='routing', tone=TEAL)
    p.slicer('Xe', 'RouteStops', 'vehicle', x - 12 - 200, 200)
    p.slicer('Phương án tuyến', 'RouteCases', 'case_label', x - 12 - 200 - 12 - 300, 300, default=default_case, sync='route_case')
    p.tape('RouteCases', 'Kết luận tuyến')
    for index, (label, measure) in enumerate([('Nhiên liệu mô phỏng (VND)', 'Nhiên liệu mô phỏng'), ('Xe sử dụng', 'Số xe sử dụng'),
                                              ('Quãng đường chuẩn', 'Quãng đường benchmark'), ('Giảm quãng đường', 'Giảm quãng đường')]):
        cx = X0 + index * 322
        p.plate(cx, 150, 306, 96, radius=16, small=True)
        p.text(label, cx + 20, 160, 266, 18, 9, MUTED)
        p.card(cx + 14, 180, 278, 56, 'RouteCases', measure, 28, INK)
    p.plate(X0, 262, 620, 710)
    p.heading(X0 + 20, 276, 560, 'Thứ tự phục vụ')
    p.table('', [('RouteStops', 'vehicle'), ('RouteStops', 'sequence'), ('RouteStops', 'node'), ('RouteStops', 'x'), ('RouteStops', 'y')],
            X0 + 16, 316, 588, 640, weights=[0.16, 0.18, 0.22, 0.22, 0.22])
    p.plate(X0 + 636, 262, 636, 710)
    p.heading(X0 + 656, 276, 560, 'Toàn bộ phương án', 'Sơ đồ hiển thị mọi xe trong phương án')
    p.well(X0 + 648, 318, 612, 640, radius=14)
    p.picture(X0 + 652, 322, 604, 632, 'RouteCases', 'Bản đồ tuyến', 'Toàn bộ các tuyến của phương án đang chọn')


def main():
    report()


if __name__ == '__main__':
    main()
