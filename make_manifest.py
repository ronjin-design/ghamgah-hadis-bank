"""Writes manifest.json for the question-pack repository.

  python make_manifest.py <folder with pack-0001.json, pack-0002.json, ...>

Each pack's version is read from the file; its SHA-256 is computed from the
exact bytes, so the app can verify what it downloads. Commit the packs and
manifest.json together.
"""
import hashlib
import json
import sys
from pathlib import Path


def main(folder):
    root = Path(folder)
    packs = []
    for f in sorted(root.glob('pack-*.json')):
        raw = f.read_bytes()
        version = json.loads(raw.decode('utf-8'))['version']
        packs.append({'version': version, 'file': f.name, 'sha256': hashlib.sha256(raw).hexdigest()})
    versions = [p['version'] for p in packs]
    assert versions == sorted(set(versions)), f'pack versions must be unique and ordered: {versions}'
    # Plain LF bytes on every OS (write_text would use CRLF on Windows).
    (root / 'manifest.json').write_bytes((json.dumps({'format': 1, 'packs': packs}, indent=1) + '\n').encode('utf-8'))
    print(f'manifest.json: {len(packs)} pack(s), latest version {versions[-1] if versions else 0}')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
