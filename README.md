# 📚 데일리 지식 봇 (배터리 × AI)

매일 아침 **공부용 지식 노트 한 편**을 텔레그램으로 보내 주는 봇입니다. 뉴스가 아니라 오래 남는 개념을 다룹니다.
아래 8개 주제 중 **매일 하나를 무작위로** 골라, 아직 배우지 않은 개념 하나를 정리해 보냅니다.

| 분야 | 주제 |
|---|---|
| 🔋 배터리 | 🧪 소재 · 🧱 계면 · ⚡ 전기화학 · 🔬 분석법 |
| 🤖 AI | 📊 머신러닝 · 🧠 딥러닝 · 💬 LLM · 🕸️ 온톨로지 |

- 주제마다 개념 15개, 총 **120편의 공부 노트를 미리 써서** `content/lessons/`에 넣어 두었습니다. **API 키 없이, 비용 0원**으로 매일 완성된 노트가 옵니다.
- 같은 개념은 다시 보내지 않습니다. 최근 3일 안에 보낸 주제는 피해서 고르기 때문에 같은 주제가 연달아 나오지도 않습니다.
- 120편을 다 보내면(약 4개월) 가장 오래전에 배운 개념부터 **복습** 표시를 달고 다시 보냅니다.
  (선택) `ANTHROPIC_API_KEY`를 넣으면 그때부터는 Claude가 아직 안 배운 새 개념을 골라 노트를 새로 씁니다.
- 노트 구성: 한 줄 요약 → 본문 3~4단락 → 핵심 수식 → 예시 → 흔한 오해 → 배터리 × AI 연결점 → 키워드 → 다음에 공부할 것.
- 퀴즈는 **텔레그램 퀴즈 투표**로 따로 보냅니다(정답을 누르면 해설이 보임). 길이 제한을 넘으면 본문에 스포일러로 넣습니다.
- 보낸 노트는 `data/lessons/`에 마크다운으로 쌓여서 GitHub에서 복습 노트처럼 볼 수 있습니다.

## 메시지 예시

```text
⚡ 오늘의 지식 | 배터리 › 전기화학
10월 14일 (수) · 중급

버틀러-볼머 식: 전극 반응 속도는 과전압에 지수적으로 반응한다

💡 전극 반응의 알짜 전류는 산화·환원 두 방향 속도의 차이이고, 과전압이 커질수록 한쪽이 지수적으로 우세해진다.

📖 정의
버틀러-볼머 식(Butler–Volmer equation)은 전하전달이 속도를 결정할 때 전극 전류 밀도와 과전압(η)의 관계를 나타낸다. 평형 전위에서는 산화 전류와 환원 전류가 같아 알짜 전류가 0이지만, 두 방향 반응은 계속 일어나고 있다. 이때 한 방향의 전류 크기를 교환 전류 밀도(i₀)라고 한다.

📖 원리
전위를 바꾸면 산화와 환원의 활성화 에너지 장벽이 서로 반대 방향으로 기울어진다. 전달 계수(α)는 이 전위 변화가 장벽을 얼마나 낮추는지를 나타내며, 보통 0.5 근처로 가정한다. 그래서 η가 작을 때는 전류가 η에 거의 비례하고(선형 영역), η가 크면 한쪽 항만 남아 로그 관계(타펠 영역)가 된다.

📖 배터리에서의 의미
i₀가 큰 전극은 같은 전류를 작은 과전압으로 흘릴 수 있다. 선형 영역에서 전하전달 저항은 R_ct = RT/(nF·i₀)로, EIS 반원의 지름과 연결된다. 저온에서 i₀가 크게 줄어드는 것이 저온 출력 저하와 리튬 도금 위험의 한 원인이다.

🧮 핵심 수식·원리
i = i₀ · [exp(α_a·F·η/RT) − exp(−α_c·F·η/RT)]
(i₀: 교환 전류 밀도, α_a·α_c: 전달 계수, η: 과전압, F: 패러데이 상수)

🔍 예시·적용
같은 셀을 25 °C와 −10 °C에서 EIS로 측정하면 −10 °C에서 전하전달 반원이 훨씬 커진다. 아레니우스 플롯으로 R_ct의 활성화 에너지를 구할 수 있다.

⚠️ 흔한 오해
과전압이 크다고 무조건 전하전달이 느린 것은 아니다. 전체 과전압에는 옴 저항과 농도(확산) 과전압도 섞여 있으니 측정법으로 나눠 봐야 한다.

🔗 배터리 × AI
DFN 같은 물리 기반 모델은 계면마다 버틀러-볼머 식을 쓰고, 이를 신경망과 결합한 하이브리드 모델로 배터리 상태를 추정하는 연구가 많다.

🏷 키워드
교환 전류 밀도(exchange current density) · 전달 계수(transfer coefficient) · 전하전달 저항(charge-transfer resistance)

➡️ 다음에 공부할 것
• 타펠 식과 타펠 기울기
• EIS 등가회로
• 마커스 이론

📚 참고 문헌
• A. J. Bard, L. R. Faulkner, Electrochemical Methods, 2판, 2001

[원문/학습 링크 버튼] 📖 위키백과 | 🎓 Google Scholar | 📺 YouTube
[퀴즈 투표] ❓ 교환 전류 밀도 i₀가 커지면 전하전달 저항 R_ct는? → 선택지 4개, 정답 공개 시 해설 표시
```

## 동작 방식

노트는 아래 순서로 찾아서 보냅니다.

| 순서 | 출처 | 언제 |
|---|---|---|
| 1 | `content/lessons/<주제>.yaml`에 미리 써 둔 노트 | 기본(120개 개념 모두 준비됨) |
| 2 | Claude(기본 `claude-opus-5-5`)가 새로 쓴 노트 | 라이브러리에 없는 개념이고 `ANTHROPIC_API_KEY`가 있을 때 |
| 3 | 위키백과 요약(한국어 문서가 있으면 한국어) | 라이브러리에 없고 키도 없을 때 |
| 4 | 개념 이름과 검색 링크만 | 위의 것이 모두 실패했을 때(발송 자체는 계속) |

링크 버튼은 위키백과, Google Scholar, (AI 주제) arXiv / (배터리 주제) YouTube **검색 링크**라서 깨진 주소가 나오지 않습니다.
Claude에게는 URL을 쓰지 말고, 확실히 아는 교과서·리뷰 논문만 참고 문헌으로 적도록 지시했습니다.

## 폴더 구조

```text
config/topics.yaml          주제 8개와 개념 목록, 설정
content/lessons/            미리 써 둔 공부 노트 120편(주제별 YAML)
knowledge_bot/
  main.py                   CLI (send / commands)
  selector.py               오늘의 주제·개념 고르기
  library.py                미리 써 둔 노트 읽기
  lesson.py                 노트 고르기: 라이브러리 → Claude → 위키백과
  formatter.py              텔레그램 HTML, 퀴즈 투표, 마크다운 보관본
  telegram.py               Bot API 호출(재시도, chat not found 안내)
  history.py                data/history.json 기록과 정리
data/history.json           발송 기록, 봇 명령 offset
data/lessons/               보낸 노트(.md, .json)
scripts/commit-data.sh      워크플로에서 기록 커밋·push
.github/workflows/          daily.yml(매일 발송), commands.yml(봇 명령), tests.yml
tests/                      pytest(네트워크는 전부 모킹)
```

## 설치 가이드

### 1. 텔레그램 봇 만들기
1. 텔레그램에서 **@BotFather** → `/newbot` → 이름과 아이디를 정하면 토큰이 나옵니다. 토큰은 채팅이나 코드에 붙여 넣지 마세요.
   - 이미 쓰는 봇(예: Daily Jazz 봇)을 같이 써도 됩니다.
2. 만든 봇을 검색해 대화를 열고 **시작(Start)** 을 누릅니다. 안 누르면 발송할 때 `chat not found` 오류가 납니다.

### 2. chat_id 확인
1. 봇에게 아무 메시지나 보냅니다.
2. 브라우저에서 `https://api.telegram.org/bot<토큰>/getUpdates` 를 엽니다.
3. `"chat":{"id":123456789,...}` 의 숫자가 chat_id입니다. 결과가 `[]`이면 봇에게 메시지를 한 번 더 보내고 새로고침하세요.
   - @userinfobot 으로 내 ID를 확인해도 됩니다. 기존 봇과 같은 대화방으로 받으려면 기존 chat_id를 그대로 쓰면 됩니다.
   - `TELEGRAM_CHAT_ID`를 넣기 전에는 명령 폴링 워크플로가 getUpdates를 호출하지 않습니다(호출하면 메시지가 읽음 처리되어 이 단계에서 chat_id가 안 보이게 됩니다).

### 3. GitHub Secrets 등록
저장소 **Settings → Secrets and variables → Actions → New repository secret**

| 이름 | 필수 | 설명 |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | ✅ | BotFather 토큰 |
| `TELEGRAM_CHAT_ID` | ✅ | 위에서 확인한 숫자 |
| `ANTHROPIC_API_KEY` | 선택 | 없어도 됩니다. 미리 써 둔 노트를 다 쓴 뒤 새 노트를 만들 때만 사용 |

모델을 바꾸려면 같은 화면의 **Variables** 탭에 `CLAUDE_MODEL`(예: `claude-haiku-5-5`)을 추가하세요.

### 4. 워크플로 쓰기 권한 켜기
**Settings → Actions → General → Workflow permissions → Read and write permissions** → Save.
발송 기록을 저장소에 커밋하기 때문에 필요합니다.

### 5. main 브랜치에 머지
수동 실행 버튼(Run workflow)과 예약 실행은 **기본 브랜치(main)에 있는 워크플로에만** 생깁니다. 이 브랜치의 PR을 먼저 머지하세요.

### 6. 첫 실행
**Actions → Daily knowledge → Run workflow**
- **`dry_run`은 끈 채로** 실행해야 텔레그램으로 옵니다. `dry_run`을 켜면 발송·기록 없이 Actions 로그에만 메시지를 찍습니다(미리보기용).
- `topic`에 `계면`, `LLM` 같은 이름을 넣으면 그 주제로 보냅니다.
- 실패하면 로그를 Claude에게 보여 주세요.

이후에는 **매일 05:00 KST**에 자동으로 옵니다. GitHub의 예약 실행은 1~2시간씩 늦게 시작하는 일이 잦아서(실제로 07:00 예약이 08:30~09:00에 도착),
02:07·03:07·04:07 KST에 미리 시작해 **05:00까지 기다렸다가** 보냅니다. 세 번 중 먼저 도착한 실행만 보내고 나머지는 건너뜁니다
(Actions 탭에 건너뛰거나 취소된 실행이 보여도 정상). 세 번 모두 05:00 이후에 시작되면 그때 바로 보냅니다.
시간을 바꾸려면 `.github/workflows/daily.yml`에서 cron 세 줄(UTC = KST − 9시간)과 `Wait until` 단계의 `05:00`을 함께 고치세요.

## 봇 명령

| 명령 | 설명 |
|---|---|
| `/today` | 오늘 보낸 노트 다시 보기 |
| `/now [주제]` | 지금 바로 새 노트 받기. 예: `/now`(무작위), `/now 분석법`, `/now ai-llm` |
| `/topics` | 주제 목록과 주제별 진도(배운 개념 수) |
| `/history` | 최근 7일 기록 |
| `/help` | 도움말 |

- 명령은 **1시간마다** 확인합니다(`commands.yml`). 그래서 답장이 최대 1시간쯤 늦을 수 있습니다. 빠른 응답이 필요하면 서버에서 cron으로 짧게 돌리세요(아래 참고).
- `TELEGRAM_CHAT_ID`로 설정한 대화방의 명령에만 응답합니다. 모르는 사람이 `/now`를 반복해 API 비용을 쓰는 일을 막기 위해서입니다.
- `/now`는 한 번 확인할 때 2개까지만 처리하고, 6시간보다 오래된 `/now` 요청은 무시합니다.

## 비용과 사용량

- **Claude API**: 기본 설정(키 없음)에서는 쓰지 않으므로 비용이 없습니다. 키를 넣을 경우 Claude 구독(Pro/Max)과 API는 결제가 따로입니다. [console.anthropic.com](https://console.anthropic.com)에서 키를 만들고 크레딧을 충전해야 합니다.
  노트 한 편은 대략 입력 2천 토큰, 출력 수천 토큰이라 `claude-opus-5-5` 기준 한 편에 대략 0.1달러 안팎, 매일 받으면 한 달에 몇 달러 수준입니다.
  더 아끼려면 `CLAUDE_MODEL=claude-haiku-5-5`로 바꾸세요(노트 품질은 조금 떨어질 수 있음).
- **GitHub Actions**: 공개 저장소는 무료입니다. 비공개 저장소는 월 2,000분 무료인데, 명령 폴링이 1시간마다 1분씩 잡혀 **한 달 약 720분**,
  매일 발송이 **약 30~60분**을 씁니다. 명령을 안 쓰면 `commands.yml`의 `schedule` 부분을 지우거나 간격을 늘리세요(예: `17 */3 * * *`).

## 주제·개념 추가하기

`config/topics.yaml`의 `topics`에 항목을 추가하면 됩니다.

```yaml
  - key: battery-modeling          # 영문 고유 키
    category: 배터리
    name: 모델링
    emoji: "🧮"
    description: 전기화학·등가회로·데이터 기반 배터리 모델
    concepts:
      - { name: "등가회로 모델(ECM)", en: "Equivalent circuit model battery" }
      - { name: "PyBaMM으로 DFN 모델 돌려 보기", en: "PyBaMM" }
```

- `en`은 위키백과·Scholar 검색어로 쓰입니다.
- 새 개념의 노트는 `content/lessons/<주제 key>.yaml`에 같은 형식으로 추가하세요(`concept`은 `topics.yaml`의 `name`과 글자까지 같아야 함).
  노트를 안 쓰면 그 개념은 Claude(키가 있을 때)나 위키백과 요약으로 보냅니다.
  `python -m pytest tests/test_library.py`가 형식(퀴즈 4지선다, 텔레그램 투표 길이 제한 등)을 검사합니다.
- 기존 주제의 `concepts`에 개념을 더 넣어도 됩니다. 이미 배운 개념은 기록을 보고 건너뜁니다.
- `settings.avoid_recent_days`(최근 며칠 주제 피하기), `settings.audience`(독자 수준), `settings.quiz_as_poll`로 동작을 조정할 수 있습니다.

## 로컬·서버에서 실행

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # 값 채우기

python -m knowledge_bot --dry-run            # 발송·저장 없이 출력
python -m knowledge_bot send --topic 계면     # 한 주제만
python -m knowledge_bot send --force         # 오늘 이미 보냈어도 다시
python -m knowledge_bot commands             # 봇 명령 한 번 처리
python -m pytest -q                          # 테스트
```

서버 cron 예시(서버 시간대가 KST일 때). 서버에서 돌릴 때는 GitHub Actions의 schedule을 꺼서 두 번 보내지 않게 하세요.

```cron
0 5 * * *    cd /path/to/daily-knowledge-bot && .venv/bin/python -m knowledge_bot send >> bot.log 2>&1
*/5 * * * *  cd /path/to/daily-knowledge-bot && .venv/bin/python -m knowledge_bot commands >> bot.log 2>&1
```

## 문제 해결

| 증상 | 원인과 해결 |
|---|---|
| `chat not found` | 봇에게 Start를 안 눌렀거나 chat_id가 틀림 |
| `Unauthorized` | 봇 토큰이 틀림 |
| 커밋 단계에서 403 | Workflow permissions를 Read and write로 바꾸지 않음 |
| Run workflow 버튼이 없음 | 워크플로가 아직 main에 머지되지 않음 |
| Run workflow는 성공인데 메시지가 안 옴 | `dry_run`을 켜고 실행함. 끄고 다시 실행 |
| 노트 끝에 "위키백과 요약으로 보냈습니다" | 미리 써 둔 노트가 없는 개념이고 Claude 키도 없음. `content/lessons/`에 노트 추가 |
| 같은 날 두 번 안 옴 | 정상. 하루 한 번만 보냄. 다시 받으려면 `force` 또는 `/now` |
