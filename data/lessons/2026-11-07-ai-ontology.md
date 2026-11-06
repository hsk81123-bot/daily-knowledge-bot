# SPARQL: 그래프 모양을 그려서 묻는 질의 언어

🕸️ AI › 온톨로지 · 2026-11-07 · 중급

> 💡 SPARQL은 RDF 그래프에 대한 표준 질의 언어로, 변수가 들어간 트리플 패턴을 적으면 그 모양과 일치하는 부분 그래프를 모두 찾아 돌려준다.

## 기본 형태

SELECT 절에 원하는 변수를, WHERE 절에 트리플 패턴을 쓴다. 예를 들어 '?cell ex:hasCathode ?cathode . ?cathode a ex:NCM811 .'은 NCM811 양극을 가진 모든 셀을 찾는다. 여러 패턴은 공통 변수로 연결되어 그래프 위의 경로를 표현한다.

## 자주 쓰는 기능

FILTER로 조건(온도 > 40)을 걸고, OPTIONAL로 없을 수도 있는 정보를 함께 가져오며, GROUP BY와 집계 함수(AVG, COUNT)로 요약한다. 속성 경로(ex:partOf+)로 여러 단계 관계를 한 번에 따라가고, SERVICE로 다른 엔드포인트의 데이터를 함께 묻는 연합 질의도 할 수 있다.

## SQL과의 차이

SQL은 미리 정한 표 구조를 조인하지만, SPARQL은 스키마가 유연한 그래프에서 관계를 따라간다. 새로운 종류의 관계를 추가해도 기존 질의가 깨지지 않는다. 추론을 켠 저장소에서는 하위 클래스 관계까지 반영된 결과가 나온다. 대신 대용량에서 성능 튜닝이 SQL보다 까다로울 수 있다.

## 🧮 핵심 수식·원리

```
SELECT ?cell (AVG(?life) AS ?avgLife) WHERE {
  ?cell ex:hasCathode/a ex:NCM811 ;
        ex:testTemperature ?T ; ex:cycleLife ?life .
  FILTER(?T >= 45)
} GROUP BY ?cell
```

## 🔍 예시·적용

위키데이터 SPARQL 엔드포인트에서 '리튬을 포함하는 화합물 중 녹는점이 기록된 것'을 묻는 질의를 써 보면 SPARQL 문법을 빠르게 익힐 수 있다.

## ⚠️ 흔한 오해

SPARQL을 쓰면 데이터가 자동으로 정리된다고 생각하기 쉽지만, 같은 의미를 다른 URI로 기록한 데이터는 찾지 못한다. 온톨로지와 URI 관리가 먼저다.

## 🔗 배터리 × AI

셀 제조·시험 지식 그래프에 SPARQL을 쓰면 '특정 첨가제를 쓴 셀들의 45 °C 수명 분포' 같은 질문으로 머신러닝 학습 데이터를 바로 뽑을 수 있다. LLM이 자연어를 SPARQL로 바꾸는 연구도 활발하다.

## ❓ 퀴즈

SPARQL에서 없을 수도 있는 정보를 함께 가져올 때 쓰는 키워드는?

- A. FILTER
- B. OPTIONAL
- C. DELETE
- D. LIMIT

<details><summary>정답 보기</summary>

**B** — OPTIONAL 패턴은 일치하면 값을 붙이고, 없어도 결과 행을 버리지 않는다(SQL의 LEFT JOIN과 비슷).

</details>

## 🏷 키워드

SPARQL · 트리플 패턴 (triple pattern) · 속성 경로 (property path)

## ➡️ 다음에 공부할 것

- 지식 그래프
- LLM과 지식 그래프의 결합(GraphRAG)

## 📚 참고 문헌

- W3C, SPARQL 1.1 Query Language, W3C Recommendation, 2013

## 🔗 더 읽어보기

- [📖 위키백과](https://en.wikipedia.org/w/index.php?search=SPARQL)
- [🎓 Google Scholar](https://scholar.google.com/scholar?q=SPARQL)
- [📄 arXiv](https://arxiv.org/search/?query=SPARQL&searchtype=all)
