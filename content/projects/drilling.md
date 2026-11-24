---
id: drilling
title: Drilling
subtitle: 성장감을 고려한 게임플레이 기믹 구현
category:
- 게임 기획
- 게임 클라이언트 개발
project_type: team
status: unknown
# 상단 표시 문구만 변경. 실제 참여 범위는 participation 및 본문에 유지.
display_label: "Available on Steam"
role:
- 타일 파기 기믹 설계 및 구현
- 기본 캐릭터 조작 설계 및 구현
technologies: []
summary:
  overview: 타일을 파고 나가는 행동을 중심으로 하는 게임 팀 프로젝트입니다.
  problem: 업그레이드에 따른 성장이 단순한 수치 증가에 머물지 않고 실제 플레이의 변화로 체감되도록 하는 것이 목표였습니다.
  contribution: 초기 개발 단계에서 타일 파기 기믹과 기본 캐릭터 조작을 설계하고 구현했습니다.
  result: 초기 개발 단계의 타일 파기 및 기본 조작 기능을 구현했습니다. 팀 프로젝트는 Steam 상점에 소개되어 있습니다.
  resume: 초기 개발 단계에서 성장감을 고려한 타일 파기 기믹과 기본 캐릭터 조작을 설계·구현했습니다.
featured: true
order: 2
cover: steam-1
media:
- id: steam-1
  src: https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/4304980/d21c854de521ece2e5f92c86c5268ed1841ad33d/ss_d21c854de521ece2e5f92c86c5268ed1841ad33d.1920x1080.jpg?t=1779042818
  alt: Steam 상점에 공개된 Drilling 게임플레이 화면
  caption: 팀 프로젝트의 Steam 공개 화면(초기 개인 구현과 동일한 버전인지는 미확인).
  kind: screenshot
  credit: Drilling Steam 상점
- id: steam-2
  src: https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/4304980/e175bc1fb88caad5dda3c8adf777cb98633694fd/ss_e175bc1fb88caad5dda3c8adf777cb98633694fd.1920x1080.jpg?t=1779042818
  alt: Steam 상점에 공개된 Drilling 게임플레이 화면
  caption: 팀 프로젝트의 Steam 공개 화면(초기 개인 구현과 동일한 버전인지는 미확인).
  kind: screenshot
  credit: Drilling Steam 상점
links:
- kind: store
  label: Drilling Steam 상점 페이지
  url: https://store.steampowered.com/app/4304980/Drilling/?l=koreana
updated_at: '2026-11-24'
participation: 초기 개발 단계
implementation_techniques:
- 타일 상호작용 판정
- 캐릭터 입력 처리
---

## 문제 정의

업그레이드에 따른 성장이 단순한 수치 증가에 머물지 않고 실제 플레이의 변화로 체감되어야 한다고 생각했습니다. 성장할수록 더 빠르게 지형을 파고 나가는 경험을 목표로 했습니다.

## 역할 및 기여

팀 프로젝트의 초기 개발 단계에서 타일 파기 기믹과 기본 캐릭터 조작의 설계 및 구현을 담당했습니다.

## 설계 및 구현

### 성장감을 고려한 기믹 설계

앞서 정의한 성장감을 플레이어가 반복하는 핵심 행동인 타일 파기에 반영했습니다. 전달받은 업그레이드 수치를 실제 파기 속도에 적용하도록 구현했습니다.

### 핵심 타일 파기 구현

게임의 반복적인 핵심 행동인 타일 파기 기믹을 기획하고, 타일의 시각적 경계와 독립적인 상호작용 판정 범위를 설계하고 구현했습니다. 시각적 경계에 조작이 방해받지 않고 연속적으로 땅을 파는 경험을 목표로 했습니다.

### 기본 캐릭터 조작

WASD 이동, 마우스 방향 제어, 클릭 상호작용을 하나의 기본 조작 흐름으로 설계하고 구현했습니다.

## 결과 및 검증

초기 개발 단계에서 담당한 타일 파기와 기본 조작 기능을 구현했습니다. Steam 상점에는 팀 프로젝트의 소개와 게임 화면이 공개되어 있습니다.
