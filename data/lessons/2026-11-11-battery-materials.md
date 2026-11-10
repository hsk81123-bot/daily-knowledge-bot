# 흑연 음극: 리튬이 층을 건너뛰며 채워지는 스테이징

🧪 배터리 › 소재 · 2026-11-11 · 중급

> 💡 흑연은 그래핀 층 사이에 리튬을 넣어 LiC₆까지 만들 수 있고, 이 과정은 여러 단계(stage)의 상전이로 진행된다.

## 삽입 반응

흑연은 그래핀 층이 약한 반데르발스 힘으로 쌓인 구조다. 충전하면 리튬 이온이 층 사이에 들어가 탄소 6개당 리튬 1개인 LiC₆까지 만들 수 있다. 이론 용량은 약 372 mAh/g이고, 반응 전위가 리튬 금속 대비 약 0.1~0.2 V로 낮아 셀 전압을 높여 준다.

## 스테이징

리튬은 모든 층에 고르게 들어가지 않고, 일정한 간격으로 층을 건너뛰며 채워진다. n개 층마다 리튬 층이 하나 있는 상태를 stage n이라 한다. 충전이 진행되면 묽은 상태에서 stage 4, 3, 2L, 2를 거쳐 stage 1(LiC₆)로 바뀐다. 상이 바뀔 때마다 전압 곡선에 평탄 구간이 생기고, dQ/dV 그래프에는 뚜렷한 피크로 나타난다.

## 실제 사용의 쟁점

첫 충전 때 전해질이 흑연 표면에서 환원되어 SEI가 만들어지며, 이때 쓰인 리튬은 돌아오지 않는다. 또 흑연 전위가 리튬 석출 전위(0 V)에 가까워서, 급속 충전이나 저온 충전 시 리튬이 흑연 안으로 들어가지 못하고 표면에 금속으로 석출될 수 있다. 층간 간격은 리튬이 들어가면 약 10% 늘어난다.

## 🧮 핵심 수식·원리

```
6C + Li⁺ + e⁻ ⇌ LiC6
이론 용량 = 96485 / (3.6 × 72.06) ≈ 372 mAh/g (C6 기준)
```

## 🔍 예시·적용

흑연 반쪽 셀을 아주 느린 전류(예: C/20)로 충전하며 dQ/dV를 그리면 약 0.2, 0.12, 0.09 V 부근에 스테이지 전이 피크가 보인다. 이 피크 위치와 크기의 변화로 흑연의 열화를 추적할 수 있다.

## ⚠️ 흔한 오해

흑연 음극의 용량을 높이려고 무조건 리튬을 더 넣을 수 있는 것은 아니다. LiC₆가 상한이며, 그 이상은 금속 리튬 석출로 이어진다.

## 🔗 배터리 × AI

dQ/dV 피크의 위치·높이를 특징으로 뽑아 셀의 잔존 수명(RUL)을 예측하는 머신러닝 연구가 많다. 스테이징이 물리적 근거가 있는 특징을 만들어 주는 셈이다.

## ❓ 퀴즈

흑연에 리튬이 완전히 삽입된 화합물은?

- A. LiC₂
- B. LiC₆
- C. LiC₁₂
- D. Li₂C₆

<details><summary>정답 보기</summary>

**B** — 탄소 6개당 리튬 1개인 LiC₆(stage 1)가 완전 삽입 상태이며 이론 용량 약 372 mAh/g에 해당한다.

</details>

## 🏷 키워드

층간 삽입 (intercalation) · 스테이징 (staging) · 리튬 석출 (lithium plating)

## ➡️ 다음에 공부할 것

- 리튬 도금(lithium plating)
- dQ/dV 미분 용량 분석
- SEI(고체 전해질 계면)의 형성과 조성

## 📚 참고 문헌

- T. Ohzuku, Y. Iwakoshi, K. Sawai, Formation of lithium-graphite intercalation compounds in nonaqueous electrolytes, J. Electrochem. Soc., 1993

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Graphite+intercalation+compound)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Graphite+intercalation+compound)
- [📺 YouTube](https://www.youtube.com/results?search_query=Graphite+intercalation+compound)
