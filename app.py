import streamlit as st
import google.generativeai as genai

def generate_answer(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        if hasattr(response, "text"):
            return response.text
        return str(response)
    except Exception as e:
        return f"⚠️ 오류 발생: {e}"

def main():
    st.set_page_config(page_title="Gemini 채팅", layout="centered")
    st.markdown(
        """
        <style>
            /* 전체 배경 투명도 및 폰트 스타일 */
            body, .stApp {
                font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
            }

            /* 채팅 말풍선 스타일 */
            .chat-box {
                border-radius: 12px;
                padding: 15px 18px;
                margin: 10px 0;
                font-size: 1rem;
                line-height: 1.5;
                word-break: keep-all;
            }

            /* 라이트 모드 */
            @media (prefers-color-scheme: light) {
                .user-msg {
                    background-color: #e8f0ff;
                    color: #1a1a1a;
                }
                .assistant-msg {
                    background-color: #e8f5e9;
                    color: #1a1a1a;
                }
            }

            /* 다크 모드 */
            @media (prefers-color-scheme: dark) {
                .user-msg {
                    background-color: #1a2b4c;
                    color: #f5f5f5;
                }
                .assistant-msg {
                    background-color: #253423;
                    color: #f5f5f5;
                }
            }

            /* 말풍선 내부 텍스트 정돈 */
            .msg-name {
                font-weight: 600;
                display: block;
                margin-bottom: 5px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("💬 Gemini 채팅 앱")

    # API 키 확인
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("❌ st.secrets에 GEMINI_API_KEY가 없습니다.")
        return
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "안녕하세요! 무엇이 궁금하신가요? 😊"}
        ]

    # 대화 표시
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(
                f"<div class='chat-box user-msg'><span class='msg-name'>🧑 사용자</span>{msg['content']}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='chat-box assistant-msg'><span class='msg-name'>🤖 Gemini</span>{msg['content']}</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ✅ chat_input은 엔터키 자동 전송 지원
    prompt = st.chat_input("질문을 입력하고 Enter를 눌러보세요!")

    if prompt:
        st.session_state["messages"].append({"role": "user", "content": prompt})
        answer = generate_answer(prompt)
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.rerun()

if __name__ == "__main__":
    main()
