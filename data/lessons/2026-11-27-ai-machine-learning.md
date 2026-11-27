# 베이지안 최적화: 비싼 실험을 적게 하며 최적점 찾기

📊 AI › 머신러닝 · 2026-11-27 · 중급

> 💡 베이지안 최적화는 지금까지의 실험 결과로 대리 모델(주로 GP)을 만들고, 기대 개선량 같은 획득 함수로 다음에 해 볼 조건을 골라, 적은 시도로 최적값을 찾는다.

## 언제 쓰나

목적 함수가 블랙박스이고 한 번 평가하는 데 비용이 크며(실험 하루, 시뮬레이션 몇 시간) 기울기를 모를 때 쓴다. 변수는 보통 수 개~20개 안팎일 때 잘 작동한다. 머신러닝 하이퍼파라미터 튜닝과 실험 조건 최적화에 널리 쓰인다.

## 반복 과정

(1) 초기 몇 점을 실험한다. (2) 결과로 대리 모델을 학습해 모든 후보 조건에서 예측 평균과 불확실성을 얻는다. (3) 획득 함수가 가장 큰 조건을 다음 실험으로 고른다. (4) 결과를 추가하고 반복한다. 획득 함수로는 기대 개선량(EI), 상한 신뢰 구간(UCB), 개선 확률(PI) 등이 있다.

## 탐색과 활용의 균형

예측이 좋은 곳만 고르면(활용) 지역 최적에 갇히고, 불확실한 곳만 고르면(탐색) 효율이 떨어진다. 획득 함수는 두 가지를 자동으로 섞는다. 여러 조건을 동시에 실험할 수 있으면 배치 베이지안 최적화를, 목표가 여러 개면 다목적 최적화(파레토 전선)를 쓴다.

## 🧮 핵심 수식·원리

```
EI(x) = E[max(f(x) − f⁺, 0)]
UCB(x) = μ(x) + κ·σ(x)   (κ: 탐색 정도)
```

## 🔍 예시·적용

급속 충전 프로토콜 224가지 후보 중 최적을 찾는 연구에서, 초기 사이클로 수명을 예측하는 모델과 베이지안 최적화를 결합해 전체를 다 시험하는 것보다 훨씬 짧은 기간에 좋은 프로토콜을 찾았다.

## ⚠️ 흔한 오해

베이지안 최적화가 전역 최적을 보장한다고 생각하기 쉽지만, 정해진 예산 안에서 효율적으로 좋은 해를 찾는 방법일 뿐이다. 변수가 매우 많으면 효율이 크게 떨어진다.

## 🔗 배터리 × AI

로봇 실험 장치와 결합한 자율 실험실(self-driving lab)에서 전해질 조성, 합성 온도, 코팅 조건을 사람 개입 없이 최적화하는 핵심 알고리즘이다.

## ❓ 퀴즈

UCB 획득 함수에서 κ를 크게 하면?

- A. 활용을 더 중시한다
- B. 탐색을 더 중시한다
- C. 대리 모델이 필요 없어진다
- D. 실험 수가 늘어난다

<details><summary>정답 보기</summary>

**B** — UCB = μ + κσ이므로 κ가 클수록 불확실성(σ)이 큰 곳을 더 선호해 탐색이 늘어난다.

</details>

## 🏷 키워드

베이지안 최적화 (Bayesian optimization) · 획득 함수 (acquisition function) · 자율 실험실 (self-driving laboratory)

## ➡️ 다음에 공부할 것

- 능동 학습(active learning)
- 하이퍼파라미터 튜닝 전략
- C-rate와 율속 특성

## 📚 참고 문헌

- P. M. Attia et al., Closed-loop optimization of fast-charging protocols for batteries with machine learning, Nature, 2020
- B. Shahriari et al., Taking the human out of the loop: a review of Bayesian optimization, Proceedings of the IEEE, 2016

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Bayesian+optimization)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Bayesian+optimization)
- [📄 arXiv](https://arxiv.org/search/?query=Bayesian+optimization&searchtype=all)
