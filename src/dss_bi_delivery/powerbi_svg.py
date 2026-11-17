"""Data-driven SVG measures for native Power BI image visuals.

Each function returns a DAX expression that builds a percent-encoded SVG data URI,
so the picture follows the report filters exactly like the route map does.
"""
from __future__ import annotations

import math
import re
from urllib.parse import quote

SAFE = "/:;=,'.-_*!~"

# Palette shared with powerbi_report.py (light "control panel" theme).
INK, INK2, MUTED = '#1D2A33', '#45545E', '#5E6D76'
FACE1, FACE2, WELL1, WELL2 = '#F1EEE7', '#DAD6CC', '#D3CFC4', '#E8E5DD'
RED, TEAL, BRASS, STEEL = '#D2472A', '#0E7C86', '#B8860B', '#8E9AA3'
SHADOW = '#686044'


def _rgb(value: str):
    return [int(value[i:i + 2], 16) for i in (1, 3, 5)]


def mix(a: str, b: str, t: float) -> str:
    x, y = _rgb(a), _rgb(b)
    return '#%02X%02X%02X' % tuple(round(p + (q - p) * t) for p, q in zip(x, y))


def dax_svg(template: str, prefix: bool = True, **exprs: str) -> str:
    """Turn an SVG template with {name} placeholders into a DAX string expression."""
    pieces = re.split(r'\{(\w+)\}', template)
    out = ['"data:image/svg+xml;utf8,"'] if prefix else []
    for index, piece in enumerate(pieces):
        if index % 2 == 0:
            if piece:
                out.append('"' + quote(piece, safe=SAFE) + '"')
        else:
            out.append(exprs[piece])
    return ' & '.join(out)


def num(expression: str, pattern: str = '0.0') -> str:
    return f'FORMAT({expression}, "{pattern}", "en-US")'


def _shadow_filter(fid: str, dx=4, dy=5, blur=4, opacity=.42) -> str:
    return (f'<filter id="{fid}" x="-30%" y="-30%" width="160%" height="160%">'
            f'<feDropShadow dx="{dx}" dy="{dy}" stdDeviation="{blur}" flood-color="{SHADOW}" flood-opacity="{opacity}"/></filter>')


# --------------------------------------------------------------------------- logo
def logo_expression() -> str:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="72" height="72" viewBox="0 0 72 72">
<defs>
<linearGradient id="b" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{FACE1}"/><stop offset="1" stop-color="{FACE2}"/></linearGradient>
{_shadow_filter('s', 3, 4, 3.5, .45)}
</defs>
<g filter="url(#s)"><rect x="6" y="6" width="60" height="60" rx="20" fill="url(#b)"/></g>
<rect x="12" y="12" width="48" height="48" rx="15" fill="none" stroke="{SHADOW}" stroke-opacity=".22" stroke-width="2"/>
<g transform="translate(36 38)">
<polygon points="0,-17 15,-8.5 0,0 -15,-8.5" fill="{mix(TEAL, '#FFFFFF', .55)}"/>
<polygon points="-15,-8.5 0,0 0,17 -15,8.5" fill="{TEAL}"/>
<polygon points="15,-8.5 0,0 0,17 15,8.5" fill="#0A636B"/>
<path d="M-15,-8.5 L0,0 L15,-8.5 M0,0 V17" fill="none" stroke="#FFFFFF" stroke-opacity=".5" stroke-width="1"/>
<path d="M-8,-4.2 L6,3.8" stroke="#FFFFFF" stroke-opacity=".85" stroke-width="2" stroke-linecap="round" stroke-dasharray="1 4"/>
<circle cx="14" cy="-14" r="6" fill="{RED}" stroke="{FACE1}" stroke-width="2.2"/>
</g></svg>'''
    return dax_svg(svg)


# --------------------------------------------------------------------------- ring
def ring_expression(value: str, color: str, caption: str) -> str:
    cx, cy, radius, stroke = 150, 107, 70, 24
    outer = radius + stroke / 2
    ticks = []
    for i in range(40):
        angle = math.radians(i * 9 - 90)
        major = i % 10 == 0
        r1, r2 = outer + 6, outer + (15 if major else 11 if i % 5 == 0 else 9)
        ticks.append(f'<line x1="{cx + r1 * math.cos(angle):.1f}" y1="{cy + r1 * math.sin(angle):.1f}" '
                     f'x2="{cx + r2 * math.cos(angle):.1f}" y2="{cy + r2 * math.sin(angle):.1f}" '
                     f'stroke="{INK2}" stroke-width="{1.8 if major else 1}" opacity="{.7 if major else .35}"/>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="214" viewBox="0 0 300 214">
<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{mix(color, '#FFFFFF', .42)}"/><stop offset=".5" stop-color="{color}"/><stop offset="1" stop-color="{mix(color, '#000000', .25)}"/></linearGradient>
<radialGradient id="k" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="{FACE1}"/><stop offset="1" stop-color="{FACE2}"/></radialGradient>
{_shadow_filter('s', 4, 5, 4, .42)}
</defs>
{''.join(ticks)}
<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{WELL1}" stroke-width="{stroke}"/>
<circle cx="{cx}" cy="{cy}" r="{outer - 1}" fill="none" stroke="{SHADOW}" stroke-opacity=".45" stroke-width="2.2"/>
<circle cx="{cx}" cy="{cy}" r="{radius - stroke / 2 + 1}" fill="none" stroke="#FFFFFF" stroke-opacity=".8" stroke-width="2.2"/>
<g filter="url(#s)"><circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="url(#g)" stroke-width="{stroke - 8}" stroke-linecap="round" stroke-dasharray="{{dash}} 440" transform="rotate(-90 {cx} {cy})"/></g>
<g transform="rotate({{ang}} {cx} {cy})"><g filter="url(#s)"><circle cx="{cx}" cy="{cy - radius}" r="{stroke / 2 + 1}" fill="url(#k)"/></g><circle cx="{cx}" cy="{cy - radius}" r="4" fill="{color}"/></g>
<g filter="url(#s)"><circle cx="{cx}" cy="{cy}" r="{radius - stroke / 2 - 9}" fill="url(#k)"/></g>
<text x="{cx}" y="{cy + 5}" text-anchor="middle" font-family="Segoe UI Light, Segoe UI" font-size="30" fill="{color}">{{txt}}</text>
<text x="{cx}" y="{cy + 22}" text-anchor="middle" font-family="Segoe UI" font-size="10" fill="{MUTED}">{caption}</text>
</svg>'''
    body = dax_svg(svg, dash=num('v * 439.82'), ang=num('v * 360'), txt='txt')
    return (f'VAR raw = {value}\nVAR v = MAX(0, MIN(1, COALESCE(raw, 0)))\n'
            f'VAR txt = IF(ISBLANK(raw), "–", SUBSTITUTE(FORMAT(v, "0.0%", "vi-VN"), "%", "%25"))\nRETURN {body}')


# --------------------------------------------------------------------------- thermometer
def thermometer_expression(value: str) -> str:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="44" height="250" viewBox="0 0 44 250">
<defs>
<linearGradient id="f" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{mix(RED, '#FFFFFF', .5)}"/><stop offset="1" stop-color="{RED}"/></linearGradient>
{_shadow_filter('s', 2, 2, 2, .4)}
</defs>
<rect x="8" y="2" width="28" height="244" rx="14" fill="{WELL1}"/>
<rect x="8" y="2" width="28" height="244" rx="14" fill="none" stroke="{SHADOW}" stroke-opacity=".4" stroke-width="2"/>
<g filter="url(#s)"><rect x="12" y="{{y}}" width="20" height="{{h}}" rx="10" fill="url(#f)"/></g>
<line x1="8" y1="124" x2="36" y2="124" stroke="{INK}" stroke-opacity=".3"/>
</svg>'''
    body = dax_svg(svg, y=num('6 + (1 - v) * 236'), h=num('MAX(4, v * 236)'))
    return f'VAR v = MAX(0, MIN(1, COALESCE({value}, 0)))\nRETURN {body}'


# --------------------------------------------------------------------------- track bar
def track_expression(value: str, average: str) -> str:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="240" height="16" viewBox="0 0 240 16">
<defs>{_shadow_filter('s', 1, 2, 1.5, .4)}</defs>
<rect x="0" y="0" width="240" height="16" rx="8" fill="{WELL1}"/>
<rect x="0.75" y="0.75" width="238.5" height="14.5" rx="7.25" fill="none" stroke="{SHADOW}" stroke-opacity=".35" stroke-width="1.5"/>
<g filter="url(#s)"><rect x="3" y="3" width="{{w}}" height="10" rx="5" fill="{{c}}"/></g>
<rect x="5" y="4" width="{{w2}}" height="2.6" rx="1.3" fill="#FFFFFF" opacity=".38"/>
<rect x="{{n}}" y="0" width="2" height="16" fill="{INK}" opacity=".55"/>
</svg>'''
    colour = f'IF(v > a, "%23{RED[1:]}", "%23{TEAL[1:]}")'
    body = dax_svg(svg, w=num('MAX(4, v * 234)'), w2=num('MAX(2, v * 234 - 4)'), c=colour, n=num('2 + a * 234'))
    return (f'VAR v = MAX(0, MIN(1, COALESCE({value}, 0)))\nVAR a = MAX(0, MIN(1, COALESCE({average}, 0)))\n'
            f'RETURN {body}')


# --------------------------------------------------------------------------- heat keypad
MODES = ['First Class', 'Second Class', 'Same Day', 'Standard Class']
MARKETS = ['Africa', 'Europe', 'LATAM', 'Pacific Asia', 'USCA']


def keypad_expression(rate: str, mode_column: str, market_column: str) -> str:
    head_cols = ''.join(
        f'<text x="{92 + i * 49 + 22}" y="12" text-anchor="middle" font-family="Segoe UI" font-size="9.5" fill="{MUTED}">{name if name != "Pacific Asia" else "P. Asia"}</text>'
        for i, name in enumerate(MARKETS))
    head_rows = ''.join(
        f'<text x="0" y="{24 + i * 36 + 15}" font-family="Segoe UI" font-size="11.5" font-weight="600" fill="{INK2}">{name}</text>'
        for i, name in enumerate(MODES))
    frame = (f'<svg xmlns="http://www.w3.org/2000/svg" width="340" height="172" viewBox="0 0 340 172">'
             f'<defs>{_shadow_filter("s", 2, 3, 2.5, .42)}</defs>{head_cols}{head_rows}')
    cell = ('<g filter="url(#s)"><rect x="{x}" y="{y}" width="44" height="30" rx="9" fill="rgb({r},{g},{b})"/></g>'
            f'<text x="{{tx}}" y="{{ty}}" text-anchor="middle" font-family="Segoe UI" font-size="12" font-weight="700" fill="{{ink}}">{{txt}}</text>')
    cell_dax = dax_svg(cell, prefix=False, x='FORMAT(92 + [ci] * 49, "0", "en-US")', y='FORMAT(20 + [ri] * 36, "0", "en-US")',
                       r='FORMAT(rr, "0", "en-US")', g='FORMAT(gg, "0", "en-US")', b='FORMAT(bb, "0", "en-US")',
                       tx='FORMAT(92 + [ci] * 49 + 22, "0", "en-US")', ty='FORMAT(20 + [ri] * 36 + 20, "0", "en-US")',
                       ink='IF(strong, "%23FFFFFF", "%231D2A33")',
                       txt='SUBSTITUTE(FORMAT(v, "0%", "vi-VN"), "%", "%25")')
    face = _rgb('#EFECE5')
    red, teal = _rgb(RED), _rgb(TEAL)
    cells = f'''VAR grid = ADDCOLUMNS(
    CROSSJOIN(VALUES({mode_column}), VALUES({market_column})),
    "ri", SWITCH({mode_column}, "First Class", 0, "Second Class", 1, "Same Day", 2, "Standard Class", 3, 4),
    "ci", SWITCH({market_column}, "Africa", 0, "Europe", 1, "LATAM", 2, "Pacific Asia", 3, "USCA", 4, 5),
    "val", {rate})'''
    per_cell = f'''CONCATENATEX(FILTER(grid, NOT ISBLANK([val])),
    VAR v = [val]
    VAR hot = v >= baseline
    VAR t = IF(hot, MIN(1, DIVIDE(v - baseline, 1 - baseline)) * 0.95, MIN(1, DIVIDE(baseline - v, baseline - 0.38)) * 0.85)
    VAR rr = ROUND({face[0]} + (IF(hot, {red[0]}, {teal[0]}) - {face[0]}) * t, 0)
    VAR gg = ROUND({face[1]} + (IF(hot, {red[1]}, {teal[1]}) - {face[1]}) * t, 0)
    VAR bb = ROUND({face[2]} + (IF(hot, {red[2]}, {teal[2]}) - {face[2]}) * t, 0)
    VAR strong = v > 0.7 || v < 0.45
    RETURN {cell_dax}, "")'''
    return (f'{cells}\nVAR baseline = COALESCE({rate}, 0.57)\n'
            f'RETURN {dax_svg(frame)} & {per_cell} & "%3C/svg%3E"')


# --------------------------------------------------------------------------- detection funnel
def funnel_expression(total: str, late: str, caught: str, missed: str) -> str:
    rows = [('late', 'đơn trễ thực tế', BRASS, INK), ('caught', 'cảnh báo đúng', TEAL, '#FFFFFF'), ('missed', 'bỏ sót', RED, '#FFFFFF')]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="592" height="200" viewBox="0 0 592 200"><defs>{_shadow_filter("s", 2, 3, 2.5, .4)}</defs>']
    labels = [('tot', 'đơn kiểm tra', STEEL, INK)] + rows
    for i, (key, caption, fill, ink) in enumerate(labels):
        y = 4 + i * 48
        parts.append(f'<text x="0" y="{y + 15}" font-family="Segoe UI" font-size="16" font-weight="600" fill="{INK}">{{n_{key}}}</text>')
        parts.append(f'<text x="0" y="{y + 31}" font-family="Segoe UI" font-size="11" fill="{MUTED}">{caption}</text>')
        parts.append(f'<rect x="136" y="{y}" width="456" height="32" rx="11" fill="{WELL1}"/>')
        parts.append(f'<rect x="136.75" y="{y + .75}" width="454.5" height="30.5" rx="10.25" fill="none" stroke="{SHADOW}" stroke-opacity=".35" stroke-width="1.5"/>')
        parts.append(f'<g filter="url(#s)"><rect x="140" y="{y + 4}" width="{{w_{key}}}" height="24" rx="8" fill="{fill}"/></g>')
        parts.append(f'<text x="152" y="{y + 20}" font-family="Segoe UI" font-size="11.5" font-weight="700" fill="{ink}">{{p_{key}}}</text>')
    parts.append('</svg>')
    exprs = {}
    for key, source in (('tot', 'tot'), ('late', 'late'), ('caught', 'caught'), ('missed', 'missed')):
        exprs[f'n_{key}'] = f'FORMAT({source}, "#,0", "vi-VN")'
        exprs[f'w_{key}'] = num(f'MAX(6, DIVIDE({source}, tot) * 448)')
        exprs[f'p_{key}'] = f'SUBSTITUTE(FORMAT(DIVIDE({source}, tot), "0.0%", "vi-VN"), "%", "%25")'
    body = dax_svg(''.join(parts), **exprs)
    return (f'VAR tot = COALESCE({total}, 0)\nVAR late = COALESCE({late}, 0)\nVAR caught = COALESCE({caught}, 0)\n'
            f'VAR missed = COALESCE({missed}, 0)\nRETURN IF(tot = 0, BLANK(), {body})')
