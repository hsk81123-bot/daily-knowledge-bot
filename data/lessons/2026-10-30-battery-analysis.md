# 고체 NMR: 리튬 원자의 주변을 직접 듣는다

🔬 배터리 › 분석법 · 2026-10-30 · 심화

> 💡 고체 NMR은 ⁷Li·⁶Li·¹⁹F 같은 핵의 공명 주파수 변화로 리튬의 국소 환경과 움직임을 알려 주며, 죽은 리튬이나 SEI 성분, 확산을 정량하는 데 쓰인다.

## 원리

자기장 안에서 핵스핀은 특정 주파수(라모어 주파수)의 전파에 공명한다. 주변 전자 구조에 따라 공명 주파수가 조금씩 달라지는데(화학적 이동), 이것으로 핵의 환경을 구분한다. 고체에서는 방향에 따른 상호작용 때문에 신호가 넓어지므로, 시료를 54.7°(매직각)로 빠르게 회전시키는 MAS로 선폭을 줄인다.

## 배터리에서

⁷Li NMR에서 리튬 금속은 전도 전자에 의한 나이트 이동으로 약 260 ppm 부근에 신호가 나타나, 이온 상태 리튬(0 ppm 근처)과 쉽게 구분된다. 이를 이용해 죽은 리튬이나 도금된 리튬을 정량한다. 상자성 양극 소재는 전이금속의 홀전자 때문에 큰 이동이 생겨 해석이 어렵지만 리튬 자리 정보를 준다.

## 움직임 측정

온도에 따른 선폭 좁아짐이나 이완 시간으로 리튬의 도약 속도를 구하고, 자기장 기울기를 쓰는 PFG-NMR로 전해질 속 리튬·음이온의 자기 확산 계수를 각각 잴 수 있다. 이 값으로 전이수를 추정하기도 한다. 감도가 낮아 시료가 꽤 많이 필요하다는 것이 단점이다.

## 🧮 핵심 수식·원리

```
라모어 주파수: ω0 = γ·B0
화학적 이동: δ(ppm) = (ν − ν_ref) / ν_ref × 10⁶
```

## 🔍 예시·적용

리튬 금속 셀을 여러 사이클 돌린 뒤 operando ⁷Li NMR로 금속 리튬 신호의 크기 변화를 추적하면, 매끄러운 리튬과 이끼 모양 리튬의 비율 변화를 정량할 수 있다.

## ⚠️ 흔한 오해

NMR은 액체 분석용이라 고체 전극에는 못 쓴다고 생각하기 쉽지만, MAS와 전용 셀을 쓰면 고체 전극과 작동 중인 셀도 측정할 수 있다.

## 🔗 배터리 × AI

상자성 소재의 복잡한 NMR 스펙트럼을 DFT 계산과 비교해 해석하는데, 계산량을 줄이려고 머신러닝으로 화학적 이동을 예측하는 방법이 연구된다.

## ❓ 퀴즈

⁷Li NMR에서 금속 리튬 신호가 이온 리튬과 크게 떨어져 나타나는 원인은?

- A. 매직각 회전
- B. 전도 전자에 의한 나이트 이동
- C. XRD 회절
- D. 온도 상승

<details><summary>정답 보기</summary>

**B** — 금속 리튬의 전도 전자가 큰 나이트 이동(약 260 ppm)을 만들어 이온 리튬 신호와 구분된다.

</details>

## 🏷 키워드

고체 핵자기공명 (solid-state NMR) · 매직각 회전 (magic angle spinning) · 나이트 이동 (Knight shift)

## ➡️ 다음에 공부할 것

- 리튬 금속 음극과 덴드라이트
- 이온 전도도와 리튬 이온 전이수

## 📚 참고 문헌

- R. Bhattacharyya et al., In situ NMR observation of the formation of metallic lithium microstructures in lithium batteries, Nature Materials, 2010

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Solid-state+nuclear+magnetic+resonance)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Solid-state+nuclear+magnetic+resonance)
- [📺 YouTube](https://www.youtube.com/results?search_query=Solid-state+nuclear+magnetic+resonance)
