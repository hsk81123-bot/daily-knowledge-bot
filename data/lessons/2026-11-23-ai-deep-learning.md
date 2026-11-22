# 정규화 층: 층마다 입력의 크기를 맞춰 학습을 안정시킨다

🧠 AI › 딥러닝 · 2026-11-23 · 중급

> 💡 배치 정규화는 미니배치 안에서 특징별로, 레이어 정규화는 표본 하나 안에서 모든 특징에 걸쳐 평균과 분산을 맞춰, 깊은 망을 더 큰 학습률로 안정적으로 학습하게 한다.

## 배치 정규화

각 특징(채널)마다 미니배치의 평균과 분산으로 값을 표준화한 뒤, 학습 가능한 크기(γ)와 이동(β)을 곱하고 더한다. 학습이 빨라지고 초기화에 덜 민감해져 CNN에서 표준이 되었다. 추론 때는 학습 중 모아 둔 이동 평균 통계를 쓴다. 배치가 작으면 통계가 불안정해 성능이 떨어진다.

## 레이어 정규화

표본 하나의 모든 특징에 대해 평균과 분산을 구해 표준화한다. 배치 크기와 무관하고 학습과 추론이 같은 계산이라 RNN과 트랜스포머에서 표준이다. 최근 LLM은 평균 빼기를 생략하고 크기만 맞추는 RMSNorm을 많이 쓴다.

## 왜 효과가 있나

처음에는 앞 층이 바뀌면서 뒤 층 입력 분포가 계속 변하는 문제(내부 공변량 변화)를 줄인다고 설명되었다. 이후 연구는 손실 지형을 더 매끄럽게 만들어 기울기가 안정되는 효과가 더 중요하다고 본다. 트랜스포머에서는 정규화를 잔차 연결 앞에 두는 Pre-LN 방식이 깊은 망 학습을 더 안정시킨다.

## 🧮 핵심 수식·원리

```
x̂ = (x − μ) / √(σ² + ε),  y = γ·x̂ + β
BatchNorm: μ, σ를 배치 축으로 / LayerNorm: 특징 축으로
RMSNorm: y = γ · x / √(mean(x²) + ε)
```

## 🔍 예시·적용

배치 크기를 2~4로밖에 못 쓰는 큰 3D 전극 이미지 분할 모델에서는 배치 정규화보다 그룹 정규화나 레이어 정규화를 쓰는 것이 안정적이다.

## ⚠️ 흔한 오해

정규화 층이 드롭아웃 같은 정규화(regularization)와 같은 뜻이라고 오해하기 쉽다. 이름이 비슷하지만 정규화 층(normalization)은 값의 크기를 맞추는 것이고, 과적합 방지는 부수 효과다.

## 🔗 배터리 × AI

배터리 시계열 모델에서 셀마다 측정 범위가 다르면 입력 표준화와 레이어 정규화가 함께 필요하다. 특히 셀 사이 편차가 큰 데이터에서 학습 안정성에 영향을 준다.

## ❓ 퀴즈

트랜스포머에서 배치 정규화 대신 레이어 정규화를 주로 쓰는 이유는?

- A. 배치 크기와 시퀀스 길이에 무관하게 동작해서
- B. 파라미터가 없어서
- C. 출력이 항상 양수라서
- D. 합성곱에만 쓸 수 있어서

<details><summary>정답 보기</summary>

**A** — 레이어 정규화는 표본 하나 안에서 계산해 배치 크기·가변 길이 시퀀스와 무관하고 학습·추론이 같다.

</details>

## 🏷 키워드

배치 정규화 (batch normalization) · 레이어 정규화 (layer normalization) · RMS 정규화 (RMSNorm)

## ➡️ 다음에 공부할 것

- 트랜스포머 구조
- 잔차 연결(ResNet)

## 📚 참고 문헌

- S. Ioffe, C. Szegedy, Batch normalization: accelerating deep network training by reducing internal covariate shift, ICML, 2015
- J. L. Ba, J. R. Kiros, G. E. Hinton, Layer normalization, arXiv:1607.06450, 2016

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Batch+normalization)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Batch+normalization)
- [📄 arXiv](https://arxiv.org/search/?query=Batch+normalization&searchtype=all)
