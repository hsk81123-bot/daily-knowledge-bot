# GITT: 짧게 충전하고 오래 쉬며 확산을 읽는다

🔬 배터리 › 분석법 · 2026-11-14 · 중급

> 💡 GITT는 짧은 정전류 펄스와 긴 휴지를 반복하며, 펄스 중 전압 변화와 휴지 후 평형 전압 변화로 리튬 함량별 확산 계수와 OCV를 함께 얻는 방법이다.

## 측정 절차

작은 전류(예: C/20 정도)를 짧은 시간(예: 10분) 흘린 뒤, 전압이 거의 평형에 이를 때까지(예: 1시간 이상) 쉰다. 이것을 전체 SOC 범위에 걸쳐 반복한다. 각 휴지 끝 전압을 이으면 준평형 OCV 곡선이 되고, 각 펄스의 전압 응답으로 그 SOC의 확산 계수를 계산한다.

## 계산식

Weppner와 Huggins가 제시한 식은 펄스 시간이 확산 시간보다 충분히 짧고(τ ≪ L²/D), 전압이 √t에 대해 선형으로 변한다는 가정을 쓴다. 펄스 중 전압 변화 ΔE_τ(옴 강하 제외)와 휴지 전후 평형 전압 변화 ΔE_s를 넣어 D를 구한다.

## 해석상 주의

식에 들어가는 확산 길이 L(입자 크기)과 몰 부피·면적 가정에 따라 값이 크게 달라진다. 2상 반응 구간에서는 ΔE_s가 거의 0이라 식이 성립하지 않고, 확산 계수가 비정상적으로 작게 나온다. 그래서 GITT 확산 계수는 절대값보다 같은 셀 안 SOC에 따른 추세를 보는 데 더 의미가 있다.

## 🧮 핵심 수식·원리

```
D = (4 / πτ) · (m_B·V_M / M_B·S)² · (ΔE_s / ΔE_τ)²   (τ ≪ L²/D)
m_B, M_B: 활물질 질량·몰질량, V_M: 몰 부피, S: 계면 면적
```

## 🔍 예시·적용

NCM 셀의 GITT 결과에서 높은 충전 상태로 갈수록 확산 계수가 몇 배 줄어드는 경향이 보고되는데, 층간 간격이 줄어드는 구조 변화와 연결해 해석한다.

## ⚠️ 흔한 오해

GITT 확산 계수를 문헌 값과 그대로 비교하면 안 된다. 면적과 길이를 어떻게 잡았는지에 따라 같은 소재라도 한두 자릿수 차이가 날 수 있다.

## 🔗 배터리 × AI

GITT는 시간이 매우 오래 걸린다. 짧은 펄스 데이터로 전체 OCV·확산 곡선을 추정하는 신경망이나 베이지안 추정 방법이 측정 시간을 줄이는 데 연구된다.

## ❓ 퀴즈

GITT 확산 계수 식이 2상 반응 구간에서 잘 맞지 않는 이유는?

- A. 전류가 너무 커서
- B. 평형 전압 변화 ΔE_s가 거의 0이라서
- C. 옴 저항이 없어서
- D. 온도가 일정해서

<details><summary>정답 보기</summary>

**B** — 2상 공존 구간은 전압이 평탄해 ΔE_s≈0이 되고, 식의 단일상 확산 가정도 깨진다.

</details>

## 🏷 키워드

정전류 간헐 적정법 (galvanostatic intermittent titration technique) · 준평형 OCV (quasi-equilibrium OCV) · 확산 계수 (chemical diffusion coefficient)

## ➡️ 다음에 공부할 것

- Fick 확산과 고체 내 확산 계수
- OCV, 엔트로피 계수, 가역 발열

## 📚 참고 문헌

- W. Weppner, R. A. Huggins, Determination of the kinetic parameters of mixed-conducting electrodes and application to the system Li3Sb, J. Electrochem. Soc., 1977

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Galvanostatic+intermittent+titration+technique)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Galvanostatic+intermittent+titration+technique)
- [📺 YouTube](https://www.youtube.com/results?search_query=Galvanostatic+intermittent+titration+technique)
