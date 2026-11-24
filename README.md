# KimJ6 Portfolio

게임 클라이언트 개발 및 게임 기획 포트폴리오입니다. Markdown 원본에서 메인 페이지, 프로젝트 상세 페이지, 공개용 이력서 PDF를 생성합니다. GitHub Pages로 배포하며 서버나 데이터베이스를 사용하지 않습니다.

## 저장소 구조

```text
content/                 # 콘텐츠의 단일 원본 (Markdown + YAML)
  profile.md             # 닉네임, 관심 분야, 소개, 공통 링크
  projects/*.md          # 프로젝트 요약, 상세 설명, 이미지 및 링크
  resume.md              # 이력서 출력 설정과 프로젝트 참조
assets/                  # 공개용 이미지
docs/                    # 작성 기준, 공통 서식, 검수 기록
src/templates/           # 공통 HTML 및 PDF 템플릿
src/static/              # CSS, JavaScript
scripts/build.py         # 정적 사이트 생성 및 기본 검증
.github/workflows/       # GitHub Pages 자동 배포
site/                    # 생성된 출력물 (Git 추적 제외)
```

## 실행 및 미리보기

Python 3.12 권장. PDF 생성에는 WeasyPrint의 시스템 라이브러리(Pango 등)와 한글 글꼴(Noto Sans CJK KR 권장)이 필요합니다. Ubuntu 또는 WSL Ubuntu에서 다음 명령을 실행합니다.

```bash
sudo apt-get update
sudo apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 fonts-noto-cjk
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build.py
python -m http.server 8000 --directory site
```

브라우저에서 `http://localhost:8000/`을 엽니다. Windows에서 빌드 환경을 설치하지 않고 결과만 확인하려면 별도 제공된 정적 사이트 ZIP의 압축을 풀어 `index.html`을 열면 됩니다. 외부 이미지와 외부 링크에는 인터넷 연결이 필요합니다. 로컬 파일 열람은 브라우저의 로컬 저장소 정책에 따라 테마 저장이 제한될 수 있습니다.

## 콘텐츠 관리

- 프로필: `content/profile.md`에서 수정합니다.
- 프로젝트: `content/projects/`에서 프로젝트당 Markdown 파일 하나를 관리합니다. [프로젝트 서식](docs/templates/project-template.md)을 복제하여 고유한 `id`, `title`, `summary`, `role`, `technologies`, `media`, `links` 등을 작성합니다. `featured`는 대표 캐러셀 포함 여부, `order`는 표시 순서입니다. 본문은 H2부터 시작합니다. 기존 프로젝트의 표시 순서는 기존 프로젝트의 상대적 순서와 사용자 지정 삽입 위치(렌더링 연구, Drilling, OverTheHorizon, PinShift, PrecisionTick)를 유지하며, 명시적인 요청 없이 변경하지 않습니다. 미확인 상태에는 `unknown`을 사용하며 화면에 상태를 출력하지 않습니다. 확인하지 못한 기술은 추정하지 않습니다.
- 이미지: `assets/`에 파일을 추가한 뒤 `media[].src`에 `assets/파일명` 경로를 지정합니다. `cover`는 해당 이미지의 ID를 참조합니다. 외부 이미지의 권한과 접근성을 먼저 확인합니다.
- 이력서: `content/resume.md`의 `projects` 배열에서 포함할 프로젝트 ID를 관리합니다. 출력 순서는 프로젝트의 `order`를 따릅니다. 학력 및 어학 정보는 작성하지 않습니다. 프로젝트 요약, 기술, 논문 서지는 원본 문서에서 가져옵니다. 각 프로젝트 설명 아래 `technologies`를 사용 기술로 표시하며, 빈 목록은 생략합니다. 독립적인 기술 역량 섹션은 출력하지 않습니다.
- 수정 후 `python scripts/build.py`를 실행합니다. `site/`의 HTML과 PDF를 직접 수정하지 않습니다.

## 검증

빌드 과정에서 필수 메타데이터, 주요 자료형, 날짜, ID, 상태, 표시 순서, 필수 섹션과 제목 계층, 이미지 및 이력서 참조, 논문 기본 정보, 내부 파일 경로와 앵커 및 중복 HTML ID를 검사합니다. 실제 기여 범위, 기간, 성과, 외부 링크 및 공개 권한은 작성자가 별도로 확인해야 합니다. `docs/content-review.md`의 미확인 사항과 `docs/implementation-review.md`를 참고합니다.

## GitHub Pages 배포

1. GitHub에 새 저장소를 만들고 이 소스 ZIP의 내용을 저장소 루트에 넣습니다. `.github` 숨김 폴더를 포함합니다. `site/`는 커밋하지 않습니다.
2. 기본 브랜치를 `main`으로 설정하고 커밋 및 푸시합니다.
3. 저장소 Settings > Pages > Build and deployment > Source에서 GitHub Actions를 선택합니다.
4. Actions에서 `Deploy portfolio to GitHub Pages`를 실행하거나 `main`으로 푸시합니다. 최초 실행이 Pages 설정 전에 실패한 경우 다시 실행합니다.
5. 성공한 배포의 URL을 확인한 뒤 로그아웃 상태에서 페이지와 PDF를 확인합니다.

프로젝트 Pages와 사용자 Pages 모두 상대 경로를 사용합니다. 실제 배포 URL은 아직 생성되지 않았습니다. GitHub Actions에서 configure-pages의 base_url을 PDF 생성에 전달합니다. 로컬에서는 실제 주소를 확인한 경우에만 `profile.md`의 `links.portfolio` 또는 `PORTFOLIO_URL` 환경 변수를 설정합니다. 과제 제출 TXT에는 배포와 공개 접근을 확인한 URL만 기록합니다.

## 작성 및 관리 기준

- [요구사항 및 작성 원칙](docs/requirements.md)
- [정보 구조 및 형식 설계](docs/information-architecture.md)
- [Markdown 서식 규격](docs/markdown-specification.md)
- [공통 작성 서식](docs/templates/)

- [콘텐츠 검수 및 수정 기록](docs/content-review.md)
- [Markdown 서식 보정](docs/markdown-specification-amendment.md)
- [웹사이트 구현 및 검증 기록](docs/implementation-review.md)

상위 요구사항 및 정보 구조 설계는 아래 저장소 문서를 따릅니다. 작성 원본과 렌더링 구조의 변경은 별도 작업 단위로 관리합니다. 공개 저장소에 포함할 문서와 자료의 공개 적합성을 검토합니다.

현재 `featured`는 캐러셀 포함 여부이며 모든 프로젝트는 목록에 표시합니다. 최소 한 프로젝트의 `featured`는 true여야 합니다. 추가 경험 문서, 본문 이미지 ID 참조, 수식 렌더링, 구문 강조는 아직 지원하지 않습니다.
