# Python Project Starter for KIER

## 프로젝트 개요

**이 리포지토리는 AI 응용 연구를 위한 프로젝트의 기본 구조와 환경 설정을 자동화하는 스타터 템플릿입니다.**

`init_project.py` 스크립트 실행 한 번으로 디렉토리 구조, 환경 변수 로드 시스템, 로깅 시스템이 즉시 구성되어 개발 초기 설정 시간을 획기적으로 단축할 수 있습니다.

-----

## 시작하기 (Quick Start)

새로운 프로젝트를 시작할 때는 **이 템플릿 리포지토리를 클론하여 로컬에서 새로운 Git 프로젝트로 재시작**하는 것을 권장합니다.

1.  **클론:** 이 템플릿 리포지토리를 로컬에 클론합니다.

    ```bash
    git clone [템플릿-리포지토리-URL] [새 프로젝트 이름]
    cd [새 프로젝트 이름]
    ```

2.  **Git 재시작:** 템플릿 리포지토리와의 연결을 끊고, 새 프로젝트를 위한 Git 히스토리를 새로 시작합니다.

    ```bash
    # 기존 Git 히스토리 삭제
    rm -rf .git

    # 새 프로젝트로 Git 초기화
    git init
    ```

    > **팁:** GitHub의 **`Use this template`** 버튼을 이용하면 위의 Git 재시작 과정 없이 바로 새 리포지토리가 생성됩니다.

3.  **초기화 스크립트 실행:** 프로젝트 초기 구조 및 설정을 자동 생성합니다.

    ```bash
    python init_project.py
    ```

### 필수 후속 단계

1.  **로컬 환경 설정 파일 생성** (API 키, 비밀번호 등 민감 정보 입력)

    ```bash
    cp secrets/.env.local.example secrets/.env.local
    # secrets/.env.local 파일을 열어 OPENAI_API_KEY, POSTGRES_PASSWORD 등을 입력합니다.
    ```

2.  **의존성 설치** (이 템플릿의 기본 요구 사항)

    ```bash
    # (선택) 가상 환경 활성화 후
    pip install python-dotenv
    # AI/ML 프로젝트에 필요한 추가 패키지를 requirements.txt에 추가하고 설치합니다.
    ```

3.  **설정 검증**

    ```bash
    python src/configs/config.py
    # 환경 변수가 정상적으로 로드되었는지 확인합니다.
    ```

-----

## 프로젝트 구조

`init_project.py` 스크립트 실행 후 AI 응용 연구에 최적화된 핵심 구조가 생성됩니다.

```
project/
├── src/
│   ├── configs/
│   │   ├── config.py           # 경로 관리, 환경변수 로드(dotenv), DB 설정
│   │   └── config_logs.py      # 컬러 콘솔/파일 로테이션 로깅 시스템 정의
│   └── utils/                  # 프로젝트 공통 유틸리티 모듈
├── secrets/
│   ├── .env.defaults           # 비민감 기본 설정 (Git Commit)
│   └── .env.local.example      # 민감 정보 템플릿 (Git Ignore)
├── .vscode/
│   └── settings.json           # VSCode 권장 설정 (인터프리터 경로 등)
├── data/                       # 원본 또는 처리된 데이터 파일 저장
├── db/                         # 데이터베이스 파일 (SQLite 등)
├── logs/                       # 실행 로그 파일 (자동 로테이션)
├── notebooks/                  # Jupyter/Colab 노트북 (모델 실험 및 분석)
├── init_project.py             # 템플릿 초기화 스크립트
└── .gitignore                  # Git 추적 제외 목록
```

-----

## 환경 변수 관리

모든 환경 변수는 `secrets/` 폴더 내의 **2단계 계층 구조**를 통해 관리되며, `src/configs/config.py`가 이 순서대로 로드합니다.

| 파일명 | 역할 | 민감 정보 포함 여부 | Git 커밋 여부 |
| :--- | :--- | :--- | :--- |
| **`.env.defaults`** | 프로젝트의 **기본값** (DB 타입, 포트 등 비민감 정보) | ❌ | ✅ **(커밋)** |
| **`.env.local`** | **로컬/운영 환경별** 민감 정보 (API Key, 비밀번호 등) | ✅ | ❌ **(무시)** |

### 로딩 우선순위:

$$.env.defaults \rightarrow .env.local \text{ (Overrides)}$$

-----

## 주요 모듈 사용 예시

### 1\. 설정 및 경로 사용 (`config.py`)

```python
# main.py 또는 기타 모듈에서
from src.configs.config import PATHS, DB_CONFIG

# 데이터 경로 접근 (AI/ML 데이터셋 저장)
data_path = PATHS["data"]

# 환경 변수로 로드된 DB 설정 사용
if DB_CONFIG["type"] == "postgresql":
    print(f"Connecting to {DB_CONFIG['postgresql']['host']}:{DB_CONFIG['postgresql']['port']}")
```

### 2\. 로깅 시스템 사용 (`config_logs.py`)

`config_logs.py`는 **날짜별 로그 파일** 자동 생성 및 **콘솔 컬러 출력**을 지원하여 디버깅 및 실험 추적에 유용합니다.

```python
# main.py 또는 시작 지점에서
import logging
from src.configs.config_logs import setup_root_logger, setup_logger

# 1. 루트 로거 초기화 (최초 1회 실행)
root_logger = setup_root_logger("project_core", log_level=logging.INFO)

# 2. 모듈별 로거 생성
logger = setup_logger(__name__)

# 로깅 메시지 출력 (콘솔에는 색상 적용, 파일에는 일반 텍스트 저장)
logger.info("모델 학습을 시작합니다.")
logger.debug(f"데이터 경로: {PATHS['data']}")
logger.error("데이터 로딩 중 치명적인 오류 발생.")
```

-----

## 라이선스

이 프로젝트 스타터는 KIER AI/CS 조직 내부에서 사용하기 위해 제공됩니다.
