# 열화 모드: 리튬을 잃었나, 활물질을 잃었나

🔬 배터리 › 분석법 · 2026-11-22 · 중급

> 💡 용량 감소의 원인은 크게 쓸 수 있는 리튬의 손실(LLI)과 양극·음극 활물질 손실(LAM)로 나뉘며, 저율 충방전 곡선 분석으로 셀을 열지 않고도 그 비율을 추정할 수 있다.

## 수명 시험

정해진 C-rate, 전압 범위, 온도로 충방전을 반복하며 용량과 저항을 추적한다(사이클 수명). 충방전 없이 특정 SOC와 온도로 보관하며 열화를 보는 것이 캘린더 수명이다. 주기적으로 아주 느린 충방전(예: C/20)과 펄스 시험을 끼워 넣어 진단 데이터를 얻는다(RPT, 기준 성능 시험).

## 열화 모드

LLI(loss of lithium inventory)는 SEI 성장, 리튬 도금 같은 부반응으로 양·음극 사이를 오갈 리튬이 줄어든 것이다. LAM(loss of active material)은 입자 균열, 접촉 손실, 구조 붕괴로 리튬을 받아 줄 활물질이 줄어든 것으로 양극(LAM_PE)과 음극(LAM_NE)을 나눈다. 저항 증가는 용량을 직접 줄이지 않지만 높은 C-rate에서 쓸 수 있는 용량을 줄인다.

## 분리하는 방법

반쪽 셀로 측정한 양극·음극 OCV 곡선을 늘이고 옮겨 풀셀 저율 곡선에 맞추면(전극 정렬, 차분 전압 분석) 각 전극의 용량과 상대 위치가 나온다. 전극 용량 감소는 LAM을, 두 전극 곡선의 상대 위치 이동은 LLI를 뜻한다. dQ/dV·dV/dQ 피크 변화를 함께 본다.

## 🧮 핵심 수식·원리

```
풀셀 OCV(Q) = U_PE((Q − δ_PE)/C_PE) − U_NE((Q − δ_NE)/C_NE)
C_PE·C_NE 감소 → LAM,  δ(전극 간 오프셋) 변화 → LLI
```

## 🔍 예시·적용

NCM/흑연 셀을 고온에서 사이클하면 초기에는 LLI가 주된 열화이다가, 어느 순간 음극 LAM과 리튬 도금이 겹치며 용량이 급격히 떨어지는 '무릎(knee)'이 나타나기도 한다.

## ⚠️ 흔한 오해

용량 유지율 곡선만 보면 열화 원인을 알 수 있다고 생각하기 쉽지만, 같은 용량 감소라도 LLI와 LAM의 조합은 여러 가지일 수 있다. 진단 시험이 따로 필요하다.

## 🔗 배터리 × AI

시뮬레이션으로 LLI·LAM 조합별 dQ/dV 곡선을 대량 생성해 학습한 모델로 실제 셀의 열화 모드를 추정하는 방법이 연구된다. 초기 사이클로 수명을 예측한 Severson 등의 연구도 유명하다.

## ❓ 퀴즈

SEI가 계속 자라며 리튬이 소모되는 열화는 어떤 모드에 해당하나?

- A. LAM_PE
- B. LAM_NE
- C. LLI
- D. 옴 저항 감소

<details><summary>정답 보기</summary>

**C** — SEI 성장은 양·음극 사이를 오갈 리튬을 소모하므로 리튬 재고 손실(LLI)이다.

</details>

## 🏷 키워드

리튬 재고 손실 (loss of lithium inventory) · 활물질 손실 (loss of active material) · 기준 성능 시험 (reference performance test)

## ➡️ 다음에 공부할 것

- dQ/dV 미분 용량 분석
- 쿨롱 효율과 에너지 효율
- 그래디언트 부스팅(XGBoost, LightGBM)

## 📚 참고 문헌

- C. R. Birkl, M. R. Roberts, E. McTurk, P. G. Bruce, D. A. Howey, Degradation diagnostics for lithium ion cells, J. Power Sources, 2017
- K. A. Severson et al., Data-driven prediction of battery cycle life before capacity degradation, Nature Energy, 2019

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Battery+degradation+modes+loss+of+lithium+inventory)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Battery+degradation+modes+loss+of+lithium+inventory)
- [📺 YouTube](https://www.youtube.com/results?search_query=Battery+degradation+modes+loss+of+lithium+inventory)
