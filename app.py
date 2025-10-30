# ...existing code...
import streamlit as st
import google.generativeai as genai

def main():
    st.title('채팅 앱')

    if "GEMINI_API_KEY" not in st.secrets:
        st.error("st.secrets에 GEMINI_API_KEY가 없습니다. 키를 설정해 주세요.")
        return

    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    # 세션에 메시지 보관
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요! 질문을 입력해 주세요."}
        ]

    # 입력 UI
    user_input = st.text_input("질문을 입력하세요", key="user_input")
    submit = st.button("전송")

    # 전송 처리
    if submit and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("응답 중..."):
            try:
                model= genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(
                    contents=user_input,)
                # 응답 텍스트 추출(여러 형식에 대해 안전하게 처리)
                assistant_text = None
                if hasattr(response, "candidates") and response.candidates:
                    assistant_text = getattr(response.candidates[0], "content", None)
                if not assistant_text and hasattr(response, "output") and response.output:
                    assistant_text = getattr(response.output[0], "content", None)
                if not assistant_text and hasattr(response, "content"):
                    assistant_text = response.content
                if not assistant_text:
                    assistant_text = str(response)

            except Exception as e:
                assistant_text = f"오류 발생: {e}"

        st.session_state.messages.append({"role": "assistant", "content": assistant_text})
        # 입력창 초기화
        st.session_state.user_input = ""

    # 대화 표시
    for msg in st.session_state.messages:
        role = "assistant" if msg["role"] == "assistant" else "user"
        try:
            with st.chat_message(role):
                st.markdown(msg["content"])
        except Exception:
            # st.chat_message가 없는 환경 대비
            if role == "user":
                st.markdown(f"**사용자:** {msg['content']}")
            else:
                st.markdown(f"**앱:** {msg['content']}")

if __name__ == '__main__':
    main()
# ...existing code...