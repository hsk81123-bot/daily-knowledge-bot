"""저장소에 미리 써 둔 공부 노트(content/lessons/<주제 key>.yaml) 읽기."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

from .config import ROOT

LIBRARY_DIR = ROOT / "content" / "lessons"

FIELDS = ("title", "level", "one_liner", "sections", "formula", "example", "misconception",
          "connection", "quiz", "keywords", "next_topics", "references")


@lru_cache(maxsize=None)
def _load(directory: str, topic_key: str) -> dict[str, dict]:
    path = Path(directory) / f"{topic_key}.yaml"
    if not path.exists():
        return {}
    items = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    return {item["concept"]: item for item in items}


def find(topic_key: str, concept_name: str, directory: Path = LIBRARY_DIR) -> dict | None:
    """미리 써 둔 노트가 있으면 lesson 형식으로 돌려준다."""
    item = _load(str(directory), topic_key).get(concept_name)
    if item is None:
        return None
    lesson = {"concept": concept_name, "concept_en": item.get("concept_en", "")}
    for f in FIELDS:
        default = [] if f in ("sections", "keywords", "next_topics", "references") else ""
        lesson[f] = item.get(f, None if f == "quiz" else default)
    for s in lesson["sections"]:
        s["body"] = s["body"].strip()
    for f in ("one_liner", "formula", "example", "misconception", "connection"):
        lesson[f] = (lesson[f] or "").strip()
    lesson["source"] = "library"
    return lesson
