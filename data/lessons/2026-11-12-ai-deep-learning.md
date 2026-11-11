# SGD와 Adam: 손실 지형을 내려가는 방법

🧠 AI › 딥러닝 · 2026-11-12 · 중급

> 💡 SGD는 작은 미니배치의 기울기로 가중치를 조금씩 내려가는 방법이고, Adam은 기울기의 이동 평균(모멘텀)과 크기의 이동 평균으로 파라미터마다 보폭을 자동 조절한다.

## 확률적 경사 하강법

전체 데이터의 기울기 대신 무작위 미니배치(예: 32~512개)의 기울기로 갱신한다. 계산이 싸고, 기울기의 잡음이 날카로운 극소점을 벗어나게 도와 일반화에 유리할 수 있다. 모멘텀은 이전 갱신 방향을 일부 이어 가 골짜기에서 진동을 줄이고 평평한 방향으로 빨리 나아가게 한다.

## Adam

Adam은 기울기의 1차 모멘트(평균)와 2차 모멘트(제곱 평균)를 지수 이동 평균으로 추적하고, 1차 모멘트를 2차 모멘트의 제곱근으로 나눠 갱신한다. 기울기가 자주 큰 파라미터는 보폭이 줄고, 드물게 작은 파라미터는 보폭이 커진다. 기본값으로도 잘 작동해 가장 널리 쓰인다. 가중치 감쇠를 분리한 AdamW가 사실상 표준이다.

## 학습률 일정

어떤 최적화기든 학습률이 가장 중요한 하이퍼파라미터다. 처음 몇 단계는 학습률을 서서히 올리는 워밍업, 이후 코사인이나 선형으로 줄이는 감소 일정을 흔히 쓴다. 학습률이 너무 크면 손실이 발산하고, 너무 작으면 학습이 매우 느리다.

## 🧮 핵심 수식·원리

```
SGD+모멘텀: v ← βv + g,  w ← w − ηv
Adam: m ← β1·m + (1−β1)g,  s ← β2·s + (1−β2)g²
      w ← w − η · m̂ / (√ŝ + ε)   (m̂, ŝ: 편향 보정)
```

## 🔍 예시·적용

작은 배터리 데이터셋으로 신경망을 학습할 때 AdamW(학습률 1e-3, 가중치 감쇠 1e-4)와 코사인 감소 일정으로 시작하고, 검증 손실을 보며 학습률부터 조정하는 것이 일반적인 출발점이다.

## ⚠️ 흔한 오해

Adam이 항상 SGD보다 낫다고 생각하기 쉽지만, 이미지 분류 등 일부 분야에서는 잘 튜닝한 SGD+모멘텀이 더 좋은 일반화를 보이기도 한다.

## 🔗 배터리 × AI

전기화학 모델 파라미터를 측정 데이터에 맞추는 문제도 미분 가능하게 만들면 Adam으로 최적화할 수 있다. 다만 파라미터 크기가 몇 자릿수씩 달라 로그 변환이 중요하다.

## ❓ 퀴즈

AdamW가 Adam과 다른 점은?

- A. 모멘텀을 쓰지 않는다
- B. 가중치 감쇠를 기울기 갱신과 분리해 적용한다
- C. 학습률이 없다
- D. 2차 모멘트를 쓰지 않는다

<details><summary>정답 보기</summary>

**B** — AdamW는 가중치 감쇠를 적응형 보폭과 섞지 않고 따로 적용해 정규화 효과를 의도대로 낸다.

</details>

## 🏷 키워드

확률적 경사 하강법 (stochastic gradient descent) · 모멘텀 (momentum) · 학습률 일정 (learning rate schedule)

## ➡️ 다음에 공부할 것

- 배치 정규화와 레이어 정규화
- 하이퍼파라미터 튜닝 전략

## 📚 참고 문헌

- D. P. Kingma, J. Ba, Adam: A method for stochastic optimization, ICLR, 2015
- I. Loshchilov, F. Hutter, Decoupled weight decay regularization, ICLR, 2019

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Stochastic+gradient+descent)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Stochastic+gradient+descent)
- [📄 arXiv](https://arxiv.org/search/?query=Stochastic+gradient+descent&searchtype=all)
