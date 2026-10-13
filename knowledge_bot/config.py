"""설정 파일(config/topics.yaml)과 환경변수 읽기."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT / "config" / "topics.yaml"
DEFAULT_MODEL = "claude-opus-5-5"


@dataclass
class Concept:
    name: str
    en: str = ""


@dataclass
class Topic:
    key: str
    category: str
    name: str
    emoji: str
    description: str
    concepts: list[Concept] = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"{self.category} › {self.name}"


@dataclass
class Settings:
    timezone: str = "Asia/Seoul"
    avoid_recent_days: int = 3
    retention_days: int = 365
    audience: str = "배터리와 AI를 함께 공부하는 대학원·연구자 수준 독자"
    quiz_as_poll: bool = True
    bot_token_env: str = "TELEGRAM_BOT_TOKEN"
    chat_id_env: str = "TELEGRAM_CHAT_ID"

    @property
    def bot_token(self) -> str:
        return os.environ.get(self.bot_token_env, "").strip()

    @property
    def chat_id(self) -> str:
        return os.environ.get(self.chat_id_env, "").strip()

    @property
    def anthropic_key(self) -> str:
        return os.environ.get("ANTHROPIC_API_KEY", "").strip()

    @property
    def model(self) -> str:
        return os.environ.get("CLAUDE_MODEL", "").strip() or DEFAULT_MODEL


@dataclass
class Config:
    settings: Settings
    topics: list[Topic]

    def find_topic(self, query: str) -> Topic | None:
        """key, 이름, "배터리 소재" 같은 표현으로 주제를 찾는다."""
        q = query.strip().lower().replace(" ", "")
        if not q:
            return None
        for t in self.topics:
            names = {t.key.lower(), t.name.lower(), (t.category + t.name).lower()}
            if q in names:
                return t
        matches = [t for t in self.topics if q in t.key.lower() or q in t.name.lower()]
        return matches[0] if len(matches) == 1 else None


def load_config(path: Path | str = DEFAULT_CONFIG) -> Config:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    s = data.get("settings") or {}
    tg = data.get("telegram") or {}
    settings = Settings(
        timezone=s.get("timezone", "Asia/Seoul"),
        avoid_recent_days=int(s.get("avoid_recent_days", 3)),
        retention_days=int(s.get("retention_days", 365)),
        audience=s.get("audience", Settings.audience),
        quiz_as_poll=bool(s.get("quiz_as_poll", True)),
        bot_token_env=tg.get("bot_token_env", "TELEGRAM_BOT_TOKEN"),
        chat_id_env=tg.get("chat_id_env", "TELEGRAM_CHAT_ID"),
    )
    topics = []
    for t in data.get("topics") or []:
        concepts = [
            Concept(name=c["name"], en=c.get("en", "")) if isinstance(c, dict) else Concept(name=str(c))
            for c in t.get("concepts") or []
        ]
        topics.append(
            Topic(
                key=t["key"],
                category=t.get("category", ""),
                name=t.get("name", t["key"]),
                emoji=t.get("emoji", "📘"),
                description=t.get("description", ""),
                concepts=concepts,
            )
        )
    if not topics:
        raise ValueError(f"{path}에 topics가 없습니다.")
    keys = [t.key for t in topics]
    if len(keys) != len(set(keys)):
        raise ValueError("topics의 key가 중복됩니다.")
    return Config(settings=settings, topics=topics)
