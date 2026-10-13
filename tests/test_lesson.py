import json
from types import SimpleNamespace
from unittest import mock

from knowledge_bot import lesson as lesson_mod
from knowledge_bot.selector import Pick


def fake_client(payload, stop_reason="end_turn"):
    response = SimpleNamespace(
        stop_reason=stop_reason,
        model="claude-opus-5-5",
        content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=json.dumps(payload))],
    )
    client = mock.MagicMock()
    client.beta.messages.create.return_value = response
    return client


def test_claude_lesson(config, sample_lesson, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")
    topic = config.topics[1]
    pick = Pick(topic, topic.concepts[0])
    client = fake_client(sample_lesson)
    result = lesson_mod.make_lesson(pick, config.settings, client=client)
    assert result["source"] == "claude"
    assert result["concept"] == topic.concepts[0].name
    kwargs = client.beta.messages.create.call_args.kwargs
    assert kwargs["model"] == "claude-opus-5-5"
    assert kwargs["fallbacks"] == "default"
    assert kwargs["output_config"]["format"]["type"] == "json_schema"
    assert topic.concepts[0].name in kwargs["messages"][0]["content"]


def test_model_env_override(config, sample_lesson, monkeypatch):
    monkeypatch.setenv("CLAUDE_MODEL", "claude-haiku-5-5")
    client = fake_client(sample_lesson)
    topic = config.topics[0]
    lesson_mod.make_lesson(Pick(topic, topic.concepts[0]), config.settings, client=client)
    assert client.beta.messages.create.call_args.kwargs["model"] == "claude-haiku-5-5"


def test_bad_quiz_is_dropped(config, sample_lesson):
    sample_lesson["quiz"]["answer_index"] = 9
    topic = config.topics[0]
    result = lesson_mod.make_lesson(Pick(topic, topic.concepts[0]), config.settings, client=fake_client(sample_lesson))
    assert result["quiz"] is None


def test_refusal_falls_back_to_wikipedia(config, sample_lesson):
    topic = config.topics[0]
    pick = Pick(topic, topic.concepts[0])
    wiki = {"lang": "ko", "title": "니켈", "en_title": "x", "extract": "요약문", "url": "https://ko.wikipedia.org/wiki/x"}
    with mock.patch.object(lesson_mod, "wikipedia_summary", return_value=wiki):
        result = lesson_mod.make_lesson(pick, config.settings, client=fake_client(sample_lesson, "refusal"))
    assert result["source"] == "wikipedia"
    assert result["sections"][0]["body"] == "요약문"
    assert result["source_url"].startswith("https://ko.wikipedia.org")


def test_no_key_uses_wikipedia(config, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    topic = config.topics[4]
    with mock.patch.object(lesson_mod, "wikipedia_summary", return_value=None):
        result = lesson_mod.make_lesson(Pick(topic, topic.concepts[0]), config.settings)
    assert result["source"] == "none"
    assert result["concept"] == topic.concepts[0].name


def test_claude_chooses_concept_when_none(config, sample_lesson):
    topic = config.topics[0]
    sample_lesson["concept"] = "새 개념"
    pick = Pick(topic, None, covered_names=("A", "B"))
    client = fake_client(sample_lesson)
    result = lesson_mod.make_lesson(pick, config.settings, client=client)
    assert result["concept"] == "새 개념"
    prompt = client.beta.messages.create.call_args.kwargs["messages"][0]["content"]
    assert "A, B" in prompt


def test_wikipedia_summary_prefers_korean():
    calls = []

    def fake_get(url, params=None):
        calls.append(url)
        if params and params.get("list") == "search":
            return {"query": {"search": [{"title": "Cyclic voltammetry"}]}}
        if params and params.get("prop") == "langlinks":
            return {"query": {"pages": {"1": {"langlinks": [{"lang": "ko", "*": "순환 전압전류법"}]}}}}
        return {"title": "순환 전압전류법", "extract": "전위를 주기적으로 바꾸며 전류를 측정한다.",
                "content_urls": {"desktop": {"page": "https://ko.wikipedia.org/wiki/x"}}}

    with mock.patch.object(lesson_mod, "_get_json", side_effect=fake_get):
        result = lesson_mod.wikipedia_summary("Cyclic voltammetry")
    assert result["lang"] == "ko"
    assert calls[-1].startswith("https://ko.wikipedia.org/api/rest_v1/page/summary/")
