"""발송 기록(data/history.json)과 공부 노트 보관(data/lessons/)."""
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

from .config import ROOT

DATA_DIR = ROOT / "data"


class History:
    def __init__(self, path: Path | None = None):
        self.path = Path(path) if path else DATA_DIR / "history.json"
        self.lessons_dir = self.path.parent / "lessons"
        self.data = {"lessons": [], "telegram_offset": 0}
        if self.path.exists():
            loaded = json.loads(self.path.read_text(encoding="utf-8") or "{}")
            self.data.update(loaded)

    @property
    def lessons(self) -> list[dict]:
        return self.data["lessons"]

    @property
    def telegram_offset(self) -> int:
        return int(self.data.get("telegram_offset", 0))

    @telegram_offset.setter
    def telegram_offset(self, value: int) -> None:
        self.data["telegram_offset"] = int(value)

    def daily_entry(self, day: date) -> dict | None:
        for e in reversed(self.lessons):
            if e["date"] == day.isoformat() and e.get("trigger") == "daily":
                return e
        return None

    def entries_on(self, day: date) -> list[dict]:
        return [e for e in self.lessons if e["date"] == day.isoformat()]

    def recent(self, today: date, days: int) -> list[dict]:
        start = (today - timedelta(days=days - 1)).isoformat()
        return [e for e in self.lessons if e["date"] >= start]

    def recent_topic_keys(self, today: date, days: int) -> set[str]:
        """오늘을 포함해 최근 days일 안에 보낸 주제 key."""
        if days <= 0:
            return set()
        return {e["topic"] for e in self.recent(today, days)}

    def covered(self, topic_key: str) -> list[dict]:
        """그 주제에서 배운 개념들(오래된 순)."""
        return [e for e in self.lessons if e["topic"] == topic_key]

    def lesson_path(self, day: date, topic_key: str, suffix: str) -> Path:
        base = f"{day.isoformat()}-{topic_key}"
        path = self.lessons_dir / f"{base}{suffix}"
        n = 2
        while path.exists():
            path = self.lessons_dir / f"{base}-{n}{suffix}"
            n += 1
        return path

    def add(self, day: date, topic_key: str, lesson: dict, markdown: str, trigger: str) -> dict:
        self.lessons_dir.mkdir(parents=True, exist_ok=True)
        json_path = self.lesson_path(day, topic_key, ".json")
        md_path = json_path.with_suffix(".md")
        json_path.write_text(json.dumps(lesson, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        md_path.write_text(markdown, encoding="utf-8")
        entry = {
            "date": day.isoformat(),
            "topic": topic_key,
            "concept": lesson["concept"],
            "title": lesson["title"],
            "source": lesson.get("source", "claude"),
            "trigger": trigger,
            "file": json_path.relative_to(self.path.parent).as_posix(),
        }
        self.lessons.append(entry)
        return entry

    def load_lesson(self, entry: dict) -> dict | None:
        path = self.path.parent / entry["file"]
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def prune(self, today: date, retention_days: int) -> int:
        """보관 기간이 지난 기록과 노트 파일을 지운다."""
        cutoff = (today - timedelta(days=retention_days)).isoformat()
        keep, removed = [], 0
        for e in self.lessons:
            if e["date"] < cutoff:
                removed += 1
                for suffix in (".json", ".md"):
                    p = (self.path.parent / e["file"]).with_suffix(suffix)
                    if p.exists():
                        p.unlink()
            else:
                keep.append(e)
        self.data["lessons"] = keep
        return removed

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
