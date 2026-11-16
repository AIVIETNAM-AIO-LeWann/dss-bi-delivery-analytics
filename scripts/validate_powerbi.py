"""Validate PBIR against Microsoft's public schemas, then check model references/layout."""
from pathlib import Path
from urllib.parse import urljoin, urldefrag
from urllib.request import urlopen
import argparse
import hashlib
import json

from jsonschema import Draft7Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'dashboards/powerbi'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--schema-cache', type=Path, default=ROOT/'.cache/powerbi-schemas')
    args = parser.parse_args()
    args.schema_cache.mkdir(parents=True, exist_ok=True)
    def retrieve(uri):
        uri = urldefrag(uri)[0]
        if not uri.startswith('https://developer.microsoft.com/json-schemas/'):
            raise ValueError(f'Unexpected schema host: {uri}')
        cache = args.schema_cache/(hashlib.sha256(uri.encode()).hexdigest()+'.json')
        if not cache.exists():
            with urlopen(uri, timeout=25) as response:
                cache.write_bytes(response.read())
        schema = json.loads(cache.read_text(encoding='utf-8-sig'))
        return Resource.from_contents(schema)
    registry = Registry(retrieve=retrieve)
    checked = 0
    for path in BASE.rglob('*'):
        if not path.is_file() or (path.suffix not in {'.json','.pbip','.pbir','.pbism'} and path.name != '.platform') or '.pbi' in path.parts:
            continue
        data = json.loads(path.read_text(encoding='utf-8'))
        if '$schema' in data:
            schema = retrieve(data['$schema']).contents
            errors = list(Draft7Validator(schema, registry=registry).iter_errors(data))
            if errors:
                raise ValueError(f'{path}: '+str(errors[0]))
            checked += 1
    model = json.loads((BASE/'Delivery.SemanticModel/model.bim').read_text(encoding='utf-8'))['model']
    tables = {table['name']:table for table in model['tables']}
    refs = {name:{'Column':{c['name'] for c in table['columns']},'Measure':{m['name'] for m in table.get('measures',[])}} for name,table in tables.items()}
    def inspect(value, source_map=None):
        source_map = dict(source_map or {})
        if isinstance(value,dict):
            source_map.update({item['Name']:item['Entity'] for item in value.get('From', []) if 'Entity' in item})
            for kind in ['Column','Measure']:
                if kind in value:
                    expression = value[kind]
                    source_ref = expression['Expression']['SourceRef']
                    entity = source_ref.get('Entity') or source_map.get(source_ref.get('Source'))
                    prop = expression['Property']
                    if entity not in refs or prop not in refs[entity][kind]:
                        raise ValueError(f'Broken visual field: {entity}.{prop}')
            for child in value.values(): inspect(child, source_map)
        elif isinstance(value,list):
            for child in value: inspect(child, source_map)
    page_folder = BASE/'Delivery.Report/definition/pages'
    page_metadata = json.loads((page_folder/'pages.json').read_text(encoding='utf-8'))
    page_names = {json.loads(p.read_text(encoding='utf-8'))['name'] for p in page_folder.glob('*/page.json')}
    assert page_metadata['activePageName'] in page_names
    assert set(page_metadata['pageOrder']) == page_names
    visual_count = 0
    for page in (BASE/'Delivery.Report/definition/pages').glob('*/page.json'):
        dimensions = json.loads(page.read_text(encoding='utf-8'))
        boxes = []
        for visual in (page.parent/'visuals').glob('*/visual.json'):
            data = json.loads(visual.read_text(encoding='utf-8'))
            inspect(data)
            box = data['position']
            assert box['x'] >= 0 and box['y'] >= 0
            assert box['x']+box['width'] <= dimensions['width']
            assert box['y']+box['height'] <= dimensions['height']
            for previous in boxes:
                overlaps = box['x'] < previous['x']+previous['width'] and previous['x'] < box['x']+box['width'] and box['y'] < previous['y']+previous['height'] and previous['y'] < box['y']+box['height']
                if overlaps: raise ValueError(f'Overlapping visual containers: {visual}')
            boxes.append(box)
            visual_count += 1
    for relation in model['relationships']:
        assert relation['fromColumn'] in refs[relation['fromTable']]['Column']
        assert relation['toColumn'] in refs[relation['toTable']]['Column']
    result = {'json_schema_files_passed':checked, 'visual_references_and_layout_passed':visual_count,
              'tables':len(tables), 'measures':sum(len(t.get('measures',[])) for t in tables.values()),
              'native_power_bi_open_refresh_dax_render': 'Not covered by this command; see native_dax_validation.json and native_render_validation.json',
              'limitations':'Schema checks cannot validate visual-specific role names, DAX/M execution, or native rendering.'}
    report = ROOT/'reports/dashboard/powerbi_validation.json'
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))


if __name__ == '__main__':
    main()
