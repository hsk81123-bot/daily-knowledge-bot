# TBox와 ABox: 개념의 규칙과 실제 데이터를 나눈다

🕸️ AI › 온톨로지 · 2026-11-10 · 입문

> 💡 온톨로지 지식은 개념과 그 관계의 일반 규칙(TBox)과, 특정 개체에 대한 사실(ABox)로 나뉘며, 이 구분이 설계와 재사용의 기본 틀이 된다.

## 클래스·속성·개체

클래스는 같은 성질을 가진 것들의 집합(예: 양극)이다. 개체(인스턴스)는 그 집합의 구체적인 원소(예: 셀 A의 양극)다. 속성은 둘 사이의 관계다. 개체와 개체를 잇는 객체 속성(hasCathode)과 개체와 값(숫자, 문자열)을 잇는 데이터 속성(hasThickness)으로 나뉜다.

## TBox

용어 상자(Terminological Box)는 '양극은 전극이다', '셀은 정확히 하나의 양극을 가진다'처럼 개념 수준의 규칙을 담는다. 분야 전문가들이 합의해 천천히 바뀌며, 여러 프로젝트가 공유해 재사용한다.

## ABox

단언 상자(Assertional Box)는 '셀A는 양극P1을 가진다', '양극P1의 두께는 60 μm다'처럼 특정 개체에 대한 사실이다. 실험마다 계속 늘어나는 실제 데이터다. TBox와 ABox를 분리하면 같은 온톨로지로 여러 연구실의 데이터를 담을 수 있고, 추론기는 TBox 규칙을 ABox에 적용해 새 사실을 끌어낸다.

## 🧮 핵심 수식·원리

```
TBox: Cathode ⊑ Electrode,  Cell ⊑ (=1 hasCathode.Cathode)
ABox: Cell(cellA),  hasCathode(cellA, p1),  hasThickness(p1, 60)
```

## 🔍 예시·적용

온톨로지 파일(TBox)은 공용 저장소에서 버전 관리하고, 각 연구실의 시험 데이터(ABox)는 그 TBox를 불러와 자기 데이터베이스에 쌓는 방식이 흔하다.

## ⚠️ 흔한 오해

무엇을 클래스로, 무엇을 개체로 둘지가 항상 분명하다고 생각하기 쉽지만, 'NCM811'은 소재 종류(클래스)로도, 특정 제품 로트(개체)로도 볼 수 있다. 용도에 따라 정해야 한다.

## 🔗 배터리 × AI

배터리 데이터 관리에서는 BattINFO 같은 공용 TBox를 쓰고, 셀·측정 데이터는 ABox로 만들어 지식 그래프에 쌓는 구조가 권장된다.

## ❓ 퀴즈

'셀A의 공칭 용량은 3.0 Ah다'는 어디에 속하나?

- A. TBox
- B. ABox
- C. 토크나이저
- D. SHACL 형태

<details><summary>정답 보기</summary>

**B** — 특정 개체(셀A)에 대한 구체적 사실이므로 단언 상자(ABox)에 속한다.

</details>

## 🏷 키워드

용어 상자 (TBox) · 단언 상자 (ABox) · 객체 속성 (object property)

## ➡️ 다음에 공부할 것

- 기술 논리(description logic)
- RDFS와 OWL

## 📚 참고 문헌

- F. Baader et al., The Description Logic Handbook, 2nd ed., Cambridge University Press, 2007

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=Abox)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=Abox)
- [📄 arXiv](https://arxiv.org/search/?query=Abox&searchtype=all)
