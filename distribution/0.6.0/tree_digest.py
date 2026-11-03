"""Fingerprint bundle file bytes and symlink targets; ignore timestamps."""
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
digest = hashlib.sha256()
count = 0
for path in sorted(root.rglob('*'), key=lambda p: p.relative_to(root).as_posix()):
    rel = path.relative_to(root).as_posix()
    if path.is_symlink():
        value = 'L:' + str(path.readlink())
    elif path.is_file():
        with path.open('rb') as stream:
            value = 'F:' + hashlib.file_digest(stream, 'sha256').hexdigest()
    else:
        continue
    digest.update((rel + '\0' + value + '\n').encode('utf-8'))
    count += 1
print(json.dumps({'sha256': digest.hexdigest(), 'file_count': count}, sort_keys=True))
