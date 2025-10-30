import streamlit as st
import google.generativeai as genai

APP_VERSION = "v2-no-direct-session-write"  # 화면 좌상단에 떠서 버전 확인용

def main():
    st.title(f"채팅 앱 · {APP_VERSION}")

    # API 키 확인
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("st.secrets에 GEMINI_API_KEY가 없습니다. 키를 설정해 주세요.")
        return

    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    # 상태 초기화 (user_input 키는 만들지 않습니다!)
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "안녕하세요! 질문을 입력해 주세요."}
        ]
    if "input_reset" not in st.session_state:
        st.session_state["input_reset"] = 0  # 입력창 리셋용 카운터

    # 입력창: 리셋 카운터를 키에 반영 (키 변경 = 새 위젯 = 값 초기화)
    key_suffix = st.session_state["input_reset"]
    user_input = st.text_input("질문을 입력하세요", key=f"user_input_{key_suffix}")

    col1, col2 = st.columns([4, 1])
    with col1:
        submit = st.button("전송")
    with col2:
        clear = st.button("입력창 초기화")

    # 입력창 초기화 버튼 → 세션의 user_input을 건드리지 않고, 키만 바꿈
    if clear:
        st.session_state["input_reset"] += 1   # 새 키로 교체
        st.experimental_rerun()

    # 전송 처리
    if submit and user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})

        with st.spinner("응답 중..."):
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(user_input)
                assistant_text = getattr(response, "text", str(response))
            except Exception as e:
                assistant_text = f"오류 발생: {e}"

        st.session_state["messages"].append(
            {"role": "assistant", "content": assistant_text}
        )

        # 입력창 비우기: user_input 값을 직접 비우지 않고 키만 새로 만듦
        st.session_state["input_reset"] += 1
        st.experimental_rerun()

    # 대화 표시
    for msg in st.session_state["messages"]:
        role = msg["role"]
        try:
            with st.chat_message(role):
                st.markdown(msg["content"])
        except Exception:
            prefix = "사용자" if role == "user" else "앱"
            st.markdown(f"**{prefix}:** {msg['content']}")

if __name__ == "__main__":
    main()
