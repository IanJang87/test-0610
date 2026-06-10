# BMW 상품정보 대시보드

Streamlit 기반의 BMW 판매 데이터 대시보드와 Gemini AI 어시스턴트 통합 애플리케이션입니다.

## 🚀 시작하기

### 1. 저장소 클론

```bash
git clone https://github.com/IanJang87/test-0610.git
cd test-0610
```

### 2. 환경 설정

#### .env 파일 생성

`.env.example` 파일을 참고하여 `.env` 파일을 생성하세요:

```bash
cp .env.example .env
```

#### API 키 설정

`.env` 파일을 열어서 `GEMINI_API_KEY`에 당신의 API 키를 입력하세요:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-flash-latest
```

**Gemini API 키 생성 방법:**
1. [Google AI Studio](https://aistudio.google.com/apikey)에 접속
2. "Get API Key" 클릭
3. 새 API 키 생성
4. 생성된 키를 `.env` 파일에 복사

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 앱 실행

```bash
streamlit run dashboard.py
```

앱이 자동으로 브라우저에서 열립니다: http://localhost:8501

## 📊 주요 기능

- **📊 개요** - 판매 현황 및 KPI 메트릭
- **💰 판매분석** - 지역별/모델별 판매 분석
- **📦 재고관리** - 실시간 재고 현황
- **😊 고객만족도** - 고객 만족도 분석
- **⭐ 옵션분석** - 옵션별 판매 분석
- **🏆 경쟁분석** - 경쟁사 분석
- **🤖 AI 어시스턴트** - Gemini 기반 대시보드 문의

## 🔧 기술 스택

- **Frontend**: Streamlit
- **Data Visualization**: Plotly
- **AI**: Google Gemini API
- **Data Processing**: Pandas, NumPy

## 📝 환경 변수

| 변수명 | 설명 | 필수 |
|--------|------|------|
| `GEMINI_API_KEY` | Gemini API 키 | ✅ 필수 |
| `GEMINI_MODEL` | 사용할 Gemini 모델 | ❌ 선택 (기본값: gemini-flash-latest) |

## ☁️ Streamlit Cloud 배포

### 1. GitHub에 푸시

```bash
git push origin main
```

### 2. Streamlit Cloud에서 배포

1. [Streamlit Community Cloud](https://streamlit.io/cloud)에 로그인
2. "New App" 클릭
3. GitHub 저장소 선택: `IanJang87/test-0610`
4. 메인 파일 경로: `dashboard.py`
5. "Deploy" 클릭

### 3. Secrets 설정 (중요!)

배포 후 앱 설정에서:

1. 톱니바퀴(⚙️) 아이콘 → "Secrets" 클릭
2. 다음 내용 입력:

```toml
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
GEMINI_MODEL = "gemini-flash-latest"
```

3. "Save" 클릭

### 4. 앱 접속

배포 완료 후 자동으로 제공되는 URL에서 앱에 접속할 수 있습니다.

### ⚠️ Secrets 관리

- 🔒 **Secrets은 암호화되어 저장됨**
- 🚫 `.env` 파일과 `secrets.toml`은 GitHub에 업로드되지 않음
- ✅ Streamlit Cloud의 웹 인터페이스에서만 설정

## ⚠️ 중요 사항

- `.env` 파일은 절대 Git에 커밋하지 마세요 (API 키 노출 위험)
- `.streamlit/secrets.toml`은 로컬 개발용이며 GitHub에 업로드되지 않습니다
- 본인의 API 키만 사용하세요
- 무료 API 키는 사용량 제한이 있을 수 있습니다
- Streamlit Cloud의 Secrets은 배포 후 반드시 설정하세요

## 📄 라이선스

MIT License

## 👨‍💻 개발자

Claude Code

---

**문제가 있거나 개선 사항이 있으면 이슈를 등록해주세요.**
