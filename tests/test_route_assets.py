"""Verify route geometry and color identities, rather than a screenshot snapshot."""
import unittest
from urllib.parse import unquote
from xml.etree import ElementTree as ET

import pandas as pd

from dss_bi_delivery.route_assets import route_svg


class RouteImageContract(unittest.TestCase):
    def test_vehicle_colors_and_order_survive_string_vehicle_ids(self):
        rows = []
        for vehicle in ['1', '10', '2']:
            for sequence, node, x, y in [(2, 0, 0, 0), (0, 0, 0, 0), (1, int(vehicle), int(vehicle), 15)]:
                rows.append(dict(vehicle=vehicle, sequence=sequence, node=node, x=x, y=y))
        uri = route_svg(pd.DataFrame(rows))
        self.assertLess(len(uri), 32766)
        root = ET.fromstring(unquote(uri.split(',', 1)[1]))
        ns = {'s': 'http://www.w3.org/2000/svg'}
        paths = root.findall('s:polyline', ns)
        legend = root.findall("s:circle[@class='legend']", ns)
        # Paths are emitted in source string order; legend uses numeric order.
        self.assertEqual([p.attrib['stroke'] for p in paths], [legend[i].attrib['fill'] for i in [0, 2, 1]])
        self.assertEqual(len(root.findall("s:circle[@class='stop']", ns)), 3)
        for path in paths:
            points = path.attrib['points'].split()
            self.assertEqual(points[0], points[-1])
            self.assertNotEqual(points[0], points[1])

    def test_unsolved_case_is_an_empty_state_not_an_old_route(self):
        uri = route_svg(pd.DataFrame())
        root = ET.fromstring(unquote(uri.split(',', 1)[1]))
        self.assertIn('Chưa có tuyến khả thi', ''.join(root.itertext()))
        self.assertEqual(len(root.findall('{http://www.w3.org/2000/svg}polyline')), 0)


if __name__ == '__main__':
    unittest.main()
