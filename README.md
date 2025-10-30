# 💬 Gemini Chat App

> Google **Gemini 2.5 Flash API** 기반 Streamlit 채팅 앱  
> 💬 한글 지원 / 🌗 자동 다크모드 대응 / ⌨️ 엔터키 전송 가능

---

## 📸 미리보기
![Gemini Chat App Screenshot](https://github.com/your-repo-name/streamlit-gemini/assets/preview.png)

---

## 🚀 주요 기능

| 기능 | 설명 |
|------|------|
| 💬 **Gemini API 연동** | Google Generative AI(`google-generativeai`)를 이용해 실시간 대화 |
| ⌨️ **엔터키 입력 지원** | `st.chat_input()` 사용으로 엔터 전송 자동 처리 |
| 🌗 **자동 테마 대응** | 다크/라이트 모드 자동 전환 (`prefers-color-scheme` CSS) |
| 🧹 **가독성 강화 UI** | 사용자/AI 말풍선 색상 구분, 폰트 정돈 |
| ☁️ **Streamlit Cloud 호환** | requirements + secrets.toml로 바로 배포 가능 |

---

## 🛠️ 설치 및 실행

### 1️⃣ 로컬 실행 (Mac / Windows)

```bash
git clone https://github.com/your-username/streamlit-gemini.git
cd streamlit-gemini

# 패키지 설치
pip install -r requirements.txt

# 실행
streamlit run app.py
