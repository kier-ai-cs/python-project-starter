#!/usr/bin/env python3
"""
프로젝트 기본 구조 및 설정 파일 자동 생성 스크립트

Python 프로젝트의 디렉토리 구조, 환경 변수 템플릿, 로깅 설정 등을
자동으로 생성하여 프로젝트 초기 설정 시간을 단축합니다.

Usage:
    python init_project.py
"""

import os
from textwrap import dedent

# === 프로젝트 루트 경로 ===
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# === 디렉토리 생성 ===
DIRS = [
    os.path.join(PROJECT_ROOT, "src", "configs"),
    os.path.join(PROJECT_ROOT, "src", "utils"),
    os.path.join(PROJECT_ROOT, "notebooks"),
    os.path.join(PROJECT_ROOT, "data"),
    os.path.join(PROJECT_ROOT, "db"),
    os.path.join(PROJECT_ROOT, "logs"),
    os.path.join(PROJECT_ROOT, "secrets"),
    os.path.join(PROJECT_ROOT, ".vscode"),
]

for d in DIRS:
    os.makedirs(d, exist_ok=True)

# === .env.defaults 생성 (리포에 커밋 가능) ===
env_defaults = dedent("""\
########################################
# 🔐 기본 설정 (비민감 정보)
########################################
# 이 파일은 리포지토리에 커밋됩니다.
# 민감한 정보는 .env.local에 작성하세요.

########################################
# 🗄️ DATABASE CONFIGURATION
########################################
DB_TYPE=sqlite

# PostgreSQL 설정 (운영 단계에서 .env.local에서 오버라이드)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_DB=project_db

########################################
# 📝 LOGGING
########################################
LOG_LEVEL=INFO
""")

defaults_path = os.path.join(PROJECT_ROOT, "secrets", ".env.defaults")
if not os.path.exists(defaults_path):
    with open(defaults_path, "w", encoding="utf-8") as f:
        f.write(env_defaults)
    print(f"✅ Created: {defaults_path}")
else:
    print(f"⚠ Skipped (already exists): {defaults_path}")


# === .env.local.example 생성 ===
env_local_example = dedent("""\
########################################
# 🔐 로컬 환경 설정 (민감 정보)
########################################
# 이 파일을 .env.local로 복사하여 사용하세요.
# .env.local은 절대 커밋되지 않습니다.

########################################
# API KEYS
########################################
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
UPSTAGE_API_KEY=upstage-xxxxxxxxxxxxxxxxxxxxxxxxx
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

########################################
# DATABASE (Production)
########################################
# POSTGRES_PASSWORD=your_secure_password_here
# POSTGRES_HOST=production-db.example.com
""")

local_example_path = os.path.join(PROJECT_ROOT, "secrets", ".env.local.example")
if not os.path.exists(local_example_path):
    with open(local_example_path, "w", encoding="utf-8") as f:
        f.write(env_local_example)
    print(f"✅ Created: {local_example_path}")
else:
    print(f"⚠ Skipped (already exists): {local_example_path}")


# === .gitignore 생성 ===
gitignore_content = dedent("""\
# Python
__pycache__/
*.pyc
*.pyo
*.pyd

# Virtual environments
.venv/
venv/
env/

# Logs and data
logs/
data/
db/raw/
**/__pycache__/

# Secrets - 모든 .env 파일 무시
secrets/.env*

# 예외: 기본값과 예시 파일은 커밋 허용
!secrets/.env.defaults
!secrets/.env.local.example
""")

gitignore_path = os.path.join(PROJECT_ROOT, ".gitignore")
if not os.path.exists(gitignore_path):
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    print(f"✅ Created: {gitignore_path}")
else:
    print(f"⚠ Skipped (already exists): {gitignore_path}")


# === .vscode/settings.json 생성 ===
vscode_settings = dedent("""\
{
    // Python 인터프리터 설정
    "python.defaultInterpreterPath": "",
}
""")

vscode_settings_path = os.path.join(PROJECT_ROOT, ".vscode", "settings.json")
if not os.path.exists(vscode_settings_path):
    with open(vscode_settings_path, "w", encoding="utf-8") as f:
        f.write(vscode_settings)
    print(f"✅ Created: {vscode_settings_path}")
else:
    print(f"⚠ Skipped (already exists): {vscode_settings_path}")


# === src/configs/config.py 생성 ===
config_py = dedent("""\
import os
import sys
from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PATHS = {
    "root": PROJECT_ROOT,
    "src": os.path.join(PROJECT_ROOT, "src"),
    "configs": os.path.join(PROJECT_ROOT, "src", "configs"),
    "data": os.path.join(PROJECT_ROOT, "data"),
    "db": os.path.join(PROJECT_ROOT, "db"),
    "logs": os.path.join(PROJECT_ROOT, "logs"),
    "utils": os.path.join(PROJECT_ROOT, "src", "utils"),
    "secrets": os.path.join(PROJECT_ROOT, "secrets"),
    "notebooks": os.path.join(PROJECT_ROOT, "notebooks"),
}

# .env 파일 계층 로드: defaults -> local (로컬이 우선)
ENV_DEFAULTS = os.path.join(PATHS["secrets"], ".env.defaults")
ENV_LOCAL = os.path.join(PATHS["secrets"], ".env.local")

if os.path.exists(ENV_DEFAULTS):
    load_dotenv(ENV_DEFAULTS)
    print(f"✅ Loaded: {ENV_DEFAULTS}")
else:
    print(f"⚠ .env.defaults not found at: {ENV_DEFAULTS}")

if os.path.exists(ENV_LOCAL):
    load_dotenv(ENV_LOCAL, override=True)
    print(f"✅ Loaded: {ENV_LOCAL} (override)")
else:
    print(f"⚠ .env.local not found. Using defaults only.")

ENV_LIST = [
    "OPENAI_API_KEY",
    "UPSTAGE_API_KEY",
]

DB_CONFIG = {
    "type": os.getenv("DB_TYPE", "sqlite"),
    "sqlite": {"path": os.path.join(PATHS["db"], "database.sqlite3")},
    "postgresql": {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", ""),
        "database": os.getenv("POSTGRES_DB", "project_db"),
    },
}

for path in [PATHS["root"], PATHS["src"], PATHS["utils"]]:
    if path not in sys.path:
        sys.path.append(path)

def verify_env_vars():
    \"\"\"환경변수 검증\"\"\"
    missing = []
    for key in ENV_LIST:
        val = os.getenv(key)
        if val:
            print(f"✅ {key} is set.")
        else:
            print(f"⚠ {key} is missing!")
            missing.append(key)
    
    if missing:
        print(f"\\n💡 Tip: Copy secrets/.env.local.example to secrets/.env.local and add your keys.")
    
    return len(missing) == 0

if __name__ == "__main__":
    verify_env_vars()
    print(f"\\nDatabase type: {DB_CONFIG['type']}")
""")

config_path = os.path.join(PROJECT_ROOT, "src", "configs", "config.py")
if not os.path.exists(config_path):
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(config_py)
    print(f"✅ Created: {config_path}")
else:
    print(f"⚠ Skipped (already exists): {config_path}")


# === src/configs/config_logs.py 생성 ===
config_logs_py = dedent("""\
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone
import os

class ColorFormatter(logging.Formatter):
    \"\"\"콘솔 출력용 컬러 포매터 - 로그 레벨만 색상 적용\"\"\"
    COLORS = {
        'DEBUG': '\033[94m',      # 파란색
        'INFO': '\033[92m',       # 초록색
        'WARNING': '\033[93m',    # 노란색
        'ERROR': '\033[91m',      # 빨간색
        'CRITICAL': '\033[95m',   # 보라색
    }
    RESET = '\033[0m'

    def format(self, record):
        # 로그 레벨에 색상 적용
        levelname_color = self.COLORS.get(record.levelname, self.RESET)
        colored_levelname = f"{levelname_color}{record.levelname}{self.RESET}"
        
        # 원본 levelname을 임시로 저장하고 색상이 적용된 것으로 교체
        original_levelname = record.levelname
        record.levelname = colored_levelname
        
        # 포맷 적용
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        formatted = logging.Formatter(log_fmt).format(record)
        
        # 원본 levelname 복원
        record.levelname = original_levelname
        
        return formatted

def setup_root_logger(
    logger_name: str,
    log_level=logging.INFO,
    max_size_mb: int = 10,
    backup_count: int = 5,
    project_root_dir: str = None,
):
    \"\"\"
    루트 로거 설정

    Args:
        logger_name: 로그 파일명에 사용될 이름
        log_level: 로깅 레벨 (기본: INFO)
        max_size_mb: 로그 파일 최대 크기 (MB)
        backup_count: 백업 파일 개수
        project_root_dir: 프로젝트 루트 디렉토리 (기본: auto-detect)
    \"\"\"
    if project_root_dir is None:
        project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    log_dir = os.path.join(project_root_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    log_file = os.path.join(log_dir, f"{today}-{logger_name}.log")

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    if not root_logger.hasHandlers():
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_size_mb * 1024 * 1024,
            backupCount=backup_count, encoding="utf-8"
        )
        console_handler = logging.StreamHandler()

        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(ColorFormatter())

        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

    return root_logger

def setup_logger(module_name: str):
    \"\"\"모듈별 로거 생성\"\"\"
    logger = logging.getLogger(module_name)
    logger.propagate = True
    return logger
""")

config_logs_path = os.path.join(PROJECT_ROOT, "src", "configs", "config_logs.py")
if not os.path.exists(config_logs_path):
    with open(config_logs_path, "w", encoding="utf-8") as f:
        f.write(config_logs_py)
    print(f"✅ Created: {config_logs_path}")
else:
    print(f"⚠ Skipped (already exists): {config_logs_path}")


# === .vscode/settings.json 생성 ===
vscode_settings = dedent("""\
{
    // Python 인터프리터 경로 (사용자가 직접 설정)
    // 예시: "${workspaceFolder}/.venv/bin/python"
    // 예시: "/usr/bin/python3"
    // 예시: "C:/Python311/python.exe"
    "python.defaultInterpreterPath": "",
    
    // Jupyter 커널 경로 (사용자가 직접 설정)
    // "jupyter.kernels.filter": [
    //     {
    //         "path": "${workspaceFolder}/.venv/bin/python",
    //         "type": "pythonEnvironment"
    //     }
    // ],

    // ============================
    // Live Server 기본 보안 설정
    // ============================
    // 1) 같은 머신에서만 접속 가능 (127.0.0.1)
    // 2) 웹 루트는 프로젝트 루트가 아니라 app/으로 제한
    "liveServer.settings.host": "127.0.0.1",
    "liveServer.settings.root": "app",

    // 추가 설정
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true,
    "python.terminal.activateEnvironment": true,
    
    // 파일 제외 설정
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    },
    
    // 포맷터 (선택사항 - 필요시 활성화)
    // "python.formatting.provider": "black",
    // "[python]": {
    //     "editor.formatOnSave": true,
    //     "editor.codeActionsOnSave": {
    //         "source.organizeImports": true
    //     }
    // }
}
""")

vscode_settings_path = os.path.join(PROJECT_ROOT, ".vscode", "settings.json")
if not os.path.exists(vscode_settings_path):
    with open(vscode_settings_path, "w", encoding="utf-8") as f:
        f.write(vscode_settings)
    print(f"✅ Created: {vscode_settings_path}")
else:
    print(f"⚠ Skipped (already exists): {vscode_settings_path}")


# === README.md 생성 ===
readme_content = dedent("""\
# Python Project Structure Initializer

프로젝트 초기 구조와 설정 파일을 자동으로 생성하는 스크립트입니다.

## 🚀 사용법

```bash
python init_project.py
```

## 📂 생성되는 구조

```
project/
├── src/
│   ├── configs/
│   │   ├── config.py          # 프로젝트 설정 (경로, DB, 환경변수)
│   │   └── config_logs.py     # 로깅 설정 (파일/콘솔 출력)
│   └── utils/                 # 유틸리티 함수
├── secrets/
│   ├── .env.defaults          # 기본 설정 (커밋 가능)
│   └── .env.local.example     # 로컬 환경 템플릿
├── .vscode/
│   └── settings.json          # VSCode 설정 (Python/Jupyter)
├── data/                      # 데이터 파일
├── db/                        # 데이터베이스 파일
├── logs/                      # 로그 파일
├── notebooks/                 # Jupyter 노트북
└── .gitignore                 # Git 제외 파일 목록
```

## 🔐 환경변수 계층 구조

이 프로젝트는 환경변수를 2단계로 분리하여 관리합니다:

### 1. `.env.defaults` (커밋 가능 ✅)
- 비민감 정보 (DB 타입, 기본 포트 등)
- 팀원 모두가 공유하는 기본값
- 리포지토리에 커밋됨

### 2. `.env.local` (커밋 불가 ❌)
- 민감 정보 (API 키, 비밀번호 등)
- 개인 환경 설정
- `.gitignore`에 의해 보호됨

### 로딩 순서
```
.env.defaults 로드 → .env.local 로드 (덮어쓰기)
```

## 🔧 다음 단계

1. **로컬 환경 설정**
   ```bash
   cp secrets/.env.local.example secrets/.env.local
   # .env.local 파일을 열어 실제 API 키 입력
   ```

2. **의존성 설치**
   ```bash
   pip install python-dotenv
   # 추가 필요한 패키지 설치
   ```

3. **설정 확인**
   ```bash
   python src/configs/config.py
   ```

## 📝 주요 기능

### config.py
- 프로젝트 경로 관리 (`PATHS` 딕셔너리)
- 환경변수 계층 로드 (defaults → local)
- SQLite/PostgreSQL DB 설정
- sys.path 자동 추가

### config_logs.py
- 컬러 로그 콘솔 출력
- 날짜별 로그 파일 자동 생성
- 로그 파일 자동 로테이션

## 💡 사용 예시

```python
# 설정 불러오기
from src.configs.config import PATHS, DB_CONFIG
from src.configs.config_logs import setup_root_logger, setup_logger

# 로거 초기화
setup_root_logger("myapp")
logger = setup_logger(__name__)

# 사용
logger.info(f"Data directory: {PATHS['data']}")
```

## 🤝 기여

이 스크립트는 자유롭게 사용하고 수정할 수 있습니다.
""")

readme_path = os.path.join(PROJECT_ROOT, "README.md")
if not os.path.exists(readme_path):
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"✅ Created: {readme_path}")
else:
    print(f"⚠ Skipped (already exists): {readme_path}")


print("\n" + "="*50)
print("🎉 Project structure initialization complete!")
print("="*50)
print("\n📋 Next steps:")
print("  1. cp secrets/.env.local.example secrets/.env.local")
print("  2. Edit secrets/.env.local and add your API keys")
print("  3. python src/configs/config.py  # Verify setup")
print("\n✨ Happy coding!")
