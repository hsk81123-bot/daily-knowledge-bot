import json
from datetime import date
from pathlib import Path

import pytest

from knowledge_bot.config import load_config
from knowledge_bot.history import History

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def config():
    return load_config(ROOT / "config" / "topics.yaml")


@pytest.fixture
def history(tmp_path):
    return History(tmp_path / "history.json")


@pytest.fixture
def sample_lesson():
    return {
        "concept": "SEI(고체 전해질 계면)의 형성과 조성",
        "concept_en": "Solid electrolyte interphase",
        "title": "SEI: 음극을 지키는 얇은 막",
        "level": "중급",
        "one_liner": "SEI는 전해질이 환원되며 생긴 이온 전도성·전자 절연성 피막이다.",
        "sections": [
            {"heading": "정의", "body": "첫 충전 때 전해질이 환원되어 <막>이 생긴다."},
            {"heading": "원리", "body": "전해질의 LUMO가 음극 전위보다 낮으면 환원된다."},
        ],
        "formula": "Q_irr = Q_charge − Q_discharge",
        "example": "FEC 첨가제는 LiF가 많은 SEI를 만든다.",
        "misconception": "SEI는 한 번 생기면 끝이 아니다.",
        "connection": "EIS 데이터로 SEI 성장을 예측하는 ML 모델이 연구된다.",
        "quiz": {
            "question": "SEI의 바람직한 성질은?",
            "choices": ["전자 전도성, 이온 절연성", "이온 전도성, 전자 절연성", "둘 다 전도성", "둘 다 절연성"],
            "answer_index": 1,
            "explanation": "리튬 이온은 통과시키고 전자는 막아야 전해질 분해가 멈춘다.",
        },
        "keywords": [{"ko": "고체 전해질 계면", "en": "SEI"}],
        "next_topics": ["리튬 도금", "FEC 첨가제"],
        "references": [],
        "source": "claude",
    }


def write_history(history, entries):
    history.data["lessons"] = entries
    history.save()
