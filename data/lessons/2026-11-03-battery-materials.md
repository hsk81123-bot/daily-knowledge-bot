# NCM 양극재: 니켈을 늘리면 용량은 오르고 안정성은 내려간다

🧪 배터리 › 소재 · 2026-11-03 · 중급

> 💡 NCM은 LiCoO₂와 같은 층상 구조에서 코발트 자리를 Ni·Co·Mn이 나눠 맡은 양극재로, 니켈 비율이 용량과 안정성의 균형을 결정한다.

## 구조

NCM(LiNiₓCoᵧMn_zO₂, x+y+z=1)은 α-NaFeO₂형 층상 구조(R-3m)를 가진다. 산소가 입방 최밀 충전을 이루고, 그 사이 팔면체 자리에 전이금속 층과 리튬 층이 번갈아 쌓인다. 충전하면 리튬이 층 사이에서 빠져나가고, 방전하면 다시 들어간다. 이름의 숫자(NCM111, 523, 622, 811)는 Ni:Co:Mn 비율을 뜻한다.

## 원소별 역할

니켈은 주된 산화환원 활성 원소로, Ni²⁺/Ni³⁺/Ni⁴⁺ 사이를 오가며 용량을 낸다. 망간은 대체로 Mn⁴⁺로 남아 전기화학적으로는 거의 반응하지 않지만 구조를 안정시킨다. 코발트는 층상 구조의 질서를 유지해 양이온 혼합을 줄이고 전자 전도도와 율속 특성을 돕는다. 코발트는 비싸고 공급 위험이 커서 줄이려는 흐름이 강하다.

## 고니켈화의 득과 실

니켈 비율을 높이면 같은 전압 범위에서 더 많은 리튬을 꺼낼 수 있어 가역 용량이 커진다(NCM811은 대략 200 mAh/g 수준). 대신 높은 충전 상태에서 불안정한 Ni⁴⁺가 많아져 전해질과의 부반응, 상전이, 산소 방출, 입자 미세균열이 심해지고 열 안정성이 떨어진다. 또 표면에 LiOH·Li₂CO₃ 같은 잔류 리튬이 생기기 쉬워 수분 관리가 까다롭다.

## 🧮 핵심 수식·원리

```
이론 용량 Q = n·F / (3.6·M)  [mAh/g]
n: 화학식당 전자 수(=1), F = 96485 C/mol, M: 몰질량(g/mol)
예) LiNi0.8Co0.1Mn0.1O2, M ≈ 97.3 → Q ≈ 275 mAh/g (실제로 쓰는 것은 그 일부)
```

## 🔍 예시·적용

NCM622와 NCM811을 같은 상한 전압(예: 4.3 V vs Li/Li⁺)으로 충전하면 811이 더 많은 용량을 내지만, 고온 사이클에서 용량 유지율이 더 빨리 떨어지는 경향이 보인다. 그래서 고니켈 소재에는 도핑(Al, Zr 등)과 표면 코팅, 단결정화 같은 보완 기술이 함께 쓰인다.

## ⚠️ 흔한 오해

이론 용량 275 mAh/g를 모두 쓸 수 있는 것은 아니다. 리튬을 너무 많이 빼면 구조가 무너지므로 실제로는 상한 전압을 정해 일부만 쓴다. 니켈 함량이 같아도 공정·도핑·입자 형태에 따라 성능 차이가 크다.

## 🔗 배터리 × AI

조성(Ni:Co:Mn 비율), 도핑 원소, 소성 온도 같은 변수를 입력으로 용량과 수명을 예측하는 머신러닝 모델이 양극재 탐색에 많이 쓰인다. 실험 수가 적어서 가우시안 프로세스나 베이지안 최적화가 자주 쓰인다.

## ❓ 퀴즈

NCM 양극재에서 주로 산화환원 반응을 하며 용량을 내는 원소는?

- A. 망간(Mn)
- B. 니켈(Ni)
- C. 산소(O)
- D. 알루미늄(Al)

<details><summary>정답 보기</summary>

**B** — 니켈이 Ni²⁺↔Ni⁴⁺로 반응하며 용량의 대부분을 낸다. 망간은 주로 Mn⁴⁺로 남아 구조를 지탱한다.

</details>

## 🏷 키워드

층상 구조 (layered structure) · 고니켈 양극 (Ni-rich cathode) · 잔류 리튬 (residual lithium)

## ➡️ 다음에 공부할 것

- 양이온 혼합(cation mixing)
- 고니켈 양극의 상전이와 산소 방출
- 단결정 양극재와 입자 미세균열

## 📚 참고 문헌

- A. Manthiram, A reflection on lithium-ion battery cathode chemistry, Nature Communications, 2020

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Lithium+nickel+manganese+cobalt+oxide+cathode)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Lithium+nickel+manganese+cobalt+oxide+cathode)
- [📺 YouTube](https://www.youtube.com/results?search_query=Lithium+nickel+manganese+cobalt+oxide+cathode)
