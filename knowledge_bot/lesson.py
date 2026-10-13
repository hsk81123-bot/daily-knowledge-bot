"""공부 노트 만들기: Claude로 생성하고, 키가 없거나 실패하면 위키백과 요약으로 대신한다."""
from __future__ import annotations

import json
import logging
from urllib.parse import quote

import requests

from .config import Settings
from .selector import Pick

log = logging.getLogger(__name__)

USER_AGENT = "daily-knowledge-bot/1.0 (https://github.com/hsk81123-bot/daily-knowledge-bot)"

LESSON_SCHEMA = {
    "type": "object",
    "properties": {
        "concept": {"type": "string", "description": "오늘 다루는 개념의 한국어 이름"},
        "concept_en": {"type": "string", "description": "개념의 영어 이름(검색용)"},
        "title": {"type": "string", "description": "노트 제목"},
        "level": {"type": "string", "enum": ["입문", "중급", "심화"]},
        "one_liner": {"type": "string", "description": "핵심을 한 문장으로"},
        "sections": {
            "type": "array",
            "description": "본문 3~4개 단락",
            "items": {
                "type": "object",
                "properties": {"heading": {"type": "string"}, "body": {"type": "string"}},
                "required": ["heading", "body"],
                "additionalProperties": False,
            },
        },
        "formula": {"type": "string", "description": "핵심 수식이나 원리(유니코드 평문, 변수 설명 포함). 없으면 빈 문자열"},
        "example": {"type": "string", "description": "구체적인 예시나 실험·실무 적용"},
        "misconception": {"type": "string", "description": "흔한 오해와 바로잡기"},
        "connection": {"type": "string", "description": "배터리 연구와 AI를 잇는 연결점 한두 문장"},
        "quiz": {
            "type": "object",
            "properties": {
                "question": {"type": "string"},
                "choices": {"type": "array", "items": {"type": "string"}},
                "answer_index": {"type": "integer"},
                "explanation": {"type": "string"},
            },
            "required": ["question", "choices", "answer_index", "explanation"],
            "additionalProperties": False,
        },
        "keywords": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"ko": {"type": "string"}, "en": {"type": "string"}},
                "required": ["ko", "en"],
                "additionalProperties": False,
            },
        },
        "next_topics": {"type": "array", "items": {"type": "string"}},
        "references": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "concept", "concept_en", "title", "level", "one_liner", "sections", "formula",
        "example", "misconception", "connection", "quiz", "keywords", "next_topics", "references",
    ],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """너는 배터리 과학과 인공지능을 함께 가르치는 꼼꼼한 튜터다.
매일 아침 텔레그램으로 읽을 한 편의 공부 노트를 한국어로 쓴다. 뉴스가 아니라 오래 남는 지식을 다룬다.

원칙:
- 정확성이 가장 중요하다. 확실하지 않은 수치·연도·인명은 쓰지 말고, 범위가 있는 값은 "대략", "보통" 같은 말로 표시한다.
- 전문 용어는 처음 나올 때 영어를 괄호로 함께 쓴다. 예: 고체 전해질 계면(SEI)
- 마크다운, HTML, LaTeX를 쓰지 않는다. 줄바꿈과 "• " 글머리표만 쓴다. 수식은 유니코드 평문으로 쓴다(예: E = E° − (RT/nF)·ln Q).
- 본문(sections)은 3~4개 단락, 단락마다 3~6문장. 정의 → 원리(왜 그런가) → 어떻게 측정·구현하는가 → 한계나 최신 쟁점 흐름이 좋다.
- 노트 전체는 한국어 기준 2,000~2,800자 정도로, 휴대폰에서 5분 안에 읽을 분량으로 쓴다.
- 퀴즈는 개념 이해를 확인하는 4지선다 1문제. 질문은 250자, 선택지는 각 90자, 해설은 180자 이내. answer_index는 0부터 센다.
- references에는 네가 확실히 아는 표준 교과서나 널리 인용되는 리뷰 논문만 "저자, 제목, 연도" 형식으로 0~3개 적는다. URL은 쓰지 않는다. 확실하지 않으면 빈 배열로 둔다.
- next_topics에는 이어서 공부하면 좋은 개념 2~3개를 적는다."""


class LessonError(Exception):
    pass


def build_user_prompt(pick: Pick, settings: Settings) -> str:
    t = pick.topic
    lines = [
        f"분야: {t.category} › {t.name} — {t.description}",
        f"독자: {settings.audience}",
    ]
    if pick.concept is not None:
        lines.append(f"오늘의 개념: {pick.concept.name}" + (f" ({pick.concept.en})" if pick.concept.en else ""))
        if pick.review:
            lines.append("이 개념은 예전에 다뤘던 것이다. 복습 노트로, 지난번보다 한 단계 깊은 관점(응용, 최신 쟁점)을 중심으로 써라.")
    else:
        covered = ", ".join(pick.covered_names[-60:]) or "(없음)"
        lines.append("오늘의 개념은 네가 고른다. 이 분야에서 중요하지만 아래 목록에 없는 개념 하나를 골라라.")
        lines.append(f"이미 배운 개념: {covered}")
    lines.append("위 원칙대로 공부 노트를 작성해라.")
    return "\n".join(lines)


def _validate(data: dict) -> dict:
    quiz = data.get("quiz") or {}
    choices = quiz.get("choices") or []
    if not data.get("sections"):
        raise LessonError("본문(sections)이 비어 있습니다.")
    if len(choices) < 2 or not 0 <= int(quiz.get("answer_index", -1)) < len(choices):
        log.warning("퀴즈 형식이 올바르지 않아 퀴즈를 뺍니다.")
        data["quiz"] = None
    return data


def generate_with_claude(pick: Pick, settings: Settings, client=None) -> dict:
    if client is None:
        import anthropic

        client = anthropic.Anthropic(api_key=settings.anthropic_key, max_retries=3, timeout=600)
    response = client.beta.messages.create(
        model=settings.model,
        max_tokens=16000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        output_config={
            "effort": "medium",
            "format": {"type": "json_schema", "schema": LESSON_SCHEMA},
        },
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_prompt(pick, settings)}],
    )
    if response.stop_reason == "refusal":
        raise LessonError("Claude가 요청을 거절했습니다(refusal).")
    if response.stop_reason == "max_tokens":
        raise LessonError("응답이 max_tokens에서 잘렸습니다.")
    text = next((b.text for b in response.content if b.type == "text"), "")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise LessonError(f"JSON 파싱 실패: {e}") from e
    data = _validate(data)
    if pick.concept is not None:
        data["concept"] = pick.concept.name
        data["concept_en"] = data.get("concept_en") or pick.concept.en
    data["review"] = pick.review
    data["source"] = "claude"
    data["model"] = getattr(response, "model", settings.model)
    return data


# --- 위키백과 대체 경로 -------------------------------------------------------

def _get_json(url: str, params: dict | None = None) -> dict:
    r = requests.get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=20)
    r.raise_for_status()
    return r.json()


def wikipedia_summary(query: str) -> dict | None:
    """영어 위키백과에서 찾고, 한국어 문서가 있으면 한국어 요약을 돌려준다."""
    api = "https://en.wikipedia.org/w/api.php"
    found = _get_json(api, {"action": "query", "list": "search", "srsearch": query, "srlimit": 1, "format": "json"})
    hits = found.get("query", {}).get("search", [])
    if not hits:
        return None
    en_title = hits[0]["title"]
    lang, title = "en", en_title
    links = _get_json(api, {"action": "query", "titles": en_title, "prop": "langlinks", "lllang": "ko", "format": "json"})
    for page in links.get("query", {}).get("pages", {}).values():
        for ll in page.get("langlinks", []):
            lang, title = "ko", ll.get("*") or ll.get("title") or en_title
    summary = _get_json(f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{quote(title.replace(' ', '_'), safe='')}")
    extract = (summary.get("extract") or "").strip()
    if not extract:
        return None
    url = summary.get("content_urls", {}).get("desktop", {}).get("page", "")
    return {"lang": lang, "title": summary.get("title", title), "en_title": en_title, "extract": extract, "url": url}


def generate_from_wikipedia(pick: Pick) -> dict:
    concept = pick.concept
    name = concept.name if concept else pick.topic.name
    en = (concept.en if concept else "") or name
    lesson = {
        "concept": name,
        "concept_en": en,
        "title": name,
        "level": "",
        "one_liner": "",
        "sections": [],
        "formula": "",
        "example": "",
        "misconception": "",
        "connection": "",
        "quiz": None,
        "keywords": [{"ko": name, "en": en}] if en != name else [],
        "next_topics": [],
        "references": [],
        "review": pick.review,
        "source": "wikipedia",
    }
    try:
        wiki = wikipedia_summary(en)
    except requests.RequestException as e:
        log.warning("위키백과 요청 실패: %s", e)
        wiki = None
    if wiki:
        lang_label = "한국어" if wiki["lang"] == "ko" else "영어"
        lesson["sections"] = [{"heading": f"위키백과 요약 ({lang_label}: {wiki['title']})", "body": wiki["extract"]}]
        lesson["source_url"] = wiki["url"]
    else:
        lesson["sections"] = [{"heading": "오늘의 개념", "body": "자료를 가져오지 못했습니다. 아래 링크로 직접 공부해 보세요."}]
        lesson["source"] = "none"
    return lesson


def make_lesson(pick: Pick, settings: Settings, client=None) -> dict:
    """Claude 키가 있으면 Claude로, 없거나 실패하면 위키백과 요약으로 노트를 만든다."""
    if settings.anthropic_key or client is not None:
        try:
            return generate_with_claude(pick, settings, client=client)
        except Exception as e:  # noqa: BLE001 - 어떤 실패든 발송은 계속한다
            log.error("Claude 노트 생성 실패, 위키백과로 대신합니다: %s", e)
    else:
        log.info("ANTHROPIC_API_KEY가 없어 위키백과 요약으로 보냅니다.")
    if pick.concept is None:
        # Claude가 새 개념을 고를 예정이었지만 실패한 경우: 준비 목록의 첫 개념으로 복습
        from .config import Concept

        fallback = pick.topic.concepts[0] if pick.topic.concepts else Concept(name=pick.topic.name, en=pick.topic.name)
        pick = Pick(pick.topic, fallback, review=True, covered_names=pick.covered_names)
    return generate_from_wikipedia(pick)
