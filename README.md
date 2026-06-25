# Oboetoki Backend

Oboetoki 안드로이드 앱을 위한 백엔드 API 서버입니다. 사용자의 단어장을 관리하고, OpenAI Vision 모델을 활용하여 이미지(사진)에서 단어와 뜻, 발음(요미가나 등)을 자동으로 추출해주는 강력한 OCR 기능을 제공합니다.

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.x)
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens), bcrypt
- **AI/ML**: OpenAI Vision API (GPT-4o-mini / GPT-4-vision)
- **Infrastructure**: Docker & Docker Compose

## 📁 Project Structure

```text
oboetoki-backend/
├── docker/
│   ├── compose/
│   │   └── docker-compose.yml  # DB 및 API 서버 실행용 컨테이너 설정
│   └── env/                    # 환경변수 파일 디렉토리
└── services/api/
    ├── app/
    │   ├── core/               # 보안(JWT, Hashing) 및 공통 설정
    │   ├── db/                 # 데이터베이스 연결 설정
    │   ├── models/             # SQLAlchemy DB 모델 (User, UserWord)
    │   ├── routes/             # API 라우터 (auth, main, words)
    │   ├── schemas/            # Pydantic 데이터 검증 스키마
    │   └── services/           # 외부 연동 서비스 (LLM Service)
    ├── main.py                 # FastAPI 애플리케이션 엔트리포인트
    ├── requirements.txt        # 패키지 의존성
    └── Dockerfile              # API 서버 도커 이미지 빌드 파일
```

## ✨ Key Features

1. **사용자 인증 (Auth)**
   - 이메일 기반 회원가입 및 로그인 (JWT 인증)
   - 비밀번호 단방향 암호화 (bcrypt)
   - 이메일 중복 확인 및 내 정보 조회 기능

2. **단어장 관리 (Words)**
   - 단일 단어 및 여러 단어(Batch) 추가
   - 중복 단어 방지 로직 구현 (`409 Conflict` 반환 및 일괄 추가 시 자동 무시)
   - 원어(`original_word`), 발음(`reading`), 뜻(`translated_word`), 원본 언어(`source_language`) 저장
   - 단어 수정, 삭제, 암기 완료 상태 토글 기능
   - 단어 검색 기능: 원어, 발음, 뜻 중 하나라도 포함된 텍스트 기반 검색 지원
   - 목록 조회 시 등록일자(최신순/오래된순), 암기 여부, 원본 언어(`source_language`)에 따른 필터링 및 정렬 지원

3. **스마트 OCR 추출 (Vision AI)**
   - 사진을 업로드하면 OpenAI Vision LLM이 이미지를 분석하여 단어 목록을 추출
   - 원어뿐만 아니라 발음(일본어의 경우 요미가나)과 한국어 뜻을 한 번에 파싱
   - 결과를 클라이언트(앱)로 반환하여 사용자가 확인 후 일괄 저장 가능

4. **대시보드 통계 (Main)**
   - 로그인 사용자의 연속 출석일 수, 전체 단어 수, 외운 단어 수 집계
   - 매일 바뀌는 '오늘의 한 마디' 명언 및 저자(Author) 정보 제공 (DB 기반 순환 제공)

## 🚀 Getting Started

### 1. Prerequisites
- [Docker](https://docs.docker.com/get-docker/) 및 Docker Compose 설치
- OpenAI API Key

### 2. Environment Variables (`.env` 설정)
`docker/env/` 디렉토리에 다음 두 개의 파일을 생성하고 설정합니다.

**`docker/env/.env.api`**
```env
# Database URL (Docker Compose 내부망 기준)
DATABASE_URL=mysql+pymysql://<user>:<password>@db:3306/oboetoki

# JWT Secret
JWT_SECRET=your_super_secret_jwt_key

# OpenAI API Key (OCR 기능 사용을 위해 필수)
OPENAI_API_KEY=sk-...
```

**`docker/env/.env.db`**
```env
MYSQL_ROOT_PASSWORD=root_password
MYSQL_DATABASE=oboetoki
MYSQL_USER=<user>
MYSQL_PASSWORD=<password>
```

### 3. Run with Docker Compose
```bash
cd docker/compose
docker-compose up -d --build
```
- API 서버: `http://localhost:8000/`
- API 문서 (Swagger UI): `http://localhost:8000/docs`