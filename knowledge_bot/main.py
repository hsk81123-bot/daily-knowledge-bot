"""실행 진입점.

  python -m knowledge_bot send [--dry-run] [--topic 계면] [--force] [--seed N]
  python -m knowledge_bot commands [--dry-run]
"""
from __future__ import annotations

import argparse
import logging
import random
import sys
import time
from datetime import date, datetime
from zoneinfo import ZoneInfo

from .config import Config, Topic, load_config
from .formatter import links, message_blocks, render_markdown, render_telegram
from .history import History
from .lesson import make_lesson
from .selector import choose
from .telegram import Telegram, TelegramError

log = logging.getLogger("knowledge_bot")

MAX_NOW_PER_RUN = 2          # 한 번 폴링할 때 /now 처리 최대 횟수(API 비용 보호)
STALE_COMMAND_HOURS = 6      # 이보다 오래된 /now 요청은 무시


def today_in(config: Config) -> date:
    return datetime.now(ZoneInfo(config.settings.timezone)).date()


def deliver(tg: Telegram, lesson: dict, topic: Topic, day: date, use_poll: bool) -> None:
    messages, poll = render_telegram(lesson, topic, day, use_poll)
    buttons = links(lesson, topic)
    for i, text in enumerate(messages):
        tg.send_message(text, buttons=buttons if i == len(messages) - 1 else None)
    if poll:
        try:
            tg.send_quiz(poll)
        except TelegramError as e:
            log.warning("퀴즈 투표 발송 실패, 텍스트로 보냅니다: %s", e)
            quiz_block = message_blocks(lesson, topic, day, include_quiz_text=True)
            quiz_text = next((b for b in quiz_block if b.startswith("<b>❓")), None)
            if quiz_text:
                tg.send_message(quiz_text)


def create_and_send(config: Config, history: History, day: date, *, tg: Telegram | None, topic: Topic | None,
                    trigger: str, dry_run: bool, rng: random.Random | None = None) -> dict:
    s = config.settings
    pick = choose(config, history, day, rng=rng, can_generate=bool(s.anthropic_key), topic=topic)
    log.info("오늘의 주제: %s / 개념: %s", pick.topic.label, pick.concept.name if pick.concept else "(Claude가 선택)")
    lesson = make_lesson(pick, s)
    if dry_run:
        messages, poll = render_telegram(lesson, pick.topic, day, s.quiz_as_poll)
        for m in messages:
            print(m)
            print("-" * 40)
        if poll:
            print("[퀴즈 투표]", poll)
        for label, url in links(lesson, pick.topic):
            print(f"[버튼] {label}: {url}")
        return lesson
    deliver(tg, lesson, pick.topic, day, s.quiz_as_poll)
    history.add(day, pick.topic.key, lesson, render_markdown(lesson, pick.topic, day), trigger)
    return lesson


def make_telegram(config: Config) -> Telegram:
    s = config.settings
    if not s.bot_token:
        raise TelegramError(f"{s.bot_token_env}가 설정되지 않았습니다.")
    if not s.chat_id:
        raise TelegramError(f"{s.chat_id_env}가 설정되지 않았습니다. README의 'chat_id 확인'을 참고하세요.")
    return Telegram(s.bot_token, s.chat_id)


def cmd_send(args, config: Config, history: History) -> int:
    day = today_in(config)
    if not args.force and not args.dry_run and history.daily_entry(day):
        log.info("오늘(%s) 노트는 이미 보냈습니다. 다시 보내려면 --force를 쓰세요.", day)
        return 0
    topic = None
    if args.topic:
        topic = config.find_topic(args.topic)
        if topic is None:
            log.error("주제 '%s'를 찾지 못했습니다. 가능한 값: %s", args.topic, ", ".join(t.key for t in config.topics))
            return 2
    rng = random.Random(args.seed) if args.seed is not None else None
    tg = None if args.dry_run else make_telegram(config)
    create_and_send(config, history, day, tg=tg, topic=topic, trigger="daily", dry_run=args.dry_run, rng=rng)
    if not args.dry_run:
        removed = history.prune(day, config.settings.retention_days)
        if removed:
            log.info("오래된 기록 %d개를 정리했습니다.", removed)
        history.save()
    return 0


# --- 봇 명령 ------------------------------------------------------------------

HELP_TEXT = (
    "<b>📚 데일리 지식 봇</b>\n"
    "/today — 오늘 보낸 노트 다시 보기\n"
    "/now [주제] — 지금 바로 새 노트 받기 (예: /now 계면, /now LLM)\n"
    "/topics — 주제 목록과 진도\n"
    "/history — 최근 7일 기록\n\n"
    "<i>명령은 1시간마다 확인하므로 답장이 늦을 수 있습니다.</i>"
)


def topics_text(config: Config, history: History) -> str:
    lines = ["<b>📚 주제 목록</b>"]
    for t in config.topics:
        done = len({e["concept"] for e in history.covered(t.key)})
        lines.append(f"{t.emoji} {t.category} › {t.name} (<code>{t.key}</code>) — {done}/{len(t.concepts)}개 공부함")
    return "\n".join(lines)


def history_text(config: Config, history: History, day: date) -> str:
    entries = history.recent(day, 7)
    if not entries:
        return "최근 7일 동안 보낸 노트가 없습니다."
    by_key = {t.key: t for t in config.topics}
    lines = ["<b>🗓 최근 7일</b>"]
    for e in reversed(entries):
        t = by_key.get(e["topic"])
        emoji = t.emoji if t else "📘"
        label = t.label if t else e["topic"]
        lines.append(f"{e['date'][5:]} {emoji} {label} — {e['title']}")
    return "\n".join(lines)


def parse_command(text: str) -> tuple[str, str]:
    parts = (text or "").strip().split(maxsplit=1)
    if not parts or not parts[0].startswith("/"):
        return "", ""
    cmd = parts[0][1:].split("@", 1)[0].lower()
    return cmd, parts[1].strip() if len(parts) > 1 else ""


def cmd_commands(args, config: Config, history: History) -> int:
    s = config.settings
    if not s.bot_token or not s.chat_id:
        # chat_id가 없을 때 getUpdates를 부르면 메시지가 읽음 처리되어 사용자가 chat_id를 확인할 수 없게 된다.
        log.warning("TELEGRAM_BOT_TOKEN 또는 TELEGRAM_CHAT_ID가 없어 봇 명령 처리를 건너뜁니다.")
        return 0
    tg = Telegram(s.bot_token, s.chat_id)
    updates = tg.get_updates(history.telegram_offset)
    day = today_in(config)
    now_count = 0
    for u in updates:
        history.telegram_offset = max(history.telegram_offset, u["update_id"] + 1)
        msg = u.get("message") or {}
        chat = str((msg.get("chat") or {}).get("id", ""))
        if chat != s.chat_id:
            continue  # 허용된 대화방이 아니면 응답하지 않는다
        cmd, arg = parse_command(msg.get("text", ""))
        if not cmd:
            continue
        log.info("명령 처리: /%s %s", cmd, arg)
        try:
            reply = handle_command(cmd, arg, msg, args, config, history, tg, day, now_count)
            if reply:
                if args.dry_run:
                    print(reply)
                else:
                    tg.send_message(reply)
        except Exception:  # noqa: BLE001 - 한 명령이 실패해도 나머지는 처리하고 offset을 저장한다
            log.exception("/%s 처리 중 오류", cmd)
        if cmd == "now":
            now_count += 1
    if not args.dry_run:
        history.save()
    return 0


def handle_command(cmd, arg, msg, args, config, history, tg, day, now_count) -> str | None:
    if cmd in ("start", "help"):
        return HELP_TEXT
    if cmd == "topics":
        return topics_text(config, history)
    if cmd == "history":
        return history_text(config, history, day)
    if cmd == "today":
        entries = history.entries_on(day)
        if not entries:
            return "오늘은 아직 보낸 노트가 없습니다. /now 로 바로 받아 보세요."
        by_key = {t.key: t for t in config.topics}
        for e in entries:
            lesson, topic = history.load_lesson(e), by_key.get(e["topic"])
            if lesson and topic and not args.dry_run:
                deliver(tg, lesson, topic, day, use_poll=False)
        return None
    if cmd == "now":
        if now_count >= MAX_NOW_PER_RUN:
            return f"/now는 한 번에 {MAX_NOW_PER_RUN}개까지만 처리합니다. 다음 확인 때 다시 요청해 주세요."
        if time.time() - int(msg.get("date", time.time())) > STALE_COMMAND_HOURS * 3600:
            return None  # 오래된 요청은 조용히 넘긴다
        topic = None
        if arg:
            topic = config.find_topic(arg)
            if topic is None:
                return f"'{arg}' 주제를 찾지 못했습니다.\n\n" + topics_text(config, history)
        create_and_send(config, history, day, tg=tg, topic=topic, trigger="command", dry_run=args.dry_run)
        return None
    return "모르는 명령입니다.\n\n" + HELP_TEXT


def main(argv: list[str] | None = None) -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--config", default=None, help="설정 파일 경로(기본: config/topics.yaml)")
    common.add_argument("--history", default=None, help="기록 파일 경로(기본: data/history.json)")
    common.add_argument("--dry-run", action="store_true", help="발송·저장 없이 출력만")
    parser = argparse.ArgumentParser(prog="knowledge_bot", description="매일 공부 노트를 텔레그램으로 보내는 봇")
    sub = parser.add_subparsers(dest="command")
    p_send = sub.add_parser("send", parents=[common], help="오늘의 노트 보내기(기본)")
    p_send.add_argument("--topic", help="주제 지정(key 또는 이름, 예: 계면, ai-llm)")
    p_send.add_argument("--force", action="store_true", help="오늘 이미 보냈어도 다시 보내기")
    p_send.add_argument("--seed", type=int, help="무작위 선택 시드(테스트용)")
    sub.add_parser("commands", parents=[common], help="텔레그램 봇 명령 처리")

    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] not in ("send", "commands", "-h", "--help"):
        argv = ["send", *argv]  # 하위 명령을 생략하면 send
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    try:
        from dotenv import load_dotenv  # 선택 사항

        load_dotenv()
    except ImportError:
        pass

    config = load_config(args.config) if args.config else load_config()
    history = History(args.history) if args.history else History()
    try:
        if args.command == "commands":
            return cmd_commands(args, config, history)
        return cmd_send(args, config, history)
    except TelegramError as e:
        log.error("%s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
