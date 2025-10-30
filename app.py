import streamlit as st
import google.generativeai as genai

APP_VERSION = "v4-enterkey-support"

def handle_submit():
    """엔터키로 입력 시 실행되는 콜백"""
    user_input = st.session_state.get("current_input", "").strip()
    if not user_input:
        return

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "안녕하세요! 질문을 입력해 주세요."}
        ]

    st.session_state["messages"].append({"role": "user", "content": user_input})

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(user_input)
        assistant_text = getattr(response, "text", str(response))
    except Exception as e:
        assistant_text = f"오류 발생: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": assistant_text})

    # 입력창 초기화 및 리렌더
    st.session_state["current_input"] = ""
    st.rerun()

def main():
    st.title(f"채팅 앱 · {APP_VERSION}")

    if "GEMINI_API_KEY" not in st.secrets:
        st.error("st.secrets에 GEMINI_API_KEY가 없습니다. 키를 설정해 주세요.")
        return

    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "안녕하세요! 질문을 입력해 주세요."}
        ]
    if "current_input" not in st.session_state:
        st.session_state["current_input"] = ""

    # ✅ 엔터키로 전송 가능 (on_change 콜백)
    user_input = st.text_input(
        "질문을 입력하세요",
        key="current_input",
        on_change=handle_submit,
    )

    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button("전송"):
            handle_submit()
    with col2:
        if st.button("입력창 초기화"):
            st.session_state["current_input"] = ""
            st.rerun()

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
