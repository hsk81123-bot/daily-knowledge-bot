import random
from datetime import date

from knowledge_bot.selector import choose, pick_topic

TODAY = date(2026, 10, 14)


def test_config_has_eight_topics(config):
    assert len(config.topics) == 8
    assert {t.category for t in config.topics} == {"배터리", "AI"}
    assert all(len(t.concepts) >= 10 for t in config.topics)


def test_random_topic_covers_all(config, history):
    seen = {pick_topic(config, history, TODAY, random.Random(i)).key for i in range(200)}
    assert seen == {t.key for t in config.topics}


def test_avoids_recent_topics(config, history):
    keys = [t.key for t in config.topics]
    history.data["lessons"] = [
        {"date": "2026-10-13", "topic": keys[0], "concept": "x", "title": "x", "trigger": "daily", "file": "x"},
        {"date": "2026-10-12", "topic": keys[1], "concept": "x", "title": "x", "trigger": "daily", "file": "x"},
        {"date": "2026-10-01", "topic": keys[2], "concept": "x", "title": "x", "trigger": "daily", "file": "x"},
    ]
    picked = {pick_topic(config, history, TODAY, random.Random(i)).key for i in range(200)}
    assert keys[0] not in picked and keys[1] not in picked
    assert keys[2] in picked  # 오래전에 보낸 주제는 다시 나올 수 있다


def test_all_recent_falls_back_to_any(config, history):
    config.settings.avoid_recent_days = 30
    history.data["lessons"] = [
        {"date": "2026-10-13", "topic": t.key, "concept": "x", "title": "x", "trigger": "daily", "file": "x"}
        for t in config.topics
    ]
    assert pick_topic(config, history, TODAY, random.Random(0)) in config.topics


def test_concept_not_repeated(config, history):
    topic = config.topics[0]
    covered = [c.name for c in topic.concepts[:-1]]
    history.data["lessons"] = [
        {"date": "2026-01-01", "topic": topic.key, "concept": n, "title": n, "trigger": "daily", "file": "x"}
        for n in covered
    ]
    pick = choose(config, history, TODAY, random.Random(0), topic=topic)
    assert pick.concept.name == topic.concepts[-1].name
    assert not pick.review


def test_exhausted_with_claude_lets_model_choose(config, history):
    topic = config.topics[0]
    history.data["lessons"] = [
        {"date": "2026-01-01", "topic": topic.key, "concept": c.name, "title": c.name, "trigger": "daily", "file": "x"}
        for c in topic.concepts
    ]
    pick = choose(config, history, TODAY, random.Random(0), can_generate=True, topic=topic)
    assert pick.concept is None
    assert len(pick.covered_names) == len(topic.concepts)


def test_exhausted_without_claude_reviews_oldest(config, history):
    topic = config.topics[0]
    order = list(reversed(topic.concepts))  # 마지막 개념을 가장 먼저 배움
    history.data["lessons"] = [
        {"date": "2026-01-01", "topic": topic.key, "concept": c.name, "title": c.name, "trigger": "daily", "file": "x"}
        for c in order
    ]
    pick = choose(config, history, TODAY, random.Random(0), can_generate=False, topic=topic)
    assert pick.review
    assert pick.concept.name == order[0].name


def test_find_topic(config):
    assert config.find_topic("계면").key == "battery-interface"
    assert config.find_topic("LLM").key == "ai-llm"
    assert config.find_topic("배터리 분석법").key == "battery-analysis"
    assert config.find_topic("ai-ontology").key == "ai-ontology"
    assert config.find_topic("없는주제") is None
