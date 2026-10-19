# 오토인코더와 VAE: 압축했다가 다시 펼치며 데이터의 핵심을 배운다

🧠 AI › 딥러닝 · 2026-10-20 · 중급

> 💡 오토인코더는 입력을 작은 잠재 벡터로 압축했다가 복원하도록 학습해 데이터의 핵심 구조를 배우고, VAE는 잠재 공간을 확률 분포로 만들어 새 데이터를 생성할 수 있게 한다.

## 오토인코더

인코더가 입력 x를 저차원 잠재 벡터 z로 줄이고, 디코더가 z에서 x를 복원한다. 복원 오차를 줄이도록 학습하면 z에는 데이터의 중요한 변화만 남는다. 선형 오토인코더는 PCA와 같은 공간을 배우고, 비선형 오토인코더는 곡선 구조까지 잡는다. 정상 데이터로만 학습하면 이상 데이터는 복원 오차가 커서 이상 탐지에 쓸 수 있다.

## VAE

변분 오토인코더(VAE)는 인코더가 z 하나가 아니라 평균과 분산(분포)을 낸다. 학습 손실은 복원 오차에 더해, 이 분포가 표준정규분포에서 너무 멀어지지 않게 하는 KL 발산 항을 가진다. 그 결과 잠재 공간이 연속적이고 매끄러워져, 표준정규분포에서 z를 뽑아 디코더에 넣으면 새로운 그럴듯한 데이터가 나온다.

## 재매개변수화

분포에서 무작위로 뽑는 과정은 그대로는 미분할 수 없다. z = μ + σ·ε(ε는 표준정규 잡음)로 바꿔 쓰면 무작위성은 ε에 있고 μ, σ로는 기울기가 흐른다. 이것이 재매개변수화 기법이다. VAE의 생성 결과는 흐릿해지기 쉬워, 이미지 생성에서는 확산 모델 등에 많이 자리를 내주었다.

## 🧮 핵심 수식·원리

```
VAE 손실: L = E_q[−log p(x|z)] + KL(q(z|x) ‖ N(0, I))
재매개변수화: z = μ + σ ⊙ ε,  ε ~ N(0, I)
```

## 🔍 예시·적용

분자 SMILES나 그래프를 VAE로 연속 잠재 공간에 넣은 뒤, 그 공간에서 물성 예측 모델과 베이지안 최적화로 좋은 지점을 찾아 디코딩하면 새로운 분자 후보를 생성할 수 있다.

## ⚠️ 흔한 오해

오토인코더의 잠재 차원 하나하나가 해석 가능한 물리 변수에 대응한다고 기대하기 쉽지만, 보통은 여러 요인이 섞여 있다. 해석 가능한 표현을 얻으려면 추가 제약이 필요하다.

## 🔗 배터리 × AI

정상 셀의 충방전 곡선으로 오토인코더를 학습해 복원 오차로 이상 셀을 찾거나, 전해질 분자 생성에 VAE를 쓰는 연구가 있다.

## ❓ 퀴즈

VAE 손실의 KL 발산 항이 하는 역할은?

- A. 복원 오차를 키운다
- B. 잠재 분포를 표준정규분포에 가깝게 해 매끄러운 잠재 공간을 만든다
- C. 학습률을 정한다
- D. 데이터를 늘린다

<details><summary>정답 보기</summary>

**B** — KL 항이 잠재 분포를 N(0, I) 쪽으로 당겨, 잠재 공간에서 샘플링해 새 데이터를 생성할 수 있게 한다.

</details>

## 🏷 키워드

오토인코더 (autoencoder) · 변분 오토인코더 (variational autoencoder) · 잠재 공간 (latent space)

## ➡️ 다음에 공부할 것

- 확산 모델
- 주성분 분석(PCA)
- 불균형 데이터 다루기

## 📚 참고 문헌

- D. P. Kingma, M. Welling, Auto-encoding variational Bayes, ICLR, 2014
- R. Gómez-Bombarelli et al., Automatic chemical design using a data-driven continuous representation of molecules, ACS Central Science, 2018

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Variational+autoencoder)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Variational+autoencoder)
- [📄 arXiv](https://arxiv.org/search/?query=Variational+autoencoder&searchtype=all)
