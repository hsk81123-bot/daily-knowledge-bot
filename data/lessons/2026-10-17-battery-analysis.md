# DRT: 겹친 반원을 시간 상수별로 풀어 헤치기

🔬 배터리 › 분석법 · 2026-10-17 · 심화

> 💡 DRT 분석은 임피던스를 무수히 많은 RC 요소의 합으로 보고 각 시간 상수에 얼마나 저항이 있는지 분포로 나타내, 등가회로를 미리 정하지 않고 과정을 분리한다.

## 아이디어

EIS 반원은 과정마다 시간 상수 τ = RC를 갖는다. 실제 셀에서는 반원이 서로 겹치고 찌그러져 몇 개의 과정이 있는지조차 알기 어렵다. DRT는 임피던스를 τ의 연속 분포 g(τ)로 표현해, 분포의 피크 위치(시간 상수)와 넓이(저항)를 읽는다.

## 계산

측정 임피던스에서 g(τ)를 구하는 것은 잡음에 매우 민감한 역문제다. 그래서 티호노프 정규화(릿지 회귀) 같은 방법으로 매끄러운 해를 구한다. 정규화 강도를 너무 크게 하면 피크가 합쳐지고, 너무 작으면 가짜 피크가 생긴다. 가우시안 프로세스 같은 베이지안 방법으로 불확실성까지 구하는 접근도 있다.

## 해석

피크마다 어떤 물리 과정인지는 DRT가 알려 주지 않는다. 온도를 바꾸거나(활성화 에너지), SOC를 바꾸거나, 대칭 셀로 전극을 나누어 피크의 행동을 보고 SEI, 전하전달, 접촉 저항 등에 대응시킨다. 확산처럼 RC로 잘 표현되지 않는 과정은 분포가 넓게 퍼져 해석이 어렵다.

## 🧮 핵심 수식·원리

```
Z(ω) = R∞ + ∫ g(τ) / (1 + jωτ) d(ln τ)
정규화: min ‖Z_meas − A·g‖² + λ‖L·g‖²
```

## 🔍 예시·적용

풀셀 DRT에서 1~10 ms 부근 피크는 양극 전하전달, 더 빠른 피크는 SEI·접촉으로 해석하는 식으로 셀마다 대응 표를 만든다. 사이클에 따라 어느 피크가 커지는지로 열화 위치를 추정한다.

## ⚠️ 흔한 오해

DRT 피크 개수가 곧 물리 과정 개수라고 단정하기 쉽지만, 정규화 파라미터와 측정 잡음에 따라 피크가 생기거나 사라진다. 여러 조건에서 일관되게 나타나는 피크만 믿어야 한다.

## 🔗 배터리 × AI

DRT는 정규화가 들어간 회귀 문제이므로 머신러닝과 직접 닮았다. 정규화 강도를 교차검증으로 고르거나, 신경망으로 DRT를 바로 추정하는 연구도 있다.

## ❓ 퀴즈

DRT 계산에 정규화가 필요한 이유는?

- A. 계산이 너무 빨라서
- B. 잡음에 민감한 역문제라서
- C. 임피던스가 실수라서
- D. 등가회로를 먼저 정해야 해서

<details><summary>정답 보기</summary>

**B** — 임피던스에서 분포를 구하는 것은 불안정한 역문제여서, 정규화로 매끄럽고 안정된 해를 얻는다.

</details>

## 🏷 키워드

완화 시간 분포 (distribution of relaxation times) · 티호노프 정규화 (Tikhonov regularization) · 역문제 (inverse problem)

## ➡️ 다음에 공부할 것

- 전기화학 임피던스 분광법(EIS)과 등가회로
- L1·L2 정규화
- 가우시안 프로세스 회귀

## 📚 참고 문헌

- T. H. Wan, M. Saccoccio, C. Chen, F. Ciucci, Influence of the discretization methods on the distribution of relaxation times deconvolution, Electrochimica Acta, 2015

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Distribution+of+relaxation+times)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Distribution+of+relaxation+times)
- [📺 YouTube](https://www.youtube.com/results?search_query=Distribution+of+relaxation+times)
