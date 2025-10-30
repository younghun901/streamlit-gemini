import streamlit as st
import google.generativeai as genai

# ---------------------------
# Gemini 응답 함수
# ---------------------------
def generate_answer(prompt: str) -> str:
    """Gemini API로 답변 생성"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        if hasattr(response, "text"):
            return response.text
        return str(response)
    except Exception as e:
        return f"⚠️ 오류 발생: {e}"

# ---------------------------
# 메인 앱
# ---------------------------
def main():
    st.set_page_config(page_title="Gemini 채팅", layout="centered")
    st.markdown(
        f"""
        <style>
            .chat-box {{
                background-color: #f9fafb;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
            }}
            .user-msg {{
                background-color: #d1e7ff;
                border-radius: 10px;
                padding: 10px 15px;
                margin: 5px 0;
            }}
            .assistant-msg {{
                background-color: #e8f5e9;
                border-radius: 10px;
                padding: 10px 15px;
                margin: 5px 0;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("💬 Gemini 채팅 앱")

    # API 키 확인
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("❌ st.secrets에 GEMINI_API_KEY가 없습니다.")
        return
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    # 세션 초기화
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "안녕하세요! 무엇이 궁금하신가요? 😊"}
        ]

    # ---------------------------
    # UI 구성
    # ---------------------------
    with st.container():
        for msg in st.session_state["messages"]:
            if msg["role"] == "user":
                st.markdown(f"<div class='user-msg'><b>🧑 사용자:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='assistant-msg'><b>🤖 Gemini:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # 입력창 (엔터키 + 버튼 지원)
    prompt = st.chat_input("질문을 입력하고 Enter를 눌러보세요!")

    if prompt:  # 엔터 또는 버튼 입력 시
        # 사용자 메시지 추가
        st.session_state["messages"].append({"role": "user", "content": prompt})
        # 응답 생성
        answer = generate_answer(prompt)
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        # Streamlit은 chat_input 입력 시 자동 rerun → rerun() 불필요

if __name__ == "__main__":
    main()
