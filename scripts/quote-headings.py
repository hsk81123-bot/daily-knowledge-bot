"""content/lessons/*.yaml의 heading 값을 따옴표로 감싼다(제목에 콜론이 있어도 YAML이 깨지지 않게)."""
import re
import sys
from pathlib import Path

for path in sys.argv[1:] or Path("content/lessons").glob("*.yaml"):
    p = Path(path)
    text = re.sub(r'^(\s*- heading: )(?!")(.+)$', lambda m: f'{m[1]}"{m[2]}"', p.read_text(encoding="utf-8"), flags=re.M)
    p.write_text(text, encoding="utf-8")
