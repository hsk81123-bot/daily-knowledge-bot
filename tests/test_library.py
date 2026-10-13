from datetime import date

import pytest

from knowledge_bot import formatter, library
from knowledge_bot.config import load_config
from knowledge_bot.lesson import make_lesson
from knowledge_bot.selector import Pick

CONFIG = load_config()
PAIRS = [(t, c) for t in CONFIG.topics for c in t.concepts]


@pytest.mark.parametrize("topic,concept", PAIRS, ids=[f"{t.key}:{i}" for t in CONFIG.topics for i in range(len(t.concepts))])
def test_every_concept_has_a_complete_lesson(topic, concept):
    lesson = library.find(topic.key, concept.name)
    assert lesson is not None, f"{topic.key}: '{concept.name}' 노트가 없습니다"
    for f in ("title", "level", "one_liner", "example", "misconception", "connection"):
        assert lesson[f], f"{concept.name}: {f} 비어 있음"
    assert lesson["level"] in ("입문", "중급", "심화")
    assert 2 <= len(lesson["sections"]) <= 4
    quiz = lesson["quiz"]
    assert len(quiz["choices"]) == 4 and 0 <= quiz["answer_index"] < 4
    assert formatter.quiz_fits_poll(quiz), f"{concept.name}: 퀴즈가 투표 길이 제한을 넘습니다"
    assert len(quiz["explanation"]) <= formatter.POLL_EXPLANATION_LIMIT
    assert lesson["keywords"] and lesson["next_topics"]
    messages, _ = formatter.render_telegram(lesson, topic, date(2026, 10, 14), use_poll=True)
    assert len(messages) <= 2


def test_no_orphan_lessons():
    for t in CONFIG.topics:
        names = {c.name for c in t.concepts}
        stored = set(library._load(str(library.LIBRARY_DIR), t.key))
        assert stored <= names, f"{t.key}: 설정에 없는 노트 {stored - names}"


def test_library_is_used_before_claude_or_wikipedia(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    topic = CONFIG.topics[0]
    lesson = make_lesson(Pick(topic, topic.concepts[0], review=True), CONFIG.settings)
    assert lesson["source"] == "library" and lesson["review"]
