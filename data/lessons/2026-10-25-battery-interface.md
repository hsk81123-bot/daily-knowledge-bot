# 전고체 계면 접촉 손실: 고체는 흘러 들어가지 않는다

🧱 배터리 › 계면 · 2026-10-25 · 심화

> 💡 전고체 전지에서는 전극 입자가 충방전 중 부피가 변해도 고체 전해질이 액체처럼 틈을 메우지 못해, 계면이 벌어지며 용량과 출력이 떨어진다.

## 액체와 고체의 차이

액체 전해질은 전극 입자가 줄어들어도 틈으로 흘러 들어가 접촉을 유지한다. 고체 전해질은 그렇지 못하다. 그래서 전고체 전지에서는 입자와 전해질 사이 고체-고체 접촉 면적이 성능을 좌우하며, 처음부터 공극 없이 밀착시키는 것 자체가 어렵다.

## 부피 변화와 균열

NCM은 충전 중 수 % 부피가 줄고, 실리콘이나 리튬 금속 음극은 크게 변한다. 이 변화가 반복되면 계면이 떨어지거나(박리) 전해질과 입자 안에 균열이 생긴다. 떨어진 입자는 리튬이나 전자를 주고받지 못해 활물질 손실이 된다. 계면 분해로 생긴 층이 다시 기계적 응력을 키우는 식으로 화학과 기계 열화가 서로를 부추긴다.

## 대응

셀에 높은 압력을 가해 접촉을 유지하는 방법이 흔히 쓰이지만, 실용 셀에서 큰 압력은 부담이다. 부피 변화가 작은 전극 소재, 무른 전해질(황화물·할라이드), 입자 크기와 혼합 비율 최적화, 유연한 고분자 첨가 등이 연구된다.

## 🧮 핵심 수식·원리

```
유효 이온 전류 ∝ 접촉 면적 A_contact
계면 저항 R_int ≈ R_specific / A_contact  → 접촉 손실 시 R_int 증가
```

## 🔍 예시·적용

같은 전고체 셀을 서로 다른 압력으로 눌러 사이클하면, 압력이 낮은 셀에서 용량이 더 빨리 줄고 EIS 계면 저항이 크게 늘어나는 결과가 흔히 보고된다.

## ⚠️ 흔한 오해

전고체 전지의 문제는 고체 전해질 전도도만 높이면 해결된다고 보기 쉽지만, 실제 셀에서는 계면 접촉과 기계적 안정성이 더 큰 병목인 경우가 많다.

## 🔗 배터리 × AI

X선 CT로 얻은 3차원 전극 구조에서 접촉 면적과 공극을 자동으로 분할·정량하는 딥러닝 이미지 분석이 전고체 전극 설계에 쓰인다.

## ❓ 퀴즈

전고체 전지에서 셀에 높은 압력을 가하는 주된 이유는?

- A. 전해질을 녹이려고
- B. 입자와 고체 전해질의 접촉을 유지하려고
- C. 리튬 도금을 일부러 일으키려고
- D. SEI를 없애려고

<details><summary>정답 보기</summary>

**B** — 고체는 틈을 메우지 못하므로 압력으로 입자와 전해질의 접촉 면적을 유지해 계면 저항을 줄인다.

</details>

## 🏷 키워드

화학-기계 열화 (chemo-mechanical degradation) · 계면 박리 (interfacial delamination) · 적층 압력 (stack pressure)

## ➡️ 다음에 공부할 것

- 황화물·산화물 고체 전해질
- 단결정 양극재와 입자 미세균열

## 📚 참고 문헌

- R. Koerver et al., Capacity fade in solid-state batteries: interphase formation and chemomechanical processes in nickel-rich layered oxide cathodes and lithium thiophosphate solid electrolytes, Chemistry of Materials, 2017

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Chemo-mechanical+degradation+solid-state+battery)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Chemo-mechanical+degradation+solid-state+battery)
- [📺 YouTube](https://www.youtube.com/results?search_query=Chemo-mechanical+degradation+solid-state+battery)
