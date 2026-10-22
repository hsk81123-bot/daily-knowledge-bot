# LFP: 에너지 밀도 대신 안전성과 수명을 택한 양극재

🧪 배터리 › 소재 · 2026-10-23 · 입문

> 💡 LiFePO₄는 강한 P–O 결합 덕분에 열에 강하고 수명이 길지만, 전압과 전도도가 낮아 나노화와 탄소 코팅으로 단점을 메운다.

## 구조

LFP는 올리빈 구조(사방정계, Pnma)를 가진다. FeO₆ 팔면체와 PO₄ 사면체가 골격을 이루고, 리튬은 b축 방향의 1차원 통로를 따라 움직인다. 인산 음이온(PO₄³⁻)의 P–O 공유 결합이 매우 강해 충전 상태에서도 산소를 잘 내놓지 않는다.

## 2상 반응과 평탄한 전압

충방전은 LiFePO₄와 FePO₄ 두 상 사이의 2상 반응으로 진행된다. 두 상이 공존하는 동안 깁스 상률에 따라 전압이 거의 일정해서, 약 3.4 V(vs Li/Li⁺)의 매우 평탄한 전압 곡선이 나타난다. 이 덕분에 출력이 안정적이지만, 전압만 보고 충전 상태(SOC)를 추정하기는 어렵다.

## 약점과 해결

LFP는 전자 전도도와 리튬 확산이 느리다. 그래서 입자를 수십~수백 nm로 작게 만들고 표면을 탄소로 얇게 감싸 전도 경로를 만든다. 이론 용량은 약 170 mAh/g이고 평균 전압이 낮아 NCM보다 에너지 밀도가 낮지만, 철과 인은 싸고 풍부하며 수명이 길어 ESS와 보급형 전기차에 널리 쓰인다.

## 🧮 핵심 수식·원리

```
LiFePO4 ⇌ FePO4 + Li⁺ + e⁻   (Fe²⁺ ⇌ Fe³⁺)
이론 용량 ≈ 96485 / (3.6 × 157.8) ≈ 170 mAh/g
```

## 🔍 예시·적용

LFP 셀의 OCV 곡선은 SOC 20~80% 구간에서 수십 mV밖에 변하지 않는다. 그래서 BMS는 전압 대신 전류 적산(쿨롱 카운팅)과 완충 시점 보정에 더 많이 의존한다.

## ⚠️ 흔한 오해

LFP가 원래 전도도가 좋은 소재라서 많이 쓰이는 것은 아니다. 나노화와 탄소 코팅 같은 공정 기술이 나온 뒤에야 실용화되었다.

## 🔗 배터리 × AI

평탄한 전압 때문에 SOC 추정이 어려운 LFP는 전류·전압·온도 이력을 입력으로 SOC를 추정하는 칼만 필터나 LSTM 같은 시계열 모델이 특히 많이 연구되는 대상이다.

## ❓ 퀴즈

LFP 전압 곡선이 넓은 SOC 범위에서 평탄한 주된 이유는?

- A. 전해질 저항이 매우 작아서
- B. LiFePO₄와 FePO₄의 2상 반응이라서
- C. 철이 전자를 2개씩 내놓아서
- D. 탄소 코팅 때문에

<details><summary>정답 보기</summary>

**B** — 두 상이 공존하면 상률에 따라 리튬 화학 퍼텐셜이 고정되어 전압이 거의 일정하게 유지된다.

</details>

## 🏷 키워드

올리빈 구조 (olivine structure) · 2상 반응 (two-phase reaction) · 탄소 코팅 (carbon coating)

## ➡️ 다음에 공부할 것

- 상전이 반응 vs 고용체 반응의 전압 곡선
- OCV, 엔트로피 계수, 가역 발열

## 📚 참고 문헌

- A. K. Padhi, K. S. Nanjundaswamy, J. B. Goodenough, Phospho-olivines as positive-electrode materials for rechargeable lithium batteries, J. Electrochem. Soc., 1997

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Lithium+iron+phosphate)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Lithium+iron+phosphate)
- [📺 YouTube](https://www.youtube.com/results?search_query=Lithium+iron+phosphate)
