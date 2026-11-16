"""Data-driven SVG route maps for native Power BI image visuals."""
from __future__ import annotations

from urllib.parse import quote
import pandas as pd

ROUTE_COLORS = [
    '#0B7D7A', '#3B637D', '#B87842', '#638D79', '#8A697C',
    '#477F9A', '#A09258', '#755C48', '#5A7191', '#567664',
]


def route_svg(stops: pd.DataFrame) -> str:
    """Draw only verified stops and depot-to-depot routes, without real-world map claims."""
    width, height = 760, 500
    if stops.empty:
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="760" height="500">'
               '<rect width="760" height="500" fill="#F8FAFA"/>'
               '<text x="380" y="225" text-anchor="middle" font-family="Segoe UI" '
               'font-size="22" fill="#435969">Chưa có tuyến khả thi để hiển thị</text>'
               '<text x="380" y="260" text-anchor="middle" font-family="Segoe UI" '
               'font-size="16" fill="#687A86">Không quy kết quả thiếu thành quãng đường bằng 0</text></svg>')
        return 'data:image/svg+xml;utf8,' + quote(svg, safe='')
    xmin, xmax = float(stops.x.min()) - 6, float(stops.x.max()) + 6
    ymin, ymax = float(stops.y.min()) - 6, float(stops.y.max()) + 6
    scale = min(656 / max(1, xmax - xmin), 376 / max(1, ymax - ymin))
    xoffset = (width - (xmax - xmin) * scale) / 2
    yoffset = (height - 48 - (ymax - ymin) * scale) / 2

    def point(x, y):
        return xoffset + (x - xmin) * scale, yoffset + (ymax - y) * scale

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             '<rect width="760" height="500" rx="10" fill="#F8FAFA"/>']
    for value in range(0, 101, 20):
        x, _ = point(value, ymin)
        _, y = point(xmin, value)
        if 34 < x < 726:
            parts.append(f'<path d="M{x:.1f} 28V428" stroke="#E6ECEC" stroke-width="1"/>')
        if 28 < y < 428:
            parts.append(f'<path d="M34 {y:.1f}H726" stroke="#E6ECEC" stroke-width="1"/>')
    vehicles = sorted(stops.vehicle.unique(), key=lambda value: int(value))
    color_map = {vehicle: ROUTE_COLORS[index % len(ROUTE_COLORS)] for index, vehicle in enumerate(vehicles)}
    for vehicle, route in stops.groupby('vehicle', sort=True):
        route = route.sort_values('sequence')
        points = [point(float(row.x), float(row.y)) for row in route.itertuples()]
        color = color_map[vehicle]
        coords = ' '.join(f'{x:.1f},{y:.1f}' for x, y in points)
        parts.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="2.2" opacity="0.8" stroke-linejoin="round"/>')
        for row, (x, y) in zip(route.itertuples(), points):
            if row.node != 0:
                parts.append(f'<circle class="stop" cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{color}" stroke="white" stroke-width="0.8"/>')
    depot = stops.loc[stops.node.eq(0)].iloc[0]
    x, y = point(float(depot.x), float(depot.y))
    vehicles = sorted(stops.vehicle.unique(), key=lambda value: int(value))
    for index, vehicle in enumerate(vehicles):
        xlegend, ylegend = 28 + (index % 10) * 72, 432 + (index // 10) * 18
        fill = color_map[vehicle]
        parts.append(f'<circle class="legend" cx="{xlegend}" cy="{ylegend}" r="3" fill="{fill}"/>')
        parts.append(f'<text x="{xlegend+8}" y="{ylegend+4}" font-family="Segoe UI" font-size="12" fill="#435969">Xe {vehicle}</text>')
    parts.extend([
        f'<rect x="{x - 6:.1f}" y="{y - 6:.1f}" width="12" height="12" rx="2" fill="#142D3B" stroke="white" stroke-width="2"/>',
        f'<text x="{x + 12:.1f}" y="{y - 8:.1f}" font-family="Segoe UI" font-size="15" font-weight="600" fill="#142D3B">Kho</text>',
        '<text x="28" y="490" font-family="Segoe UI" font-size="13" fill="#687A86">Mỗi màu là một xe. Đường nối theo thứ tự phục vụ.</text>',
        '</svg>',
    ])
    uri = 'data:image/svg+xml;utf8,' + quote(''.join(parts), safe='')
    if len(uri) >= 32766:
        raise ValueError('Route image exceeds the native Power BI text field limit')
    return uri
