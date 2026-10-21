# DSC·ARC: 열폭주가 언제 시작되는지 재기

🔬 배터리 › 분석법 · 2026-10-22 · 중급

> 💡 DSC는 소량 시료의 발열 반응 온도와 열량을, ARC는 셀이 스스로 데워지기 시작하는 온도와 열폭주 진행을 단열 조건에서 측정한다.

## DSC

시차 주사 열량계(DSC)는 시료와 기준을 같은 속도로 가열하며 들어가거나 나오는 열 흐름 차이를 잰다. 충전된 전극 조각과 전해질을 밀폐 팬에 넣어 측정하면, SEI 분해, 음극과 전해질의 반응, 양극 산소 방출에 따른 발열이 각각 어느 온도에서 얼마나 일어나는지 볼 수 있다. 시료가 수 mg이라 소재 비교에 좋다.

## ARC

가속 속도 열량계(ARC)는 셀을 단열 상태로 두고 '가열-대기-탐색'을 반복한다. 셀이 스스로 일정 속도 이상(예: 0.02 °C/min) 데워지면 그때부터 주변 온도를 셀 온도에 맞춰 따라가며, 열이 빠져나가지 않는 최악의 상황에서 온도가 어떻게 치솟는지 기록한다.

## 읽는 지표

ARC에서는 자가 발열 시작 온도(T1), 열폭주 시작 온도(T2), 최고 온도(T3)를 본다. 대체로 SEI 분해가 가장 먼저(대략 80~120 °C) 시작되고, 분리막 녹음, 양극 분해와 산소 방출, 전해질 연소가 이어진다. 충전 상태가 높고 니켈 함량이 높을수록 시작 온도가 낮고 발열이 크다.

## 🧮 핵심 수식·원리

```
DSC: 발열량 ΔH = ∫ (dQ/dt) dt
단열 온도 상승: ΔT_ad = Q_total / (m · c_p)
```

## 🔍 예시·적용

같은 셀을 SOC 30%와 100%에서 ARC로 시험하면, 100% 셀은 자가 발열과 열폭주 시작 온도가 더 낮고 최고 온도가 훨씬 높다. 운송 시 셀을 낮은 SOC로 두는 이유다.

## ⚠️ 흔한 오해

소재 DSC 결과가 좋으면 셀도 안전하다고 단정하기 쉽지만, 셀에서는 크기, 열 방출, 내부 단락 방식, 전해질 양이 결과를 크게 바꾼다. 셀 수준 시험이 따로 필요하다.

## 🔗 배터리 × AI

ARC·열폭주 시험은 비싸고 위험해 데이터가 적다. 소재 조성과 셀 설계 변수로 열폭주 특성을 예측하는 모델과, 적은 데이터를 다루는 전이 학습이 연구된다.

## ❓ 퀴즈

ARC 시험이 열폭주 연구에 쓰이는 주된 이유는?

- A. 셀을 빠르게 냉각해서
- B. 단열 조건에서 최악의 자가 발열을 재현해서
- C. 전압만 측정해서
- D. 가스를 분석해서

<details><summary>정답 보기</summary>

**B** — ARC는 열이 빠져나가지 않는 단열 조건을 만들어 자가 발열이 열폭주로 이어지는 과정을 측정한다.

</details>

## 🏷 키워드

시차 주사 열량계 (differential scanning calorimetry) · 가속 속도 열량계 (accelerating rate calorimetry) · 열폭주 (thermal runaway)

## ➡️ 다음에 공부할 것

- 분리막의 역할과 셧다운 기능
- 고니켈 양극의 상전이와 산소 방출

## 📚 참고 문헌

- X. Feng et al., Thermal runaway mechanism of lithium ion battery for electric vehicles: A review, Energy Storage Materials, 2018

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Accelerating+rate+calorimetry)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Accelerating+rate+calorimetry)
- [📺 YouTube](https://www.youtube.com/results?search_query=Accelerating+rate+calorimetry)
