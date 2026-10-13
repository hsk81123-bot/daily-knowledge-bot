import json
import time
from datetime import date
from unittest import mock

import pytest

from knowledge_bot import main as main_mod
from knowledge_bot.history import History
from knowledge_bot.telegram import Telegram, TelegramError

DAY = date(2026, 10, 14)


@pytest.fixture
def env(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:abc")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "42")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(main_mod, "today_in", lambda config: DAY)


@pytest.fixture
def fake_lesson(sample_lesson, monkeypatch):
    def make(pick, settings, client=None):
        out = dict(sample_lesson)
        out["concept"] = pick.concept.name
        return out

    monkeypatch.setattr(main_mod, "make_lesson", make)


@pytest.fixture
def sent(monkeypatch):
    calls = []

    def call(self, method, payload=None, timeout=30):
        calls.append((method, payload))
        if method == "getUpdates":
            return getattr(self, "_updates", [])
        return {"message_id": len(calls)}

    monkeypatch.setattr(Telegram, "call", call)
    return calls


def run(tmp_path, *args):
    return main_mod.main([*args, "--history", str(tmp_path / "history.json")])


def test_send_records_history(tmp_path, env, fake_lesson, sent):
    assert run(tmp_path, "send", "--topic", "계면", "--seed", "1") == 0
    methods = [m for m, _ in sent]
    assert methods.count("sendMessage") >= 1 and "sendPoll" in methods
    history = History(tmp_path / "history.json")
    entry = history.lessons[0]
    assert entry["topic"] == "battery-interface" and entry["trigger"] == "daily"
    assert (tmp_path / entry["file"]).exists()
    assert (tmp_path / entry["file"]).with_suffix(".md").exists()
    # 마지막 메시지에 링크 버튼
    last_msg = [p for m, p in sent if m == "sendMessage"][-1]
    assert "inline_keyboard" in last_msg["reply_markup"]


def test_send_once_per_day(tmp_path, env, fake_lesson, sent):
    run(tmp_path, "send")
    n = len(sent)
    run(tmp_path, "send")
    assert len(sent) == n
    run(tmp_path, "send", "--force")
    assert len(sent) > n
    assert len(History(tmp_path / "history.json").lessons) == 2


def test_dry_run_sends_nothing(tmp_path, env, fake_lesson, sent, capsys):
    assert run(tmp_path, "--dry-run") == 0
    assert sent == []
    assert not (tmp_path / "history.json").exists()
    assert "오늘의 지식" in capsys.readouterr().out


def test_missing_chat_id_fails_send(tmp_path, env, fake_lesson, sent, monkeypatch):
    monkeypatch.delenv("TELEGRAM_CHAT_ID")
    assert run(tmp_path, "send") == 1
    assert sent == []


def test_commands_skip_without_chat_id(tmp_path, env, sent, monkeypatch):
    monkeypatch.delenv("TELEGRAM_CHAT_ID")
    assert run(tmp_path, "commands") == 0
    assert sent == []  # getUpdates도 호출하지 않는다


def _update(uid, chat, text, age=0):
    return {"update_id": uid, "message": {"chat": {"id": chat}, "text": text, "date": int(time.time()) - age}}


def test_commands_only_allowed_chat(tmp_path, env, fake_lesson, sent, monkeypatch):
    monkeypatch.setattr(Telegram, "_updates", [
        _update(10, 999, "/now"),           # 모르는 사람
        _update(11, 42, "/topics"),
        _update(12, 42, "/now LLM"),
        _update(13, 42, "/now", age=7 * 3600),  # 오래된 요청
        _update(14, 42, "/history@my_bot"),
    ], raising=False)
    assert run(tmp_path, "commands") == 0
    history = History(tmp_path / "history.json")
    assert history.telegram_offset == 15
    assert [e["topic"] for e in history.lessons] == ["ai-llm"]
    assert history.lessons[0]["trigger"] == "command"
    texts = [p["text"] for m, p in sent if m == "sendMessage"]
    assert any("주제 목록" in t for t in texts)
    assert any("최근 7일" in t for t in texts)
    assert all(p.get("chat_id") in (None, "42") for m, p in sent if m != "getUpdates")


def test_now_limit_per_run(tmp_path, env, fake_lesson, sent, monkeypatch):
    monkeypatch.setattr(Telegram, "_updates", [_update(i, 42, "/now") for i in range(1, 5)], raising=False)
    run(tmp_path, "commands")
    assert len(History(tmp_path / "history.json").lessons) == main_mod.MAX_NOW_PER_RUN


def test_today_resends(tmp_path, env, fake_lesson, sent, monkeypatch):
    run(tmp_path, "send", "--topic", "온톨로지")
    sent.clear()
    monkeypatch.setattr(Telegram, "_updates", [_update(1, 42, "/today")], raising=False)
    run(tmp_path, "commands")
    texts = [p["text"] for m, p in sent if m == "sendMessage"]
    assert any("SEI: 음극을 지키는 얇은 막" in t for t in texts)


def test_chat_not_found_message(caplog):
    session = mock.MagicMock()
    resp = mock.MagicMock(status_code=400)
    resp.json.return_value = {"ok": False, "description": "Bad Request: chat not found"}
    session.post.return_value = resp
    tg = Telegram("t", "1", session=session)
    with pytest.raises(TelegramError):
        tg.send_message("hi")
    assert "Start" in caplog.text
    assert session.post.call_count == 1  # 4xx는 재시도하지 않는다


def test_prune(tmp_path, sample_lesson):
    h = History(tmp_path / "history.json")
    old = h.add(date(2025, 1, 1), "ai-llm", sample_lesson, "md", "daily")
    h.add(DAY, "ai-llm", sample_lesson, "md", "daily")
    assert h.prune(DAY, 365) == 1
    assert len(h.lessons) == 1
    assert not (tmp_path / old["file"]).exists()
