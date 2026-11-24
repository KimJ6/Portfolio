---
id: precision-tick
title: PrecisionTick Metronome
subtitle: 모바일 사용 환경 및 정밀 타이밍 구현
category:
- 웹 애플리케이션
- 시간 제어
project_type: individual
status: unknown
role:
- 모바일 UI 설계 및 구현
- 오디오 시간 처리 구조 설계 및 구현
technologies:
- Web Audio API
- AudioWorklet
summary:
  overview: 데스크톱과 모바일 브라우저에서 사용하는 메트로놈 앱입니다.
  problem: 모바일 연습 도구의 조작 편의성과 박자의 안정성을 함께 고려해야 한다고 판단했습니다.
  contribution: 반응형 UI와 화면 유지 기능을 구현하고, 샘플 단위 박자 생성, 설정 적용 시점 제어, 오차 보정 및 계측 기능을 구현했습니다.
  result: 모바일 사용 환경과 샘플 단위 시간 처리를 고려한 브라우저 앱을 구현했습니다.
  resume: AudioWorklet 기반 박자 생성, 설정 적용 시점 제어, 잔차 보정 및 계측과 모바일 UI를 구현했습니다.
featured: true
order: 5
cover: ui
media:
- id: ui
  src: assets/metronome-ui.png
  alt: PrecisionTick 메트로놈의 데스크톱 및 모바일 조작 UI
  caption: 데스크톱 및 모바일 화면의 조작 구성
  kind: screenshot
links:
- kind: demo
  label: PrecisionTick 웹 앱
  url: https://precisiontick-metronome.vercel.app/
- kind: repository
  label: PrecisionTick 소스 코드
  url: https://github.com/KimJ6/precision-metronome
updated_at: '2026-11-24'
implementation_techniques:
- 반응형 UI
---

## 문제 정의

모바일 연습 도구에서 사용자가 체감하는 조작 편의성과 박자의 안정성을 함께 확보하려면 화면 구성뿐 아니라 오디오의 시간 처리 방식까지 고려해야 한다고 판단했습니다.

## 역할 및 기여

개인 프로젝트로 모바일 UI와 오디오 시간 처리 구조를 설계하고 구현했습니다.

## 설계 및 구현

### 모바일 사용 환경

작은 화면에서도 주요 설정을 조작할 수 있도록 반응형 UI를 구성했습니다. 터치 재생 및 정지와 화면 켜짐 유지를 지원하여 모바일 사용 환경을 고려했습니다.

### 샘플 단위 박자 생성

UI 실행 주기와 오디오 처리를 분리하고 AudioWorklet의 샘플 카운터를 기준으로 박자를 생성했습니다.

### 설정 변경 시점 제어

사용 중에도 박자와 설정 상태가 일관되게 유지되도록 재생 중 변경된 BPM, 박자표, 볼륨, 강박 설정을 보류 상태로 유지하고 다음 마디의 첫 박에서 함께 적용하도록 구현했습니다.

### 오차 보정 및 계측

비정수 샘플 간격의 잔차를 누적하여 보정했습니다. 이 앱에서는 박자 시점의 편차를 Drift, 최근 박자 간격의 오차를 Jitter로 계산하고 표시하여 사용자가 재생 안정성과 설정 변경에 따른 일시적인 간격 변화를 확인할 수 있도록 했습니다.

## 결과 및 검증

모바일 사용 환경과 오디오 시간 처리 요구를 반영한 브라우저 기반 메트로놈을 구현했습니다.
