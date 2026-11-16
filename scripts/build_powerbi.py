"""Build the native Power BI model and its executive presentation."""
import uuid

from dss_bi_delivery.powerbi_model import MEASURES, TABLES, MODEL, REPORT, SCHEMA, model, write
from dss_bi_delivery.powerbi_report import report


def main():
    model()
    report()
    for folder, kind in [(REPORT, 'Report'), (MODEL, 'SemanticModel')]:
        write(folder/'.platform', {
            '$schema': SCHEMA+'gitIntegration/platformProperties/2.0.0/schema.json',
            'metadata': {'type': kind, 'displayName': 'Delivery Insights'},
            'config': {'version': '2.0', 'logicalId': str(uuid.uuid5(uuid.NAMESPACE_URL, 'delivery/'+kind))},
        })
    print('Built four management pages, a route detail page and the native model.')


if __name__ == '__main__':
    main()
