"""Restore local attachments from their original filenames without overwriting changes."""
from pathlib import Path
import argparse, hashlib, json, shutil, zipfile

ROOT = Path(__file__).resolve().parents[1]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def copy_checked(source, target, expected):
    if target.exists():
        if digest(target) != expected:
            raise ValueError(f'Refusing to overwrite changed file: {target}')
        return
    if digest(source) != expected:
        raise ValueError(f'Unexpected source checksum: {source}')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    if digest(target) != expected:
        raise ValueError(f'Copy checksum mismatch: {target}')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True, help='Folder containing the nine original attachments')
    args = parser.parse_args()
    manifest = json.loads((ROOT/'references/resource_manifest.json').read_text(encoding='utf-8'))
    # Validate every missing source first, before copying.
    for item in manifest:
        target = ROOT/item['path']
        source = target if target.exists() else args.source/item['original_name']
        if digest(source) != item['sha256']:
            raise ValueError(f'Unexpected checksum: {source}')
    for item in manifest:
        copy_checked(args.source/item['original_name'], ROOT/item['path'], item['sha256'])
    for archive, prefix, destination in [
        ('ngoc_quang_forecasting.zip','Ngoc_Quang_Chu_de_18/','workstreams/forecasting'),
        ('hoang_quan_descriptive.zip','thong_ke_mo_ta/','workstreams/descriptive'),
        ('hoai_phu_prescriptive.zip','10-11/','workstreams/prescriptive')]:
        base = (ROOT/destination).resolve()
        with zipfile.ZipFile(ROOT/'archive/handoffs'/archive) as bundle:
            for entry in bundle.infolist():
                if not entry.filename.startswith(prefix):
                    raise ValueError(f'Unexpected ZIP root: {entry.filename}')
                target = (base/entry.filename[len(prefix):]).resolve()
                if not target.is_relative_to(base):
                    raise ValueError(f'Unsafe ZIP path: {entry.filename}')
                # Existing files may contain reviewed changes: never overwrite them.
                if entry.is_dir() or target.exists():
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                content = bundle.read(entry)
                target.write_bytes(content)
                if digest(target) != hashlib.sha256(content).hexdigest():
                    raise ValueError(f'Extraction mismatch: {target}')
    for item in json.loads((ROOT/'references/restored_data_manifest.json').read_text(encoding='utf-8')):
        copy_checked(ROOT/item['source'], ROOT/item['path'], item['sha256'])
    print('Resources restored; existing workstream files preserved. Run scripts/check_project.py next.')

if __name__ == '__main__':
    main()
