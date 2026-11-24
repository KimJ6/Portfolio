---
id: rendering-research
title: 대규모 인스턴스 렌더링 성능 분석
subtitle: 렌더링 경로 구현 및 성능 비교
category:
- 실시간 렌더링
- 성능 분석
- 연구
project_type: collaborative
status: unknown
role:
- ECS 시뮬레이션 구현
- 렌더링 경로 구현
- 성능 계측 및 분석
- 제1저자 논문 작성
technologies:
- Unity
- Unity ECS
- Job System
- Graphics.RenderMeshIndirect
- BatchRendererGroup
- 셰이더
summary:
  overview: Unity ECS 기반 대규모 3D 인스턴스 환경에서 렌더링 경로와 명령 제출 방식에 따른 실행 특성을 비교한 공동 연구입니다.
  problem: 대규모 객체의 성능을 이해하기 위해 시뮬레이션과 실제 렌더링 명령 제출 구조를 함께 다룰 필요가 있다고 판단했습니다.
  contribution: 공통 ECS 시뮬레이션과 두 렌더링 경로를 구현하고, 통합 및 4분할 제출 조건에서 실행 지표를 계측하고 분석했습니다.
  result: 비교 결과를 제1저자 논문으로 정리하여 멀티미디어학회논문지에 게재했습니다(2026년 8월, 29권 8호).
  resume: 공통 ECS 시뮬레이션 및 두 렌더링 경로 구현, 성능 비교 실험과 분석을 수행하고 제1저자 논문을 게재했습니다.
featured: true
order: 1
cover: experiment
media:
- id: experiment
  src: assets/research-experiment.png
  alt: 다수의 3D 인스턴스를 배치한 Unity ECS 렌더링 실험 장면
  caption: 렌더링 경로 비교 실험 환경
  kind: screenshot
links:
- kind: repository
  label: 렌더링 연구 소스 코드
  url: https://github.com/pnucse-capstone2026/capstone-2026-team-15
- kind: paper
  label: 게재 논문 및 초록 (KCI)
  url: https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART003380515
updated_at: '2026-11-24'
publication:
  title: Unity ECS 대규모 인스턴스 렌더링의 간접 드로우와 엔진 관리 배치 제출 성능 비교
  journal: 멀티미디어학회논문지
  publisher: 한국멀티미디어학회
  year: 2026
  volume: 29
  issue: 8
  pages: 1220-1233
  author_role: 제1저자
  month: 8
  doi: 10.9717/kmms.2026.29.8.1220
---

## 문제 정의

대규모 객체의 성능을 이해하려면 시뮬레이션뿐 아니라 렌더링 명령이 실제로 제출되는 구조까지 직접 다뤄야 한다고 판단했습니다. Unity ECS 기반 3D 인스턴스 환경에서 렌더링 경로와 제출 방식에 따른 실행 특성을 비교했습니다.

## 역할 및 기여

공동 연구에서 ECS 시뮬레이션과 두 렌더링 경로의 구현, 실행 지표 계측 및 분석을 담당했습니다. 연구 결과를 제1저자 논문으로 정리했습니다.

## 설계 및 구현

### Unity ECS 기반 시뮬레이션 구현

Unity ECS의 엔티티, 컴포넌트, 시스템을 이용해 다수 유닛의 이동과 상태 갱신을 구현했습니다. Job System으로 시뮬레이션을 병렬 처리하고 두 렌더링 경로가 동일한 ECS 상태를 사용하도록 구성했습니다.

### 렌더링 경로 구현

Graphics.RenderMeshIndirect(RMI)를 이용한 간접 드로우 경로와 BatchRendererGroup(BRG) 기반 엔진 관리 배치 제출 경로를 각각 구현했습니다. 각 경로에 맞는 인스턴스 버퍼, 셰이더, 명령 제출 구성을 직접 다루고 통합 및 4분할 제출 조건을 구성했습니다.

### 렌더링 경로 비교와 성능 분석

동일한 ECS 시뮬레이션에서 렌더링 경로와 명령 제출 방식을 조합한 2×2 요인 설계로 비교했습니다. 프레임 시간, FPS, 1% Low FPS, 메인 스레드 시간, 렌더 스레드 시간, GPU 시간 및 드로우 콜 구조를 분석했습니다.

실험에서는 렌더링 자원, 애니메이션 로직, 카메라, 그래픽 설정을 동일하게 유지했으며 컬링과 LOD를 비활성화했습니다. 인스턴스 2,000~16,000개와 군집 4~16개를 대상으로 워밍업 이후 60초씩 5회 측정했습니다.

## 결과 및 검증

논문 초록에 보고된 주요 비교 결과는 다음과 같습니다.

| 비교 조건 | 측정 결과 |
| --- | --- |
| 군집 16개, 인스턴스 2,000~16,000개, 통합 제출 | BRG 평균 프레임 시간이 RMI보다 6.3~8.5% 높음 |
| 군집 16개, 인스턴스 2,000~16,000개, 통합 제출 | BRG의 샘플링된 메인 스레드 및 GPU 시간이 더 높았으며 렌더 스레드 시간은 거의 일정하게 유지됨 |
| 위와 같은 작업 부하에서 통합 및 4분할 제출 비교 | 평균 프레임 시간 차이 0.5% 미만 |

시뮬레이션이 주요 부하를 차지하는 조건에서는 렌더링 경로에 따른 차이가 대부분 가려졌습니다. 반면 중간 부하 조건에서는 BRG의 메인 스레드 비용 증가와 프레임 안정성 저하가 관찰되었습니다. 따라서 이 결과는 특정 실험 환경에서의 실행 특성 비교이며, 모든 환경에서 한 렌더링 경로가 우월하다는 의미는 아닙니다.

연구 결과를 제1저자 논문으로 멀티미디어학회논문지에 게재했습니다.
