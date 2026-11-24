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
- 타일 파괴 기믹 설계 및 구현
- 기본 캐릭터 조작 설계 및 구현
technologies:
- Unity
summary:
  overview: 동아리에서 개발한 Unity 기반 2D 채굴 탐험 게임입니다.
  problem: 업그레이드로 채굴 범위와 속도를 늘리면서도 기존 조작감을 일관되게 유지하는 것이 목표였습니다.
  contribution: 캐릭터 조작과 타일 파괴를 담당하여 물리 충돌과 채굴 판정을 분리하는 방식을 제안하고 별도의 AABB로 구현했습니다.
  result: 업그레이드에 따라 더 넓은 범위를 빠르게 채굴하면서 기존 조작감을 일관되게 유지하도록 구현했습니다.
  resume: 캐릭터 조작과 타일 파괴를 담당하고, 채굴 범위 확장이 기존 조작에 영향을 주지 않도록 물리 충돌과 AABB 기반 채굴 판정을 분리해 구현했습니다.
featured: true
order: 2
cover: steam-1
media:
- id: steam-1
  src: https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/4304980/d21c854de521ece2e5f92c86c5268ed1841ad33d/ss_d21c854de521ece2e5f92c86c5268ed1841ad33d.1920x1080.jpg?t=1779042818
  alt: Steam 상점에 공개된 Drilling 게임플레이 화면
  caption: Drilling 게임플레이 화면
  kind: screenshot
- id: steam-2
  src: https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/4304980/e175bc1fb88caad5dda3c8adf777cb98633694fd/ss_e175bc1fb88caad5dda3c8adf777cb98633694fd.1920x1080.jpg?t=1779042818
  alt: Steam 상점에 공개된 Drilling 게임플레이 화면
  caption: Drilling 게임플레이 화면
  kind: screenshot
links:
- kind: store
  label: Drilling Steam 상점 페이지
  url: https://store.steampowered.com/app/4304980/Drilling/?l=koreana
updated_at: '2026-11-24'
participation: 초기 개발 단계
implementation_techniques:
- AABB 기반 타일 파괴 판정
- 캐릭터 입력 처리
---

## 문제 정의

팀의 목표는 채굴의 재미와 성장 체감을 제공하는 것이었습니다. 업그레이드에 따른 성장이 단순한 수치 증가에 머물지 않고 더 넓은 범위를 빠르게 채굴하는 경험으로 이어지도록 하고자 했습니다.

## 역할 및 기여

동아리 팀 프로젝트의 초기 개발 단계에서 캐릭터 조작과 타일 파괴 기능의 설계 및 구현을 담당했습니다.

## 설계 및 구현

### 채굴 속도를 통한 성장 체감

플레이어가 반복하는 핵심 행동인 채굴에서 성장감을 체감하도록, 전달받은 업그레이드 수치를 실제 타일 파괴 속도에 반영했습니다.

### 물리 충돌과 타일 파괴 판정의 분리

채굴 범위를 늘릴 때 드릴의 외형과 물리 충돌 범위까지 함께 변경하면 기존 캐릭터 조작에 영향을 줄 수 있다고 판단했습니다. 이에 물리 충돌과 타일 파괴 판정을 분리하는 방식을 제안하고, 별도의 축 정렬 경계 상자(AABB)를 이용해 타일의 시각적 경계와 독립적인 파괴 판정 범위를 구현했습니다.

채굴 범위가 확장되어도 기존 조작감을 일관되게 유지하고, 시각적 경계에 방해받지 않는 연속적인 채굴 경험을 제공하도록 설계했습니다.

### 기본 캐릭터 조작

WASD 이동, 마우스 방향 제어, 클릭 상호작용을 하나의 기본 조작 흐름으로 설계하고 구현했습니다.

## 결과 및 검증

채굴 범위와 속도를 업그레이드할 수 있도록 타일 파괴 기능을 구현하고, 물리 충돌과 채굴 판정의 분리를 통해 기존 캐릭터 조작에 영향을 주지 않도록 구성했습니다. 팀 프로젝트의 소개와 게임 화면은 Steam에서 확인할 수 있습니다.
