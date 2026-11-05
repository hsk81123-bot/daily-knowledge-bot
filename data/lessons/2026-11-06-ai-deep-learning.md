# 활성화 함수: 신경망에 곡선을 넣는 장치

🧠 AI › 딥러닝 · 2026-11-06 · 입문

> 💡 활성화 함수는 층마다 출력에 비선형성을 더해 신경망이 복잡한 함수를 표현하게 하며, 기울기가 잘 흐르는지에 따라 학습 속도와 안정성이 크게 달라진다.

## 왜 필요한가

선형 층을 여러 개 쌓아도 결과는 하나의 선형 변환이다. 층 사이에 비선형 함수를 넣어야 깊이가 의미를 갖고, 충분히 넓은 망이 임의의 연속 함수를 근사할 수 있게 된다(보편 근사 정리).

## 시그모이드에서 ReLU로

시그모이드와 tanh는 입력이 크거나 작으면 기울기가 0에 가까워져 깊은 망에서 기울기 소실을 일으킨다. ReLU(max(0, x))는 양수 구간에서 기울기가 1이라 기울기가 잘 흐르고 계산이 매우 싸서 딥러닝 확산에 크게 기여했다. 단점은 음수 입력에서 기울기가 0이라 일부 뉴런이 영영 꺼지는 '죽은 ReLU' 문제다.

## 최근의 선택

Leaky ReLU는 음수 쪽에 작은 기울기를 둔다. GELU는 입력에 '그 값이 양수일 확률'을 곱한 부드러운 함수로 트랜스포머에서 표준처럼 쓰인다. SiLU(Swish)와 이를 게이트 구조로 쓴 SwiGLU는 최근 LLM에서 많이 쓰인다. 출력층에서는 회귀는 선형, 다중 분류는 소프트맥스를 쓴다.

## 🧮 핵심 수식·원리

```
ReLU(x) = max(0, x)
GELU(x) = x · Φ(x)   (Φ: 표준정규 누적분포)
SiLU(x) = x · σ(x)
```

## 🔍 예시·적용

배터리 수명 회귀 모델에서 마지막 층에 ReLU를 쓰면 출력이 음수가 될 수 없지만 0 근처에서 기울기가 막힐 수 있다. 보통 마지막 층은 선형으로 두고 필요하면 로그 변환한 목표를 쓴다.

## ⚠️ 흔한 오해

더 복잡한 활성화 함수가 항상 더 좋은 것은 아니다. 대부분의 문제에서 ReLU·GELU 계열의 차이는 크지 않고, 초기화와 정규화, 학습률이 더 중요하다.

## 🔗 배터리 × AI

PINN처럼 출력의 2차 미분이 필요한 모델에서는 ReLU의 2차 미분이 0이라 문제가 생긴다. 그래서 tanh나 SiLU처럼 매끄러운 활성화를 쓴다.

## ❓ 퀴즈

ReLU가 시그모이드보다 깊은 망 학습에 유리한 주된 이유는?

- A. 출력이 항상 0~1이라서
- B. 양수 구간 기울기가 1이라 기울기 소실이 적어서
- C. 모든 입력에서 기울기가 0이라서
- D. 계산이 더 복잡해서

<details><summary>정답 보기</summary>

**B** — 시그모이드는 포화 구간에서 기울기가 0에 가깝지만 ReLU는 양수 구간에서 기울기 1을 유지한다.

</details>

## 🏷 키워드

활성화 함수 (activation function) · 죽은 ReLU (dying ReLU) · 보편 근사 정리 (universal approximation theorem)

## ➡️ 다음에 공부할 것

- 역전파와 연쇄 법칙
- 물리 정보 신경망(PINN)

## 📚 참고 문헌

- D. Hendrycks, K. Gimpel, Gaussian error linear units (GELUs), arXiv:1606.08415, 2016

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Activation+function)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Activation+function)
- [📄 arXiv](https://arxiv.org/search/?query=Activation+function&searchtype=all)
