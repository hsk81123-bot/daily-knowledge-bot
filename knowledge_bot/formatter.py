"""공부 노트를 텔레그램 HTML 메시지와 마크다운 보관본으로 만든다."""
from __future__ import annotations

from datetime import date
from html import escape
from urllib.parse import quote_plus

from .config import Topic

TELEGRAM_LIMIT = 4096
POLL_QUESTION_LIMIT = 300
POLL_OPTION_LIMIT = 100
POLL_EXPLANATION_LIMIT = 200
WEEKDAYS = "월화수목금토일"


def _e(text: str) -> str:
    return escape(text or "", quote=False)


def links(lesson: dict, topic: Topic) -> list[tuple[str, str]]:
    """더 공부할 링크(검색 링크라 깨지지 않는다)."""
    q = lesson.get("concept_en") or lesson.get("concept") or ""
    out = []
    if lesson.get("source_url"):
        out.append(("📖 위키백과", lesson["source_url"]))
    else:
        out.append(("📖 위키백과", f"https://en.wikipedia.org/w/index.php?search={quote_plus(q)}"))
    out.append(("🎓 Google Scholar", f"https://scholar.google.com/scholar?q={quote_plus(q)}"))
    if topic.category.upper() == "AI":
        out.append(("📄 arXiv", f"https://arxiv.org/search/?query={quote_plus(q)}&searchtype=all"))
    else:
        out.append(("📺 YouTube", f"https://www.youtube.com/results?search_query={quote_plus(q)}"))
    return out


def quiz_fits_poll(quiz: dict | None) -> bool:
    if not quiz:
        return False
    choices = quiz.get("choices") or []
    return (
        2 <= len(choices) <= 10
        and len(quiz.get("question", "")) <= POLL_QUESTION_LIMIT
        and all(0 < len(c) <= POLL_OPTION_LIMIT for c in choices)
    )


def poll_payload(lesson: dict) -> dict | None:
    quiz = lesson.get("quiz")
    if not quiz_fits_poll(quiz):
        return None
    explanation = quiz.get("explanation", "")
    if len(explanation) > POLL_EXPLANATION_LIMIT:
        explanation = explanation[: POLL_EXPLANATION_LIMIT - 1] + "…"
    return {
        "question": "❓ " + quiz["question"] if len(quiz["question"]) <= POLL_QUESTION_LIMIT - 2 else quiz["question"],
        "options": quiz["choices"],
        "correct_option_id": int(quiz["answer_index"]),
        "explanation": explanation,
    }


def _header(lesson: dict, topic: Topic, day: date) -> list[str]:
    tag = " · 복습" if lesson.get("review") else ""
    level = f" · {lesson['level']}" if lesson.get("level") else ""
    head = [
        f"{topic.emoji} <b>오늘의 지식</b> | {topic.category} › {topic.name}{tag}",
        f"<i>{day.month}월 {day.day}일 ({WEEKDAYS[day.weekday()]}){level}</i>",
        "",
        f"<b>{_e(lesson['title'])}</b>",
    ]
    if lesson.get("one_liner"):
        head += ["", f"💡 {_e(lesson['one_liner'])}"]
    return head


def message_blocks(lesson: dict, topic: Topic, day: date, include_quiz_text: bool) -> list[str]:
    """메시지 덩어리(단락) 목록. 길이 제한에 맞춰 나눌 때 단락 경계를 지킨다."""
    blocks = ["\n".join(_header(lesson, topic, day))]
    for s in lesson.get("sections") or []:
        blocks.append(f"<b>📖 {_e(s['heading'])}</b>\n{_e(s['body'])}")
    if lesson.get("formula"):
        blocks.append(f"<b>🧮 핵심 수식·원리</b>\n<code>{_e(lesson['formula'])}</code>")
    if lesson.get("example"):
        blocks.append(f"<b>🔍 예시·적용</b>\n{_e(lesson['example'])}")
    if lesson.get("misconception"):
        blocks.append(f"<b>⚠️ 흔한 오해</b>\n{_e(lesson['misconception'])}")
    if lesson.get("connection"):
        blocks.append(f"<b>🔗 배터리 × AI</b>\n{_e(lesson['connection'])}")
    quiz = lesson.get("quiz")
    if include_quiz_text and quiz:
        letters = "ABCDEFGHIJ"
        lines = [f"<b>❓ 오늘의 퀴즈</b>\n{_e(quiz['question'])}"]
        lines += [f"{letters[i]}. {_e(c)}" for i, c in enumerate(quiz["choices"][:10])]
        answer = letters[int(quiz["answer_index"])]
        lines.append(f"정답: <tg-spoiler>{answer} — {_e(quiz.get('explanation', ''))}</tg-spoiler>")
        blocks.append("\n".join(lines))
    if lesson.get("keywords"):
        kws = " · ".join(
            f"{_e(k['ko'])}({_e(k['en'])})" if k.get("en") and k["en"] != k["ko"] else _e(k["ko"])
            for k in lesson["keywords"]
        )
        blocks.append(f"<b>🏷 키워드</b>\n{kws}")
    if lesson.get("next_topics"):
        blocks.append("<b>➡️ 다음에 공부할 것</b>\n" + "\n".join(f"• {_e(t)}" for t in lesson["next_topics"]))
    if lesson.get("references"):
        blocks.append("<b>📚 참고 문헌</b>\n" + "\n".join(f"• {_e(r)}" for r in lesson["references"]))
    if lesson.get("source") == "wikipedia":
        blocks.append("<i>미리 써 둔 노트가 없는 개념이라 위키백과 요약으로 보냈습니다.</i>")
    return blocks


def split_blocks(blocks: list[str], limit: int = TELEGRAM_LIMIT) -> list[str]:
    """단락을 이어 붙이되 한 메시지가 limit을 넘지 않게 나눈다."""
    messages, current = [], ""
    for block in blocks:
        while len(block) > limit:  # 단락 하나가 너무 길면 줄 단위로 자른다
            cut = block.rfind("\n", 0, limit)
            cut = cut if cut > 0 else limit
            if current:
                messages.append(current)
                current = ""
            messages.append(block[:cut])
            block = block[cut:].lstrip("\n")
        candidate = f"{current}\n\n{block}" if current else block
        if len(candidate) > limit:
            messages.append(current)
            current = block
        else:
            current = candidate
    if current:
        messages.append(current)
    return messages


def render_telegram(lesson: dict, topic: Topic, day: date, use_poll: bool) -> tuple[list[str], dict | None]:
    """(메시지 목록, 퀴즈 투표 내용 또는 None)"""
    poll = poll_payload(lesson) if use_poll else None
    blocks = message_blocks(lesson, topic, day, include_quiz_text=poll is None)
    return split_blocks(blocks), poll


def render_markdown(lesson: dict, topic: Topic, day: date) -> str:
    """저장소에 남길 마크다운 노트."""
    out = [f"# {lesson['title']}", ""]
    meta = [f"{topic.emoji} {topic.category} › {topic.name}", day.isoformat()]
    if lesson.get("level"):
        meta.append(lesson["level"])
    if lesson.get("review"):
        meta.append("복습")
    out += [" · ".join(meta), ""]
    if lesson.get("one_liner"):
        out += [f"> 💡 {lesson['one_liner']}", ""]
    for s in lesson.get("sections") or []:
        out += [f"## {s['heading']}", "", s["body"], ""]
    for key, title in (("formula", "🧮 핵심 수식·원리"), ("example", "🔍 예시·적용"),
                       ("misconception", "⚠️ 흔한 오해"), ("connection", "🔗 배터리 × AI")):
        if lesson.get(key):
            body = f"```\n{lesson[key]}\n```" if key == "formula" else lesson[key]
            out += [f"## {title}", "", body, ""]
    quiz = lesson.get("quiz")
    if quiz:
        letters = "ABCDEFGHIJ"
        out += ["## ❓ 퀴즈", "", quiz["question"], ""]
        out += [f"- {letters[i]}. {c}" for i, c in enumerate(quiz["choices"][:10])]
        out += ["", "<details><summary>정답 보기</summary>", "",
                f"**{letters[int(quiz['answer_index'])]}** — {quiz.get('explanation', '')}", "", "</details>", ""]
    if lesson.get("keywords"):
        out += ["## 🏷 키워드", "", " · ".join(
            f"{k['ko']} ({k['en']})" if k.get("en") and k["en"] != k["ko"] else k["ko"] for k in lesson["keywords"]), ""]
    if lesson.get("next_topics"):
        out += ["## ➡️ 다음에 공부할 것", ""] + [f"- {t}" for t in lesson["next_topics"]] + [""]
    if lesson.get("references"):
        out += ["## 📚 참고 문헌", ""] + [f"- {r}" for r in lesson["references"]] + [""]
    out += ["## 🔗 더 읽어보기", ""] + [f"- [{label}]({url})" for label, url in links(lesson, topic)] + [""]
    return "\n".join(out)
