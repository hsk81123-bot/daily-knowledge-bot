from datetime import date

from knowledge_bot import formatter

DAY = date(2026, 10, 14)


def test_html_is_escaped(config, sample_lesson):
    topic = config.topics[1]
    messages, poll = formatter.render_telegram(sample_lesson, topic, DAY, use_poll=True)
    text = "\n".join(messages)
    assert "&lt;막&gt;" in text and "<막>" not in text
    assert "10월 14일 (수)" in text
    assert poll["correct_option_id"] == 1
    assert "오늘의 퀴즈" not in text  # 투표로 보내면 본문에서 뺀다


def test_quiz_falls_back_to_spoiler_when_too_long(config, sample_lesson):
    sample_lesson["quiz"]["choices"][0] = "가" * 150
    messages, poll = formatter.render_telegram(sample_lesson, config.topics[1], DAY, use_poll=True)
    assert poll is None
    assert "<tg-spoiler>B —" in "\n".join(messages)


def test_split_respects_limit():
    blocks = [("단락" * 500) for _ in range(5)] + ["줄\n" * 3000]
    messages = formatter.split_blocks(blocks, limit=4096)
    assert all(len(m) <= 4096 for m in messages)
    assert sum(len(m) for m in messages) >= sum(len(b) for b in blocks) - 100


def test_links_depend_on_category(config, sample_lesson):
    battery = formatter.links(sample_lesson, config.topics[0])
    ai = formatter.links(sample_lesson, config.topics[5])
    assert any("arxiv.org" in u for _, u in ai)
    assert not any("arxiv.org" in u for _, u in battery)
    assert all("Solid+electrolyte+interphase" in u for _, u in battery)


def test_markdown_archive(config, sample_lesson):
    md = formatter.render_markdown(sample_lesson, config.topics[1], DAY)
    assert md.startswith("# SEI: 음극을 지키는 얇은 막")
    assert "<details>" in md and "**B**" in md
    assert "scholar.google.com" in md
