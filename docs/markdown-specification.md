# Markdown 서식 규격 v1.3 (웹사이트 구현 v1.2)

[요구사항](requirements.md)과 [정보 구조](information-architecture.md)를 적용한다. 이 문서는 이전 서식 설계와 v1.1 서식 보정을 통합한 현재 구현 규격이다. 실제 작성 예는 [templates](templates/)를 참고한다.

## 공통 문법

UTF-8, 영문 소문자·숫자·하이픈 파일명, YAML Front Matter, CommonMark 및 표 확장. 본문은 H2부터 시작하고 제목 계층을 건너뛰지 않는다. YAML 주석과 HTML 주석은 작성용이며 공개 내용에는 임시 표기를 남기지 않는다. 본문 내 표현용 HTML은 비활성화되어 있다. 날짜는 문자열 `YYYY-MM-DD`, 프로젝트 기간은 확인된 정밀도(`YYYY`, `YYYY-MM`, `YYYY-MM-DD`)만 사용한다.

## 프로필

필수: `nickname`, `interests`(문자열 목록), `headline`, `summary`, `links.github`, `updated_at`. 선택: `focus_technologies`, `links.email`, `links.linkedin`, `links.portfolio`. 슬로건은 단일 문자열이며 YAML `|-` 블록으로 줄바꿈을 지정할 수 있다. 선택 필드 `headline_emphasis`는 슬로건에 실제 존재하는 중복되지 않는 문자열 목록이며, 의미적 강조 대상만 지정한다. 색상과 표현은 [시각적 강조 및 테마 규격](visual-design.md)을 따른다. `PORTFOLIO_URL` 환경 변수가 실제 배포 주소를 제공하면 이력서 PDF에 우선 사용한다. 로컬 빌드에서 URL을 모르면 생략한다.

## 프로젝트

| 필드 | 형식 및 책임 |
| --- | --- |
| `id` | 고유 영문 소문자·숫자·하이픈 식별자 |
| `title`, `subtitle` | 공식명, 핵심 특징(보조 제목 선택) |
| `category` | 비어 있지 않은 문자열 목록 |
| `project_type` | individual, team, collaborative |
| `status` | planned, in-progress, prototype, completed, released, archived, unknown. 미확인은 화면에서 생략 |
| `participation` | 선택 문자열, 개인의 참여 범위 |
| `display_label` | 선택 문자열, 웹 프로젝트 상단에서 상태 및 참여 범위 표시를 대체. 빈 문자열이면 둘 다 숨김. 원본 상태와 참여 범위는 유지 |
| `period.start`, `period.end` | 선택 날짜 문자열, 확인된 기간만 |
| `role` | 비어 있지 않은 문자열 목록, 담당 역할 |
| `technologies` | 실제 사용 기술 목록. 미확인 시 빈 배열 허용 |
| `implementation_techniques` | 선택 목록, 기술 스택과 구분 |
| `summary` | overview, problem, contribution, result 필수 문자열; resume 선택 |
| `featured` | 불리언, 대표 캐러셀 포함 여부. 최소 하나 true; 모든 프로젝트는 목록에 표시 |
| `order` | 선택 양의 정수, 지정 값끼리 중복 금지. 기존 프로젝트의 상대적 순서와 사용자 지정 삽입 위치 유지; 사용자 요청 없이 재정렬 금지 |
| `media` | 선택 목록, id/src/alt 필수, caption/kind/credit 선택 |
| `cover` | 선택, media ID 참조 |
| `links` | 선택 목록, kind/label/url, 실제 공개 자료만 |
| `publication` | 선택 객체: title, journal, pages, author_role, doi, year/month/volume/issue; publisher 선택 |
| `updated_at` | 필수 YYYY-MM-DD 문자열 |

미확인 기간과 상태는 임의로 채우지 않는다. 본문 필수 영역은 문제 정의, 역할 및 기여, 설계 및 구현(또는 플레이 및 실행 구조 설계), 결과 및 검증. 인사이트 및 한계는 의미 있는 경우 추가한다. 주요 사례는 H3 또는 H4를 사용하고 문제 → 판단 → 수행 → 확인된 결과 또는 제약을 설명한다. 모든 요소를 별도 문단으로 강제하지 않는다. 설계, 구현, 검증을 구분한다. 참고 작품과 기존 인과관계를 유지한다.

이미지 경로는 `assets/`로 시작하거나 공개 HTTP(S) URL을 사용한다. 대표 이미지 및 갤러리는 메타데이터로 관리한다. 본문에서 별도 이미지 ID를 참조하는 기능은 아직 미구현이다. 외부 링크의 실제 접속 및 공개 권한은 사람이 확인한다. 공개용 캡션은 이미지가 보여주는 정보와 필요한 출처만 간결하게 표시한다. 작성·검수 과정의 미확인 기록과 작업 지침은 관리 문서에 분리하고, 독자의 판단에 필요한 실제 참여 범위와 검증 한계는 본문에서 정확하게 전달한다.

## 이력서

`title`, `projects`(고유 프로젝트 ID 목록), `updated_at` 필수. `experiences`는 현재 빈 배열만 지원. `projects`는 포함 대상을 지정하며 표시 순서는 개별 프로젝트의 `order`를 따른다. 학력 및 어학 정보는 원본과 출력에서 제외한다. 본문은 비워 둘 수 있다. 프로젝트 기여 요약, 알려진 기간, 기술 및 논문 정보는 원본을 참조한다. 각 프로젝트의 `technologies`는 해당 설명 아래 사용 기술로 표시하고 빈 배열이면 행을 생략한다. 독립적인 기술 역량 섹션은 출력하지 않는다. 미확인 기간과 배포 URL은 생략한다.

## 검증 및 지원 범위

빌드는 필수 메타데이터, 주요 자료형, 날짜, ID, 순서, 필수 프로젝트 섹션, 제목 계층, 이미지 및 프로젝트 참조, 논문 기본 정보, 상대 링크와 앵커, 중복 HTML ID를 검사한다. 모든 의미 검수 또는 모든 임시 문구 탐지를 보장하지 않는다. 수식 렌더링, 코드 구문 강조, 독립 추가 경험 문서는 미지원이다. 실제 원문·코드·논문 대조, 외부 링크 및 공개 적합성은 별도 확인한다.
