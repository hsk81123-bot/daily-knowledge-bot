"""텔레그램 Bot API 호출."""
from __future__ import annotations

import logging
import time

import requests

log = logging.getLogger(__name__)


class TelegramError(Exception):
    pass


class Telegram:
    def __init__(self, token: str, chat_id: str, retries: int = 3, session: requests.Session | None = None):
        if not token:
            raise TelegramError("TELEGRAM_BOT_TOKEN이 비어 있습니다.")
        self.base = f"https://api.telegram.org/bot{token}"
        self.chat_id = chat_id
        self.retries = retries
        self.session = session or requests.Session()

    def call(self, method: str, payload: dict | None = None, timeout: int = 30) -> dict | list:
        last_error = None
        for attempt in range(1, self.retries + 1):
            try:
                r = self.session.post(f"{self.base}/{method}", json=payload or {}, timeout=timeout)
                data = r.json()
            except (requests.RequestException, ValueError) as e:
                last_error = f"네트워크 오류: {e}"
            else:
                if data.get("ok"):
                    return data["result"]
                desc = data.get("description", "")
                if r.status_code == 429:
                    wait = int(data.get("parameters", {}).get("retry_after", 5))
                    log.warning("텔레그램 속도 제한, %s초 후 재시도", wait)
                    time.sleep(min(wait, 60))
                    last_error = desc
                    continue
                if "chat not found" in desc.lower():
                    log.error(
                        "텔레그램 'chat not found': 봇에게 먼저 Start(시작)를 눌렀는지, "
                        "TELEGRAM_CHAT_ID가 맞는지 확인하세요."
                    )
                if r.status_code < 500:
                    raise TelegramError(f"{method} 실패: {desc}")
                last_error = desc
            if attempt < self.retries:
                time.sleep(2 ** attempt)
        raise TelegramError(f"{method} 실패({self.retries}회 시도): {last_error}")

    def send_message(self, text: str, buttons: list[tuple[str, str]] | None = None, chat_id: str | None = None) -> dict:
        payload = {
            "chat_id": chat_id or self.chat_id,
            "text": text,
            "parse_mode": "HTML",
            "link_preview_options": {"is_disabled": True},
        }
        if buttons:
            # 한 줄에 버튼 3개씩
            rows = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
            payload["reply_markup"] = {"inline_keyboard": [[{"text": t, "url": u} for t, u in row] for row in rows]}
        return self.call("sendMessage", payload)

    def send_quiz(self, poll: dict, chat_id: str | None = None) -> dict:
        payload = {
            "chat_id": chat_id or self.chat_id,
            "question": poll["question"],
            "options": [{"text": o} for o in poll["options"]],
            "type": "quiz",
            "correct_option_id": poll["correct_option_id"],
            "is_anonymous": True,
        }
        if poll.get("explanation"):
            payload["explanation"] = poll["explanation"]
        return self.call("sendPoll", payload)

    def get_updates(self, offset: int) -> list[dict]:
        return self.call("getUpdates", {"offset": offset, "timeout": 0, "allowed_updates": ["message"]})
