# GNN: 원자를 점, 결합을 선으로 보고 배운다

🧠 AI › 딥러닝 · 2026-11-26 · 심화

> 💡 그래프 신경망은 이웃 노드끼리 메시지를 주고받으며 표현을 갱신해, 원자와 결합으로 이뤄진 분자·결정 구조에서 물성을 직접 예측한다.

## 메시지 전달

각 노드(원자)는 특징 벡터(원소 종류 등)를 가진다. 한 층마다 각 노드가 이웃 노드와 연결선(결합 거리 등) 정보로 메시지를 모아 자기 표현을 갱신한다. 층을 k번 쌓으면 k단계 떨어진 원자의 정보까지 반영된다. 마지막에 모든 노드 표현을 합쳐(readout) 분자·결정 전체의 성질을 예측한다.

## 왜 그래프인가

분자와 결정은 원자 번호를 매기는 순서에 따라 결과가 바뀌면 안 된다. GNN은 이웃 정보를 합(또는 평균)으로 모아 순서 바꿈에 불변이다. 결정은 주기 경계 조건을 반영해 단위 격자 밖 이웃까지 연결선으로 잇는다(CGCNN 등). 회전·이동에 맞게 바뀌는 등변(equivariant) GNN은 힘과 같은 벡터량을 더 정확히 예측한다.

## 활용과 한계

형성 에너지, 띠 간격, 전압, 이온 전도도 예측과 기계학습 원자간 퍼텐셜에 쓰인다. 대규모 계산 데이터베이스로 학습한 범용 퍼텐셜도 나와 있다. 하지만 학습 데이터(주로 DFT)의 오차를 물려받고, 학습 범위 밖 구조에서는 신뢰도가 떨어진다. 깊게 쌓으면 노드 표현이 비슷해지는 과평활화 문제도 있다.

## 🧮 핵심 수식·원리

```
m_v = Σ_{u∈N(v)} M(h_v, h_u, e_uv)
h_v ← U(h_v, m_v),   y = R({h_v})
```

## 🔍 예시·적용

고체 전해질 후보 수만 개를 DFT로 모두 계산하는 대신, 계산된 수천 개로 GNN을 학습해 나머지의 안정성과 이동 장벽을 예측하고 유망한 후보만 정밀 계산하는 방식이 쓰인다.

## ⚠️ 흔한 오해

GNN이 물리를 이해한다고 생각하기 쉽지만, 학습 데이터의 패턴을 맞추는 것이다. 정확도는 학습 데이터와 비슷한 구조에서만 보장된다.

## 🔗 배터리 × AI

양극·고체 전해질 소재 탐색, 전해질 분자 물성 예측, 계면 시뮬레이션용 기계학습 퍼텐셜 등 배터리 소재 연구에서 GNN은 핵심 도구가 되었다.

## ❓ 퀴즈

GNN이 원자 번호 매기는 순서에 영향을 받지 않는 이유는?

- A. 원자를 항상 정렬해서
- B. 이웃 메시지를 합·평균처럼 순서 무관한 연산으로 모아서
- C. 원자 하나만 봐서
- D. CNN을 써서

<details><summary>정답 보기</summary>

**B** — 합·평균·최댓값처럼 순서와 무관한 집계를 써서 노드 순서를 바꿔도 결과가 같다(순열 불변).

</details>

## 🏷 키워드

그래프 신경망 (graph neural network) · 메시지 전달 (message passing) · 기계학습 원자간 퍼텐셜 (machine-learned interatomic potential)

## ➡️ 다음에 공부할 것

- 황화물·산화물 고체 전해질
- 능동 학습(active learning)

## 📚 참고 문헌

- T. Xie, J. C. Grossman, Crystal graph convolutional neural networks for an accurate and interpretable prediction of material properties, Phys. Rev. Lett., 2018
- J. Gilmer et al., Neural message passing for quantum chemistry, ICML, 2017

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Graph+neural+network)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Graph+neural+network)
- [📄 arXiv](https://arxiv.org/search/?query=Graph+neural+network&searchtype=all)
