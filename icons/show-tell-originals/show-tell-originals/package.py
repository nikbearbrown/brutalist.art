"""Package only deliverables, never caches or the archive itself."""
from pathlib import Path
import zipfile
root=Path(__file__).resolve().parent
target=root/'show-tell-originals-25.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(root.rglob('*')):
        if path.is_file() and path.suffix in {'.py','.md','.json','.html','.svg','.png'} and '__pycache__' not in path.parts:
            archive.write(path,'show-tell-originals/'+str(path.relative_to(root)))
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    assert sum('/svg/' in n for n in archive.namelist())==25
print(target)
