"""오늘의 주제와 개념 고르기."""
from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date

from .config import Concept, Config, Topic
from .history import History


@dataclass
class Pick:
    topic: Topic
    concept: Concept | None   # None이면 Claude가 새 개념을 고른다
    review: bool = False      # 이미 배운 개념의 복습인지
    covered_names: tuple[str, ...] = ()


def pick_topic(config: Config, history: History, today: date, rng: random.Random) -> Topic:
    """8개 주제 중 무작위로 하나. 최근 며칠 안에 보낸 주제는 피한다."""
    recent = history.recent_topic_keys(today, config.settings.avoid_recent_days)
    candidates = [t for t in config.topics if t.key not in recent] or list(config.topics)
    return rng.choice(candidates)


def pick_concept(topic: Topic, history: History, rng: random.Random, can_generate: bool) -> Pick:
    covered = history.covered(topic.key)
    covered_names = tuple(e["concept"] for e in covered)
    remaining = [c for c in topic.concepts if c.name not in covered_names]
    if remaining:
        return Pick(topic, rng.choice(remaining), covered_names=covered_names)
    if can_generate:
        # 준비된 개념을 다 배웠으면 Claude에게 아직 안 배운 새 개념을 고르게 한다.
        return Pick(topic, None, covered_names=covered_names)
    # 키가 없으면 가장 오래전에 배운 준비 개념부터 복습한다.
    last_seen = {}
    for i, e in enumerate(covered):
        last_seen[e["concept"]] = i
    pool = [c for c in topic.concepts] or [Concept(name=topic.name, en=topic.name)]
    oldest = min(pool, key=lambda c: last_seen.get(c.name, -1))
    return Pick(topic, oldest, review=True, covered_names=covered_names)


def choose(
    config: Config,
    history: History,
    today: date,
    rng: random.Random | None = None,
    can_generate: bool = False,
    topic: Topic | None = None,
) -> Pick:
    rng = rng or random.Random()
    topic = topic or pick_topic(config, history, today, rng)
    return pick_concept(topic, history, rng, can_generate)
