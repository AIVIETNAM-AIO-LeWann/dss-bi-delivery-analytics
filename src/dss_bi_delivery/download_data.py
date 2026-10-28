"""Download only the pinned public Kaggle dataset; never extract arbitrary ZIP paths."""

import hashlib
import json
import shutil
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from .schema import EXPECTED_SHA256

ROOT = Path(__file__).resolve().parents[2]
URL = "https://www.kaggle.com/api/v1/datasets/download/saicharankomati/dataco-supply-chain-dataset?datasetVersionNumber=1"


def download() -> None:
    target = ROOT / "data/raw/DataCoSupplyChainDataset.csv"
    manifest_path = ROOT / "docs/source_manifest.json"
    if target.exists():
        checksum = hashlib.sha256(target.read_bytes()).hexdigest()
        if checksum != EXPECTED_SHA256:
            raise ValueError("Existing raw file differs; refusing to overwrite it.")
        if not manifest_path.exists():
            raise ValueError("CSV exists but provenance manifest is missing. Document origin before proceeding.")
        print("Pinned raw CSV already exists; no download or overwrite needed.")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    archive = target.parent / "kaggle-v1.zip"
    with urllib.request.urlopen(URL, timeout=120) as src, archive.open("wb") as dst:
        shutil.copyfileobj(src, dst)
    with zipfile.ZipFile(archive) as bundle:
        members = [n for n in bundle.namelist() if Path(n).name == target.name]
        if len(members) != 1:
            raise ValueError("Expected one exact source CSV. Check Kaggle response/version.")
        temp = target.with_suffix(".csv.partial")
        with bundle.open(members[0]) as src, temp.open("wb") as dst:
            shutil.copyfileobj(src, dst)
    checksum = hashlib.sha256(temp.read_bytes()).hexdigest()
    if checksum != EXPECTED_SHA256:
        raise ValueError("Downloaded CSV checksum differs from pinned source; original target not replaced.")
    temp.replace(target)
    manifest = {"dataset_slug": "saicharankomati/dataco-supply-chain-dataset", "requested_version": 1,
                "download_url": URL, "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                "csv_file": target.name, "csv_bytes": target.stat().st_size, "csv_sha256": checksum,
                "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Downloaded and verified pinned DataCo CSV.")


if __name__ == "__main__":
    download()
